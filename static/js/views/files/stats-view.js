require.config({
  paths: {
    'jquery': 'vendor/jquery',
    'underscore': 'vendor/underscore',
    'backbone': 'vendor/backbone',
    'bootstrap': 'vendor/bootstrap'
  },
  shim: {
    'bootstrap': {
      deps: ['jquery']
    },
    'backbone': {
      deps: ['underscore', 'jquery'],
      exports: 'Backbone'
    }
  }
});

define(['backbone', 'bootstrap'], function() {
  'use strict';
  return Backbone.View.extend({
    initialize: function() {
      this.listenTo(this.collection, 'sync', this.render);
    },
    render: function() {
      $('#files-total-count').text(this.collection.getTotal());
    }
  });
});
