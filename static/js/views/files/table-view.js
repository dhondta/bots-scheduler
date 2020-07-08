require.config({
  paths: {
    'jquery': 'vendor/jquery',
    'underscore': 'vendor/underscore',
    'backbone': 'vendor/backbone',
    'bootstrap': 'vendor/bootstrap',
    'datatables': 'vendor/jquery.dataTables',
    'utils': 'utils',
    'config': 'config',
    'add-file-view': 'views/files/add-file-view',
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

define(['utils', 'config', 'add-file-view', 'backbone', 'bootstrap', 'datatables'],
       function(utils, config, AddFileView) {
  'use strict';
  var filesCollection;
  return Backbone.View.extend({
    initialize: function() {
      filesCollection = this.collection;
      this.listenTo(this.collection, 'sync', this.render);
      this.listenTo(this.collection, 'request', this.requestRender);
      this.listenTo(this.collection, 'reset', this.resetRender);
      this.listenTo(this.collection, 'error', this.requestError);
      this.table = $('#files-table').dataTable({'order': [[2, 'desc'], [1, 'asc']],
            "columnDefs": [{ "orderable": false, "className": "table-result-column", "width": "20px", "targets": 0 }]});
    },
    requestError: function(model, response, options) {
      this.spinner.stop();
      utils.alertError('Request failed: ' + response.responseText);
    },
    requestRender: function() {
      this.table.fnClearTable();
      this.spinner = utils.startSpinner('files-spinner');
    },
    resetRender: function(e) {
      if (e) {e.preventDefault();}
      this.collection.getFiles();
    },
    render: function() {
      var files = this.collection.files;
      var data = [];
      config.files_list = [];
      _.each(files, function(file) {
        config.files_list.push(file.attributes.filename);
        data.push([
          file.getDeleteIcon(),
          file.getFilenameHTMLString(),
          file.getCreatedAtString(),
          file.getEntriesCount(),
          file.getDescription()
        ]);
      });
      if (data.length) {
        var view = this;
        this.table.fnClearTable();
        this.table.fnAddData(data);
        var buttons = $('[data-action=delete-file]');
        _.each(buttons, function(btn) {
          $(btn).on('click', _.bind(function(e) {
            e.preventDefault();
            filesCollection.deleteFile(decodeURI($(btn).data('content')));
          }, this));
        });
      }
      utils.stopSpinner(this.spinner);
    }
  });
});
