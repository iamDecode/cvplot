<template>
  <div class="app">
    <contributions ref="contributions">
      <template v-slot="{features}">
        <lineplot v-for="feature in features" :key="feature" :feature="feature" />
      </template>
    </contributions>

  </div>
</template>

<script>
import Contributions from './components/Contributions.vue'
import Lineplot from './components/Lineplot.vue'

export default {
  name: 'App',
  components: { Contributions, Lineplot },
  data() {
    return {
      loading: false
    }
  }
}
</script>


<style lang="css">
	.app *:not(.fa) {
		color: unset;
		font-size: unset;
		font-family: unset;
		font-style: unset;
		border: unset;
		padding: unset;
		background: unset;
		margin: unset;
		border-radius: unset;
		position: unset;
		float: unset;
		top: unset;
		left: unset;
		right: unset;
		bottom: unset;
    box-sizing: border-box;
    -webkit-text-size-adjust: 100%;
    -webkit-tap-highlight-color: transparent;
	}

	/* Styles extracted from bootstrap, otherwise they interfere with jupyter itself */
	.app {
		margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
    font-size: 12px;
    font-weight: 400;
    line-height: 1.5;
    color: #212529;
    text-align: left;
    background-color: #fff;
    overflow-y: hidden;
    overflow-x: auto;
	}

	.app .text-center {
	  text-align: center;
	}

	.app .btn {
	  display: inline-block;
	  font-weight: 400;
	  color: #212529;
	  text-align: center;
	  vertical-align: middle;
	  -webkit-user-select: none;
	  -moz-user-select: none;
	  -ms-user-select: none;
	  user-select: none;
	  background-color: transparent;
	  border: 1px solid transparent;
	  padding: .375em .75em;
	  font-size: 1em;
	  line-height: 1.5;
	  border-radius: .25em;
	  transition: color .15s ease-in-out, background-color .15s ease-in-out, border-color .15s ease-in-out, box-shadow .15s ease-in-out
	}

	.app .btn:hover {
	  color: #212529;
	  text-decoration: none
	}

	.app .btn.focus,
	.app .btn:focus {
	  outline: 0;
	  box-shadow: 0 0 0 .2em rgba(0, 123, 255, .25)
	}

	.app .btn:not(:disabled):not(.disabled) {
	  cursor: pointer
	}

	.app .btn-secondary {
	  color: #fff;
	  background-color: #6c757d;
	  border-color: #6c757d
	}

	.app .btn-secondary:hover {
	  color: #fff;
	  background-color: #5a6268;
	  border-color: #545b62
	}

	.app .btn-secondary.focus,
	.app .btn-secondary:focus {
	  color: #fff;
	  background-color: #5a6268;
	  border-color: #545b62;
	  box-shadow: 0 0 0 .2em rgba(130, 138, 145, .5)
	}

	.app .btn-secondary.disabled,
	.app .btn-secondary:disabled {
	  color: #fff;
	  background-color: #6c757d;
	  border-color: #6c757d
	}

	.app .btn-secondary:not(:disabled):not(.disabled).active,
	.app .btn-secondary:not(:disabled):not(.disabled):active,
	.app .show>.btn-secondary.dropdown-toggle {
	  color: #fff;
	  background-color: #545b62;
	  border-color: #4e555b
	}

	.app .btn-secondary:not(:disabled):not(.disabled).active:focus,
	.app .btn-secondary:not(:disabled):not(.disabled):active:focus,
	.app .show>.btn-secondary.dropdown-toggle:focus {
	  box-shadow: 0 0 0 .2em rgba(130, 138, 145, .5)
	}

	.app .pr-0,
	.app .px-0 {
	  padding-right: 0 !important
	}


	.app .pl-0,
	.app .px-0 {
	  padding-left: 0 !important
	}

	.app .pr-3,
	.app .px-3 {
	  padding-right: 1em !important
	}

	.app .pl-3,
	.app .px-3 {
	  padding-left: 1em !important
	}

	.app .dropdown {
	  position: relative
	}

	.app .dropdown-toggle {
	  white-space: nowrap
	}

	.app .dropdown-toggle::after {
	  display: inline-block;
	  margin-left: .255em;
	  vertical-align: .255em;
	  content: "";
	  border-top: .3em solid;
	  border-right: .3em solid transparent;
	  border-bottom: 0;
	  border-left: .3em solid transparent
	}

	.app .dropdown-toggle:empty::after {
	  margin-left: 0
	}

	.app .dropdown-menu {
	  position: absolute;
	  top: 100%;
	  left: 0;
	  z-index: 1000;
	  display: none;
	  float: left;
	  min-width: 10em;
	  padding: .5em 0;
	  margin: .125em 0 0;
	  font-size: 1em;
	  color: #212529;
	  text-align: left;
	  list-style: none;
	  background-color: #fff;
	  background-clip: padding-box;
	  border: 1px solid rgba(0, 0, 0, .15);
	  border-radius: .25em
	}

	.app .dropdown-menu.show {
	  display: block
	}

	.app .dropdown-header {
	  display: block;
	  padding: .5em 1.5em;
	  margin-bottom: 0;
	  font-size: .875em;
	  color: #6c757d;
	  white-space: nowrap
	}

	.app .form-group {
	  margin-bottom: 1em
	}

	.app .custom-control {
	  position: relative;
	  z-index: 1;
	  display: block;
	  min-height: 1.5em;
	  padding-left: 1.5em;
	  -webkit-print-color-adjust: exact;
	  color-adjust: exact
	}

	.app .custom-control-input {
	  position: absolute;
	  left: 0;
	  z-index: -1;
	  width: 1em;
	  height: 1.25em;
	  opacity: 0
	}

	.app .custom-control-input:checked~.custom-control-label::before {
	  color: #fff;
	  border-color: #007bff;
	  background-color: #007bff
	}

	.app .custom-control-input:focus~.custom-control-label::before {
	  box-shadow: 0 0 0 .2em rgba(0, 123, 255, .25)
	}

	.app .custom-control-input:focus:not(:checked)~.custom-control-label::before {
	  border-color: #80bdff
	}

	.app .custom-control-input:not(:disabled):active~.custom-control-label::before {
	  color: #fff;
	  background-color: #b3d7ff;
	  border-color: #b3d7ff
	}

	.app .custom-control-input:disabled~.custom-control-label,
	.app .custom-control-input[disabled]~.custom-control-label {
	  color: #6c757d
	}

	.app .custom-control-input:disabled~.custom-control-label::before,
	.app .custom-control-input[disabled]~.custom-control-label::before {
	  background-color: #e9ecef
	}

	.app .custom-control-label {
	  position: relative;
	  margin-bottom: 0;
	  vertical-align: top
	}

	.app .custom-control-label::before {
	  position: absolute;
	  top: .25em;
	  left: -1.5em;
	  display: block;
	  width: 1em;
	  height: 1em;
	  pointer-events: none;
	  content: "";
	  background-color: #fff;
	  border: #adb5bd solid 1px
	}

	.app .custom-control-label::after {
	  position: absolute;
	  top: .25em;
	  left: -1.5em;
	  display: block;
	  width: 1em;
	  height: 1em;
	  content: "";
	  background: no-repeat 50%/50% 50%
	}

	.app .custom-switch {
	  padding-left: 2.25em
	}

	.app .custom-switch .custom-control-label::before {
	  left: -2.25em;
	  width: 1.75em;
	  pointer-events: all;
	  border-radius: .5em
	}

	.app .custom-switch .custom-control-label::after {
	  top: calc(.25em + 2px);
	  left: calc(-2.25em + 2px);
	  width: calc(1em - 4px);
	  height: calc(1em - 4px);
	  background-color: #adb5bd;
	  border-radius: .5em;
	  transition: background-color .15s ease-in-out, border-color .15s ease-in-out, box-shadow .15s ease-in-out, -webkit-transform .15s ease-in-out;
	  transition: transform .15s ease-in-out, background-color .15s ease-in-out, border-color .15s ease-in-out, box-shadow .15s ease-in-out;
	  transition: transform .15s ease-in-out, background-color .15s ease-in-out, border-color .15s ease-in-out, box-shadow .15s ease-in-out, -webkit-transform .15s ease-in-out
	}

	@media (prefers-reduced-motion:reduce) {
	  .app .custom-switch .custom-control-label::after {
	    transition: none
	  }
	}

	.app .custom-switch .custom-control-input:checked~.custom-control-label::after {
	  background-color: #fff;
	  -webkit-transform: translateX(.75em);
	  transform: translateX(.75em)
	}

	.app .custom-switch .custom-control-input:disabled:checked~.custom-control-label::before {
	  background-color: rgba(0, 123, 255, .5)
	}

	.app .custom-range {
	  width: 100%;
	  height: 1.4em;
	  padding: 0;
	  background-color: transparent;
	  -webkit-appearance: none;
	  -moz-appearance: none;
	  appearance: none
	}

	.app .custom-range:focus {
	  outline: 0
	}

	.app .custom-range:focus::-webkit-slider-thumb {
	  box-shadow: 0 0 0 1px #fff, 0 0 0 .2em rgba(0, 123, 255, .25)
	}

	.app .custom-range:focus::-moz-range-thumb {
	  box-shadow: 0 0 0 1px #fff, 0 0 0 .2em rgba(0, 123, 255, .25)
	}

	.app .custom-range:focus::-ms-thumb {
	  box-shadow: 0 0 0 1px #fff, 0 0 0 .2em rgba(0, 123, 255, .25)
	}

	.app .custom-range::-moz-focus-outer {
	  border: 0
	}

	.app .custom-range::-webkit-slider-thumb {
	  width: 1em;
	  height: 1em;
	  margin-top: -.25em;
	  background-color: #007bff;
	  border: 0;
	  border-radius: 1em;
	  -webkit-transition: background-color .15s ease-in-out, border-color .15s ease-in-out, box-shadow .15s ease-in-out;
	  transition: background-color .15s ease-in-out, border-color .15s ease-in-out, box-shadow .15s ease-in-out;
	  -webkit-appearance: none;
	  appearance: none
	}

	@media (prefers-reduced-motion:reduce) {
	  .app .custom-range::-webkit-slider-thumb {
	    -webkit-transition: none;
	    transition: none
	  }
	}

	.app .custom-range::-webkit-slider-thumb:active {
	  background-color: #b3d7ff
	}

	.app .custom-range::-webkit-slider-runnable-track {
	  width: 100%;
	  height: .5em;
	  color: transparent;
	  cursor: pointer;
	  background-color: #dee2e6;
	  border-color: transparent;
	  border-radius: 1em
	}

	.app .custom-range::-moz-range-thumb {
	  width: 1em;
	  height: 1em;
	  background-color: #007bff;
	  border: 0;
	  border-radius: 1em;
	  -moz-transition: background-color .15s ease-in-out, border-color .15s ease-in-out, box-shadow .15s ease-in-out;
	  transition: background-color .15s ease-in-out, border-color .15s ease-in-out, box-shadow .15s ease-in-out;
	  -moz-appearance: none;
	  appearance: none
	}

	.app @media (prefers-reduced-motion:reduce) {
	  .custom-range::-moz-range-thumb {
	    -moz-transition: none;
	    transition: none
	  }
	}

	.app .custom-range::-moz-range-thumb:active {
	  background-color: #b3d7ff
	}

	.app .custom-range::-moz-range-track {
	  width: 100%;
	  height: .5em;
	  color: transparent;
	  cursor: pointer;
	  background-color: #dee2e6;
	  border-color: transparent;
	  border-radius: 1em
	}

	.app .custom-range::-ms-thumb {
	  width: 1em;
	  height: 1em;
	  margin-top: 0;
	  margin-right: .2em;
	  margin-left: .2em;
	  background-color: #007bff;
	  border: 0;
	  border-radius: 1em;
	  -ms-transition: background-color .15s ease-in-out, border-color .15s ease-in-out, box-shadow .15s ease-in-out;
	  transition: background-color .15s ease-in-out, border-color .15s ease-in-out, box-shadow .15s ease-in-out;
	  appearance: none
	}

	.app @media (prefers-reduced-motion:reduce) {
	  .custom-range::-ms-thumb {
	    -ms-transition: none;
	    transition: none
	  }
	}

	.app .custom-range::-ms-thumb:active {
	  background-color: #b3d7ff
	}

	.app .custom-range::-ms-track {
	  width: 100%;
	  height: .5em;
	  color: transparent;
	  cursor: pointer;
	  background-color: transparent;
	  border-color: transparent;
	  border-width: .5em
	}

	.app .custom-range::-ms-fill-lower {
	  background-color: #dee2e6;
	  border-radius: 1em
	}

	.app .custom-range::-ms-fill-upper {
	  margin-right: 15px;
	  background-color: #dee2e6;
	  border-radius: 1em
	}

	.app .custom-range:disabled::-webkit-slider-thumb {
	  background-color: #adb5bd
	}

	.app .custom-range:disabled::-webkit-slider-runnable-track {
	  cursor: default
	}

	.app .custom-range:disabled::-moz-range-thumb {
	  background-color: #adb5bd
	}

	.app .custom-range:disabled::-moz-range-track {
	  cursor: default
	}

	.app .custom-range:disabled::-ms-thumb {
	  background-color: #adb5bd
	}

	.app .d-inline-flex {
	  display: -ms-inline-flexbox !important;
	  display: inline-flex !important
	}

	.app h5 {
		font-size: 1.75em !important;
		margin-top: 0 !important;
		margin-bottom: .5em !important;
		font-weight: 500 !important;
		line-height: 1.2 !important;
	}
</style>
