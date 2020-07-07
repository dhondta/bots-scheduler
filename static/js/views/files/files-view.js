require.config({
  paths: {
    'jquery': 'vendor/jquery',
    'underscore': 'vendor/underscore',
    'backbone': 'vendor/backbone',
    'bootstrap': 'vendor/bootstrap',
    'add-file-view': 'views/files/add-file-view',
    'files-filter-view': 'views/files/filter-view',
    'files-stats-view': 'views/files/stats-view',
    'files-table-view': 'views/files/table-view'
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

define(['add-file-view', 'files-filter-view', 'files-stats-view', 'files-table-view',
        'backbone', 'bootstrap'], function(AddFileView, FilesFilterView, FilesStatsView, FilesTableView) {
  'use strict';
  return Backbone.View.extend({
    initialize: function() {
      new AddFileView({collection: this.collection});
      new FilesFilterView({collection: this.collection});
      new FilesStatsView({collection: this.collection});
      new FilesTableView({collection: this.collection});
    }
  });
});
