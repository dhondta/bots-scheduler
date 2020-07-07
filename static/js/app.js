require.config({
  urlArgs: 'bust=' + cacheBuster,
  baseUrl: '/static/js',
  paths: {
    'jquery': 'vendor/jquery',
    'backbone': 'vendor/backbone',
    'underscore': 'vendor/underscore',
    'jobs-view': 'views/jobs/jobs-view',
    'jobs-collection': 'models/jobs',
    'executions-view': 'views/executions/executions-view',
    'executions-collection': 'models/executions',
    'files-view': 'views/files/files-view',
    'files-collection': 'models/files',
    'logs-view': 'views/logs/logs-view',
    'logs-collection': 'models/logs'
  },
  shim: {
    'backbone': {
      deps: ['underscore', 'jquery'],
      exports: 'Backbone'
    }
  }
});

require(['jobs-view', 'executions-view', 'files-view', 'logs-view',
         'jobs-collection', 'executions-collection', 'files-collection', 'logs-collection',
         'backbone'], function(JobsView, ExecutionsView, FilesView, LogsView,
                               JobsCollection, ExecutionsCollection, FilesCollection, LogsCollection) {
  'use strict';
  var jobsCollection = new JobsCollection();
  new JobsView({collection: jobsCollection});
  var executionsCollection = new ExecutionsCollection();
  new ExecutionsView({collection: executionsCollection});
  var filesCollection = new FilesCollection();
  new FilesView({collection: filesCollection});
  var logsCollection = new LogsCollection();
  new LogsView({collection: logsCollection});

  var AppRouter = Backbone.Router.extend({
    routes: {
      'jobs': 'jobsRoute',
      'jobs/:jid': 'jobsRoute',
      'executions': 'executionsRoute',
      'executions/:eid': 'executionsRoute',
      'files': 'filesRoute',
      'logs': 'logsRoute',
      '*actions': 'defaultRoute'
    }
  });

  var switchTab = function(switchTo) {
    var pages = ['jobs', 'executions', 'files', 'logs'];
    _.each(pages, function(page) {
      $('#' + page + '-page-sidebar').hide();
      $('#' + page + '-page-content').hide();
      $('#' + page + '-tab').removeClass();
    });
    $('#' + switchTo + '-page-sidebar').show();
    $('#' + switchTo + '-page-content').show();
    $('#' + switchTo + '-tab').addClass('active');
  };

  var appRouter = new AppRouter;
  appRouter.on('route:jobsRoute', function(jobId) {
    switchTab('jobs');
    if (jobId) {
      jobsCollection.getJob(jobId);
    } else {
      jobsCollection.getJobs();
    }
  });
  appRouter.on('route:executionsRoute', function(executionId) {
    switchTab('executions');
    if (executionId) {
      executionsCollection.getExecution(executionId);
    } else {
      executionsCollection.getExecutions();
    }
  });
  appRouter.on('route:filesRoute', function() {
    switchTab('files');
    filesCollection.getFiles();
  });
  appRouter.on('route:logsRoute', function() {
    switchTab('logs');
    logsCollection.getLogs();
  });
  appRouter.on('route:defaultRoute', function(actions) {
    // Anything else defaults to jobs view
    switchTab('jobs');
    jobsCollection.getJobs();
  });

  Backbone.history.start();
});
