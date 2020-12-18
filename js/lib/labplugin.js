var plugin = require('./index');
var base = require('@jupyter-widgets/base');

module.exports = {
  id: 'cvplot',
  requires: [base.IJupyterWidgetRegistry],
  activate: function(app, widgets) {
      widgets.registerWidget({
          name: 'cvplot',
          version: plugin.version,
          exports: plugin
      });
  },
  autoStart: true
};

