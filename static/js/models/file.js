require.config({
  paths: {
    'jquery': 'vendor/jquery',
    'underscore': 'vendor/underscore',
    'backbone': 'vendor/backbone',
    'moment': 'vendor/moment'
  },
  shim: {
    'backbone': {
      deps: ['underscore', 'jquery'],
      exports: 'Backbone'
    }
  }
});

define(['backbone', 'vendor/moment-timezone-with-data'], function(backbone, moment) {
  'use strict';
  return Backbone.Model.extend({
    getFilenameHTMLString: function() {
      return this.get('filename');
    },
    getCreatedAtString: function() {
      return moment(this.get('created_time')).local().format('MM/DD/YYYY HH:mm:ss Z');
    },
    getDescription: function() {
      return this.get('description');
    },
    getEntriesCount: function() {
      return this.get('entries');
    }
  });
});
