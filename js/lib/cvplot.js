var widgets = require('@jupyter-widgets/base');
var _ = require('lodash');
var Vue = require('vue').default;
var App = require('./App.vue').default;

// See example.py for the kernel counterpart to this file.


// Custom Model. Custom widgets models must at least provide default values
// for model attributes, including
//
//  - `_view_name`
//  - `_view_module`
//  - `_view_module_version`
//
//  - `_model_name`
//  - `_model_module`
//  - `_model_module_version`
//
//  when different from the base class.

// When serialiazing the entire widget state for embedding, only values that
// differ from the defaults will be specified.
var Model = widgets.DOMWidgetModel.extend({
  defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
    _model_name : 'Model',
    _view_name : 'View',
    _model_module : 'cvplot',
    _view_module : 'cvplot',
    _model_module_version : '0.1.0',
    _view_module_version : '0.1.0',
    value : {}
  })
});

var vm = new Vue({
  render: h => h(App)
}).$mount();


// Custom View. Renders the widget model.
var View = widgets.DOMWidgetView.extend({
  // Defines how the widget gets rendered into the DOM
  render: function() {
    this.value_changed();

    this.el.appendChild(vm.$el);

    // Observe changes in the data traitlet in Python, and define
    // a custom callback.
    this.model.on('change:value', this.value_changed, this);
  },

  value_changed: function() {
    const value = this.model.get('value')
    console.log('called!', value)
    vm.$children[0].$nextTick(function() {
    	this.$refs.contributions.update(value)
    })
  }
});


module.exports = {
  Model: Model,
  View: View
};
