/**
 * Configurations / constants
 *
 */

define([], function() {

  'use strict';

  var urlPrefix = '/api/v1';

  return {
    'jobs_url': urlPrefix + '/jobs',
    'executions_url': urlPrefix + '/executions',
    'files_url': urlPrefix + '/files',
    'logs_url': urlPrefix + '/logs'
  };
});
