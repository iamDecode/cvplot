<template>
  <div class="app">
    Test {{ test }}
  </div>
</template>

<script>
export default {
  name: 'App',
  props: { test: { type: String, default: "seems to work" } },
  mounted() {
  	console.log("mounted!")
  },
  watch: {
  	test(value) {
  		console.log("Test changed to: " + value)
  	}
  }
}
</script>

<style lang="scss" scoped>
</style>
