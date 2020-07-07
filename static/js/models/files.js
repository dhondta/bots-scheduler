require.config({
  paths: {
    'jquery': 'vendor/jquery',
    'underscore': 'vendor/underscore',
    'backbone': 'vendor/backbone',
    'utils': 'utils',
    'config': 'config',
    'fileModel': 'models/file'
  },
  shim: {
    'backbone': {
      deps: ['underscore', 'jquery'],
      exports: 'Backbone'
    }
  }
});

define(['utils', 'fileModel', 'config', 'backbone'], function(utils, FileModel, config, backbone) {
  return Backbone.Collection.extend({
    getTotal: function() {
      return this.files.length;
    },
    getFiles: function() {
      this.url = config.files_url;
      this.fetch();
    },
    getFilesByRange: function(start, end) {
      this.url = config.files_url + '?time_range_end=' + end + '&time_range_start=' + start;
      this.fetch();
    },
    parse: function(response) {
      var files = response.files;
      this.files = [];
      _.each(files, function(file) {
        this.files.push(new FileModel(file));
      }, this);
      return this.files;
    }
  });
});
