<template>
  <div class="lineplot">
    <h5 class="text-center">{{feature}}</h5>
    <svg ref="svg" :style="{marginTop: -35 + 'px'}" />
    <canvas ref="canvas" />
  </div>
</template>

<script>
  import * as d3 from 'd3'
  import * as PIXI from 'pixi.js'
  import segmentsIntersect from 'robust-segment-intersect'

  Object.defineProperty(Array.prototype, 'maxIndex', {
    get: function() {
      return this.reduce((iMax, x, i, arr) => x > arr[iMax] ? i : iMax, 0)
    }
  })

  export default {
    name: 'lineplot',
    props: ['feature'],
    data() {
      const margin = {top: 10, right: 15, bottom: 10, left: 30}
      return {
        margin: margin,
        selection: [null, null],
        performanceMode: true
      }
    },
    computed: {
      width() {
        return 350 - this.margin.left - this.margin.right
      },
      height() {
        return 300 - this.margin.top - this.margin.bottom
      }
    },
    mounted() {
      const svg = d3.select(this.$refs.svg);

      this.x = this.$parent.lines[this.feature][0].map(z => z[0])
      this.y = this.$parent.lines[this.feature].map(x => x.map(z => z[1]))
      this.values = this.$parent.values[this.feature]

      Object.defineProperty(this, 'pred', { get: function() { return this.$parent.yhat } })
      //Object.defineProperty(this, 'r2', { get: function() { return this.$parent.r2 } })
      Object.defineProperty(this, 'classes', { get: function() { return this.$parent.classes } })

      Object.defineProperty(this, 'lineThreshold', { get: function() { return this.$parent.lineThreshold } })
      Object.defineProperty(this, 'fadeLine', { get: function() { return this.$parent.fadeLine } })
      Object.defineProperty(this, 'showPoints', { get: function() { return this.$parent.showPoints } })
      Object.defineProperty(this, 'averageData', { get: function() { return this.$parent.averageData } })

      if (this.$parent.contributions != null) {
        const index = this.$parent.features.indexOf(this.feature)
        this.contributions = this.$parent.contributions.map(x => x[index])
      } else {
        console.error("backend does not provide contributions2 (contributions of the actual data values). Falling back to inacurate estimation!")
        this.contributions = this.values.map((v, i) => {
          // Index of contribution closest to v
          let index = this.x.reduce((iMax, x, i, arr) => Math.abs(v - x) < Math.abs(v - arr[iMax]) ? i : iMax, 0)
          return this.y[i][index]
        })
      }

      const g = svg.append('g')
        .attr('transform', `translate(${this.margin.left}, ${this.margin.top})`)

      this.xScale = d3.scaleLinear().range([0, this.width])
      this.xAxis = g.append('g')
      this.yScale = d3.scaleLinear().range([this.height, 0])
      this.yAxis = g.append('g')

      d3.select(this.$el).selectAll('canvas')
        .style('transform', `translate(${this.margin.left}px, ${this.margin.top}px)`)
        .style('width', this.width + 'px')
        .style('height', this.height + 'px')

      this.renderer = PIXI.autoDetectRenderer({
        width: this.width,
        height: this.height,
        view: this.$refs.canvas,
        transparent: true,
        antialias: true,
        resolution: 2
      })

      this.stage = new PIXI.Container()
      this.g = new PIXI.Graphics()
      this.g2 = new PIXI.Graphics()
      this.stage.addChild(this.g)
      this.stage.addChild(this.g2)

      this.gselection = svg.append('g')
      d3.select(this.$refs.canvas).call(
        d3.drag()
          .on("start", this.brushstart)
          .on("drag", this.brushmove)
          .on("end", this.brushend)
      )

      this.update()
    },
    methods: {
      update(possible, selected) {
        if(this.x == null || this.y == null || this.pred == null) {
          return
        }

        if(this.averageData && this.y.length != 1) {
          this.y = [this.y[0].map((d,i) => d3.mean(this.y.map(x => x[i])))]
          this.values = [d3.mean(this.values)]
          this.contributions = this.values.map((v,i) => {
            let index = this.x.reduce((iMax, x, i, arr) => Math.abs(v - x) < Math.abs(v - arr[iMax]) ? i : iMax, 0)
            return this.y[i][index]
          })
        } else if (!this.averageData && this.y.length == 1) {
          this.y = this.$parent.lines[this.feature].map(x => x.map(z => z[1]))
          this.values = this.$parent.values[this.feature]
          this.contributions = this.values.map((v,i) => {
            let index = this.x.reduce((iMax, x, i, arr) => Math.abs(v - x) < Math.abs(v - arr[iMax]) ? i : iMax, 0)
            return this.y[i][index]
          })
        }

        this._selected = selected

        this.xScale.domain(d3.extent(this.x))
        this.rangeSize = this.xScale.range()[1] - this.xScale.range()[0]

        const extents = Object.values(this.$parent.lines).map(x => x.map(x => d3.extent(x.map(x => x[1]))))
        let extent = extents.map(x => x.reduce((a, b) => [Math.min(a[0], b[0]), Math.max(a[1], b[1])]))
        extent = extent.reduce((a, b) => [Math.min(a[0], b[0]), Math.max(a[1], b[1])])
        this.yScale.domain(extent).nice()

        this.xAxis.attr("transform", `translate(0, ${this.yScale(0)})`).call(d3.axisBottom(this.xScale))
        this.yAxis.call(d3.axisLeft(this.yScale))

        this.g.clear()

        let numPossible = 0
        let numSelected = 0
        if (possible != null) numPossible = possible.filter(x => x).length
        if (selected != null) numSelected = selected.filter(x => x).length

        // Line smoothing
        const tension = 0
        const k = (1 - tension) / 6

        this.y.forEach((line, i) => {
          const originalValue = this.xScale(this.values[i])

          const pred = this.pred[i]
          let width = 1
          let opacity = 0.2
          let color =  0x515263

          if (numPossible > 0) {
            if (possible[i]) {
              color = 0x007bff
              opacity = 1 / Math.pow(numPossible, 0.2)
            } else {
              opacity = 0.08
            }
          }
          if (numSelected > 0) {
            if (selected[i]) {
              color = 0x007bff
              opacity = 1 / Math.pow(numSelected, 0.2)
            } else {
              opacity = 0.08
            }
          }

          if (this.averageData) {
            width = 2
            opacity = 1
          }

          let x0, y0, x1, y1, x2, y2;

          line.forEach((yv, pi) => {
            const x = this.xScale(this.x[pi])
            const y = this.yScale(yv)

            if(width == 1) {
              this.g.lineStyle({color: color, width: width, alpha: opacity, native: true})
            } else {
              this.g.lineStyle({color: color, width: width, alpha: opacity})
            }

            switch (pi) {
              case 0:
                this.g.moveTo(x,y)
                break
              case 1:
                x1 = x
                y1 = y
                break
              default:
                this.point(x0, y0, x1, y1, x2, y2, x, y, k, [originalValue, opacity, color, width])
            }

            x0 = x1, x1 = x2, x2 = x
            y0 = y1, y1 = y2, y2 = y
          })

          this.point(x0, y0, x1, y1, x2, y2, x2, y2, k, [originalValue, opacity, color, width])
        })

        this.g2.clear()
        if (this.showPoints) {
          this.values.forEach((point, i) => {
            let color = 0x515263
            let opacity = 0.3
            if (numSelected > 0) {
              if (selected[i]) {
                color = 0x007bff
                opacity = 1
              } else {
                opacity = 0.06
              }
            }

            if (this.averageData) {
              opacity = 1
            }

            this.g2.beginFill(color, opacity);
            const radius = this.averageData ? 5 : 2;
            this.g2.drawCircle(this.xScale(point), this.yScale(this.contributions[i]), radius)
            this.g2.endFill();
          })
        }

        this.renderer.render(this.stage)
      },
      point(x0, y0, x1, y1, x2, y2, x, y, k, lineFadeParams) {
        this.bezierCurveTo(
          x1,
          y1,
          x1 + (k * (x2 - x0)),
          y1 + (k * (y2 - y0)),
          x2 + (k * (x1 - x)),
          y2 + (k * (y1 - y)),
          x2,
          y2,
          lineFadeParams
        )
      },
      bezierCurveTo(fromX, fromY, cpX, cpY, cpX2, cpY2, toX, toY, lineFadeParams) {
        const n = 6
        let dt, dt2, dt3, t2, t3 = 0

        for (let t = 1/n; t <= 1; t+=1/n) {
          t2 = t * t
          t3 = t2 * t

          dt = (1 - t)
          dt2 = t2 - 2*t + 1
          dt3 = -t3 + 3*t2 - 3*t + 1

          const x = (dt3 * fromX) + (3 * dt2 * t * cpX) + (3 * dt * t2 * cpX2) + (t3 * toX)
          const y = (dt3 * fromY) + (3 * dt2 * t * cpY) + (3 * dt * t2 * cpY2) + (t3 * toY)

          if (!this.fadeLine) {
            this.g.lineTo(x, y)
            continue
          }

          let offset = Math.abs(lineFadeParams[0] - x) / this.rangeSize
          offset = offset / this.lineThreshold
          const newOpacity = Math.min(1, lineFadeParams[1] * 2 * (1 - offset))

          if (newOpacity > 0.01) {
            const color = lineFadeParams[2]
            const width = lineFadeParams[3]
            if(width == 1) {
              this.g.lineStyle({color: color, width: width, alpha: newOpacity, native: true})
            } else {
              this.g.lineStyle({color: color, width: width, alpha: newOpacity})
            }
            this.g.lineTo(x, y)
          } else {
            this.g.moveTo(x, y)
          }
        }
      },
      intersecting() {
        if (this.selection[1] == null) return null

        const transformedSelection = [
          [this.xScale.invert(this.selection[0].x - this.margin.left), this.yScale.invert(this.selection[0].y - this.margin.top)],
          [this.xScale.invert(this.selection[1].x - this.margin.left), this.yScale.invert(this.selection[1].y - this.margin.top)],
        ]

        return this.$parent.lines[this.feature].map((line, i) => {
          return line.some((point, pi) => {
            if (pi == 0) return false;
            return segmentsIntersect(transformedSelection[0], transformedSelection[1], line[pi-1], point)
          })
        })
      },
      draw() {
        this.update()
      },
      brushstart() {
        this.$parent.updateSelection([{x: d3.event.x, y: d3.event.y}, null])
        if (this.selection[1] != null) {
          this.$parent.updateSelected(null)
        }
      },
      brushmove() {
        const x = d3.event.x
        const y = d3.event.y

        const length = (Math.abs(this.selection[0].x - x)**2 + Math.abs(this.selection[0].y - y)**2)
        if (length < 50) {
          if (this.selection[1] != null) {
            this.$parent.updateSelection([this.selection[0], null])
          }
          return
        }

        this.selection[1] = {x: x, y: y}

        const circles = this.gselection.selectAll('circle').data(this.selection)
        circles.exit().remove()
        circles.enter()
          .append('circle')
          .attr('fill', '#007bff')
          .attr('r', 3)

        this.gselection.selectAll('circle')
          .attr('cx', d => d.x)
          .attr('cy', d => d.y)

        const line = this.gselection.selectAll('line').data([this.selection])
        line.exit().remove()
        line.enter()
          .append('line')
          .attr('stroke', '#007bff')
          .attr('stroke-width', '2px')
          .attr('r', 3)

        this.gselection.selectAll('line')
          .attr('x1', d => d[0].x)
          .attr('y1', d => d[0].y)
          .attr('x2', d => d[1].x)
          .attr('y2', d => d[1].y)

        if (!this.performanceMode) {
          this.$parent.updatePossible(this.intersecting())
        }
      },
      updateSelection(selection) {
        this.gselection.selectAll("*").remove()
        this.selection = selection
      },
      updatePossible(values) {
        this.update(values, null)
      },
      brushend() {
        this.$parent.updateSelected(this.intersecting())
      },
      updateSelected(values) {
        this.update(null, values)
      }
    },
    beforeDestroy() {
      if (this.stage != null) {
        this.stage.destroy()
        this.stage = null
      }
      if (this.renderer != null) {
        this.renderer.destroy()
        this.renderer = null
      }
    }
  }
</script>

<style lang="css">
  .app div.contribution div.lineplot {
    --width: 350px;
    --height: 300px;
    position: relative;
    width: var(--width);
    height: var(--height);
    margin: -1px -1px 0 0;
  }

  .app div.contribution div.lineplot:not(:last-child) {
    margin-right: 20px;
  }

  .app div.contribution div.lineplot h5 {
    pointer-events: none;
    margin: 0  !important;
    font-size: 20px !important;
    height: 35px !important;
    line-height: 35px !important;
  }

  .app div.contribution div.lineplot svg {
    position: relative;
    width: var(--width);
    height: var(--height);
  }

  .app div.contribution div.lineplot canvas {
    position: absolute;
    top: 0;
    left: 0;
  }

  .app div.contribution div.lineplot g.lasso path {
    stroke: #007bff;
    stroke-width: 2px;
  }

  .app div.contribution div.lineplot g.lasso .drawn {
    fill: #007bff;
    fill-opacity: 0.2;
  }

  .app div.contribution div.lineplot g.lasso .loop_close {
    fill: none;
    stroke-dasharray: 4, 4;
  }

  .app div.contribution div.lineplot g.lasso .origin {
    fill: #007bff;
    fill-opacity: 0.5;
  }
</style>
