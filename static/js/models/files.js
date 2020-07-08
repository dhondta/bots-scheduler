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
  var filesCollection;
  return Backbone.Collection.extend({
    initialize: function(options) {
      filesCollection = this;
    },
    getTotal: function() {
      return this.files.length;
    },
    getFiles: function() {
      this.url = config.files_url;
      this.fetch();
      config.files_list = [];
      _.forEach(this.files, function(file) {config.files_list.push(file.attributes.filename)});
    },
    getFilesByRange: function(start, end) {
      this.url = config.files_url + '?time_range_end=' + end + '&time_range_start=' + start;
      this.fetch();
    },
    addFile: function(file) {
      var data = new FormData();
      data.append('file', file);
      $.ajax({
        url: config.files_url,
        type: 'POST',
        data: data,
        contentType: false,
        processData: false,
        cache: false,
        success: function() {
          utils.alertSuccess('Success! Data file is added.');
          filesCollection.trigger('reset');
          config.files_list.push(file.name);
        },
        error: function(err) {
          utils.alertError('Failed to add the data file.\n' + err.statusText);
        }
      });
    },
    deleteFile: function(file) {
      $.ajax({
        url: config.files_url + '/' + file,
        type: 'DELETE',
        success: function() {
          utils.alertSuccess('Success! Data file is deleted.');
          filesCollection.trigger('reset');
          config.files_list = $.grep(config.files_list, function(v) {return v != file});
        },
        error: function(err) {
          utils.alertError('Failed to delete the data file.');
        }
      });
    },
    parse: function(response) {
      var files = response.files;
      this.files = [];
      _.each(files, function(file) {
        this.files.push(new FileModel(file));
      }, this);
      config.files_list = [];
      _.forEach(this.files, function(file) {config.files_list.push(file.attributes.filename)});
      return this.files;
    }
  });
});
