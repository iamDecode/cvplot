<template>
  <div class="contribution">
    <div class="dropdown" :class="{'show': menuOpen}">
      <button class="btn btn-secondary dropdown-toggle" type="button" id="plotSettings" aria-haspopup="true" :aria-expanded="menuOpen" data-offset="0,10" @click="menuOpen = !menuOpen">
        <i class="fa fa-cog"></i>
      </button>

      <div class="dropdown-menu" :class="{'show': menuOpen}" aria-labelledby="plotSettings">
        <div class="px-3">
          <div class="form-group">
            <h6 class="dropdown-header px-0">Average data</h6>
            <div class="custom-control custom-switch" style="line-height: 1.5">
              <input type="checkbox" class="custom-control-input" id="averageData" v-model="averageData" @change="updateChildren">
              <label class="custom-control-label" for="averageData">Enabled</label>
            </div>
          </div>
          <div class="form-group">
            <h6 class="dropdown-header px-0">Show data points</h6>
            <div class="custom-control custom-switch" style="line-height: 1.5">
              <input type="checkbox" class="custom-control-input" id="showDataPoints" v-model="showPoints" @change="updateChildren">
              <label class="custom-control-label" for="showDataPoints">Enabled</label>
            </div>
          </div>
          <div class="form-group">
            <h6 class="dropdown-header px-0">Fade line</h6>
            <div class="custom-control custom-switch" style="line-height: 1.5">
              <input type="checkbox" class="custom-control-input" id="fadeLineSwitch" v-model="fadeLine" @change="updateChildren">
              <label class="custom-control-label" for="fadeLineSwitch">Enabled</label>
            </div>
          </div>
          <div class="form-group">
            <h6 class="dropdown-header px-0">Fade threshold</h6>
            <div style="white-space: nowrap">
              <input type="range" class="custom-range" min="0.01" max="0.5" step="0.05" v-model="lineThreshold" @change="updateChildren">
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="d-inline-flex">
      <slot :features="features" />
    </div>
  </div>
</template>

<script>
  Array.prototype.toDict = function() {
    return this.reduce((obj, kv) => Object.assign(obj, kv), {})
  }

  export default {
    name: 'contributions',
    data() {
      return {
        features: [],
        classes: [],
        targetClass: 0,
        menuOpen: false,
        averageData: false,
        showPoints: false,
        fadeLine: true,
        lineThreshold: 0.15
      }
    },
    methods: {
      update(data) {
        if (_.isEmpty(data)) return

        this.values = data.features.map((feature, i) => ({[feature]: data.values.map(v => v[i])})).toDict()
        this.lines = data.contributions
        this.contributions = data.contributions2
        this.yhat = data.yhat
        this.predictions = data.predictions
        this.features = data.features
        this.classes = data.classes

        this.$nextTick(_ => { // Delay to ensure every component got the right feature assigned
          this.updateChildren()
        })
      },
      updateChildren() {
        this.$children.forEach(component => component.update(null, component._selected))
      },
      updateSelection(selection) {
        this.$children.forEach(component => component.updateSelection(selection))
      },
      updatePossible(values) {
        this.$children.forEach(component => component.updatePossible(values))
      },
      updateSelected(values) {
        this.$children.forEach(component => component.updateSelected(values))
      }
    }
  }
</script>

<style lang="css">
  .app div.contribution {
    position: relative;
    display: inline-block;
  }

  .app div.contribution .dropdown {
    position: absolute !important;
    top: 10px;
    right: 10px;
    transform: translateX(100%);
    z-index: 99999;
  }

  .app div.contribution .dropdown-menu {
    padding: 0;
  }
</style>
