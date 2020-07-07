require.config({
  paths: {
    'jquery': 'vendor/jquery',
    'underscore': 'vendor/underscore',
    'backbone': 'vendor/backbone',
    'bootstrap': 'vendor/bootstrap',
    'datatables': 'vendor/jquery.dataTables',
    'utils': 'utils',
    'text': 'vendor/text'
  },
  shim: {
    'bootstrap': {
      deps: ['jquery']
    },
    'backbone': {
      deps: ['underscore', 'jquery'],
      exports: 'Backbone'
    },
    'datatables': {
      deps: ['jquery'],
      exports: '$.fn.dataTable'
    }
  }
});

define(['utils', 'backbone', 'bootstrap', 'datatables'], function(utils) {
  'use strict';
  return Backbone.View.extend({
    initialize: function() {
      this.listenTo(this.collection, 'sync', this.render);
      this.listenTo(this.collection, 'request', this.requestRender);
      this.listenTo(this.collection, 'error', this.requestError);
      this.table = $('#files-table').dataTable({'order': [[1, 'desc'], [0, 'asc']]});
    },
    requestError: function(model, response, options) {
      this.spinner.stop();
      utils.alertError('Request failed: ' + response.responseText);
    },
    requestRender: function() {
      this.table.fnClearTable();
      this.spinner = utils.startSpinner('files-spinner');
    },
    render: function() {
      var files = this.collection.files;
      var data = [];
      _.each(files, function(file) {
        data.push([
          file.getFilenameHTMLString(),
          file.getCreatedAtString(),
          file.getEntriesCount(),
          file.getDescription()
        ]);
      });
      if (data.length) {
        this.table.fnClearTable();
        this.table.fnAddData(data);
      }
      utils.stopSpinner(this.spinner);
    }
  });
});
