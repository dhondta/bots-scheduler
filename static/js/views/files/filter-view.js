require.config({
  paths: {
    'jquery': 'vendor/jquery',
    'underscore': 'vendor/underscore',
    'backbone': 'vendor/backbone',
    'bootstrap': 'vendor/bootstrap',
    'moment': 'vendor/moment'
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

define(['backbone', 'bootstrap', 'moment'], function(backbone, bootstrap, moment) {
  'use strict';
  return Backbone.View.extend({
    initialize: function() {
      $('#files-filter-button').on('click', _.bind(this.filterTable, this));
    },
    filterTable: function(e) {
      e.preventDefault();
      var range = parseInt($('#files-filter-time-range').val(), 10);
      var end = moment();
      var start = moment().subtract(range, 'second');
      this.collection.getFilesByRange(start.toISOString(), end.toISOString());
    }
  });
});
