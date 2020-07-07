require.config({
  paths: {
    'jquery': 'vendor/jquery',
    'underscore': 'vendor/underscore',
    'backbone': 'vendor/backbone',
    'config': 'config',
    'utils': 'utils'
  },
  shim: {
    'backbone': {
      deps: ['underscore', 'jquery'],
      exports: 'Backbone'
    }
  }
});

define(['backbone', 'config', 'utils'], function(backbone, config, utils) {
  'use strict';
  return Backbone.View.extend({
    initialize: function() {
      $('#add-file-button').on('click', _.bind(function(e) {
        e.preventDefault();
        var file = $('input[name="add-file-input"]')[0].files[0];
        this.addFile(file);
      }, this));
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
          dataCollection.trigger('reset');
        },
        error: function(err) {
          utils.alertError('Failed to add the data file.\n' + err.statusText);
        }
      });
    },
    deleteFile: function(file) {
      $.ajax({
        url: config.data_url + '/' + file,
        type: 'DELETE',
        success: function() {
          utils.alertSuccess('Success! Data file is deleted.');
          dataCollection.trigger('reset');
        },
        error: function() {
          utils.alertError('Failed to delete the data file.');
        }
      });
    }
  });
});
