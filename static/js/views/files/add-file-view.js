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
        this.collection.addFile(file);
        //this.collection.parse();
      }, this));
    }
  });
});
