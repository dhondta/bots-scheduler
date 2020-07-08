require.config({
  paths: {
    'jquery': 'vendor/jquery',
    'underscore': 'vendor/underscore',
    'backbone': 'vendor/backbone',
    'bootstrap': 'vendor/bootstrap',
    'bootstrapswitch': 'vendor/bootstrap-switch',
    'utils': 'utils',
    'config': 'config',
    'text': 'vendor/text',
    'edit-job-modal': 'templates/edit-job.html',
    'job-class-notes': 'templates/job-class-notes.html',
    'job-class-args': 'templates/job-class-args.html'
  },
  shim: {
    'bootstrapswitch': {
      deps: ['bootstrap']
    },
    'bootstrap': {
      deps: ['jquery']
    },
    'backbone': {
      deps: ['underscore', 'jquery'],
      exports: 'Backbone'
    }
  }
});

define(['utils', 'config', 'text!edit-job-modal', 'text!job-class-notes', 'text!job-class-args', 'backbone',
        'bootstrapswitch'], function(utils, config, EditJobModalHtml, JobClassNotesHtml, JobClassArgsHtml) {
  'use strict';
  var jobAnchor;
  return Backbone.View.extend({
    initialize: function() {
      $('body').append(EditJobModalHtml);
      this.bindEditJobConfirmClickEvent();
      this.bindDeleteJobConfirmClickEvent();
      this.bindModalPopupEvent();
    },
    bindDeleteJobConfirmClickEvent: function() {
      var $button = $('#delete-job-confirm-button');
      $button.off('click');
      $button.on('click', _.bind(function() {
        if (confirm('Really want to delete it?')) {
          var jobId = $('#edit-input-job-id').val();
          this.collection.deleteJob(jobId);
          $('#edit-job-modal').modal('hide');
        }
      }, this));
    },
    bindModalPopupEvent: function() {
      $('#edit-job-modal').on('show.bs.modal', _.bind(function(e) {
        var jobsMetaInfo = $.parseJSON($('#jobs-meta-info').html());
        var data = [];
        _.forEach(jobsMetaInfo, function(job) {
          data.push({
            id: job.job_class_string,
            text: job.job_class_name,
            job: job
          })
        });
        var $button = $(e.relatedTarget);
        jobAnchor = $button;
        var jobId = $button.data('id');
        var jobActive = $button.data('job-active');
        $('#edit-input-job-name').val($button.data('job-name'));
        $('#edit-input-job-month').val($button.data('job-month'));
        $('#edit-input-job-day-of-week').val($button.data('job-day-of-week'));
        $('#edit-input-job-day').val($button.data('job-day'));
        $('#edit-input-job-hour').val($button.data('job-hour'));
        $('#edit-input-job-minute').val($button.data('job-minute'));
        $('#edit-input-job-id').val(jobId);
        // get the job object matching the given class and populate notes and arguments
        var job = data.find(obj => { return obj.id === $button.data('job-task') });
        $('#edit-input-job-task-class').val(job.text);
        $('#edit-job-class-notes').html(_.template(JobClassNotesHtml)({
          job: job.job
        }));
        $('#edit-input-job-task-args').html(_.template(JobClassArgsHtml)({
          job: job.job,
          files: config.files_list,
          data: JSON.parse($button.attr('data-job-pubargs'))
        }));
        var $checkbox = $('<input>', {
          type: 'checkbox',
          name: 'pause-resume-checkbox',
          id: 'pause-resume-checkbox',
          checked: ''
        });
        $('#pause-resume-container').html($checkbox);
        $("[name='pause-resume-checkbox']").bootstrapSwitch({
          'onText': 'Active',
          'offText': 'Inactive',
          'state': (jobActive == 'yes'),
          'onSwitchChange': _.bind(function(event, state) {
            if (state) {
              this.collection.resumeJob(jobId);
            } else {
              this.collection.pauseJob(jobId);
            }
            $('#edit-job-modal').modal('hide');
          }, this)
        });
      }, this));
    },
    bindEditJobConfirmClickEvent: function() {
      var editConfirmButton = $('#edit-job-confirm-button').off('click');
      editConfirmButton.on('click', _.bind(function(e) {
        e.preventDefault();
        var jobId = $('#edit-input-job-id').val();
        var jobName = $('#edit-input-job-name').val();
        var jobTask = $('#edit-input-job-task-class').val();
        var month = $('#edit-input-job-month').val();
        var dayOfWeek = $('#edit-input-job-day-of-week').val();
        var day = $('#edit-input-job-day').val();
        var hour = $('#edit-input-job-hour').val();
        var minute = $('#edit-input-job-minute').val();
        var args = $('#edit-input-job-task-args').find(':input');
        if (jobName.trim() === '') {
          utils.alertError('Please fill in job name');
          return;
        }
        if (jobTask.trim() === '') {
          utils.alertError('Please fill in job task class');
          return;
        }
        // In order to pass space via command line arguments, we replace space
        // with $, and replace $ back to space. So, '$' is reserved and can't
        // be used in user input.
        if (jobName.indexOf('$') != -1 ||
            jobTask.indexOf('$') != -1) {
          utils.alertError('You cannot use "$". Please remove it.');
          return;
        }
        var taskArgs = [];
        if (args.length == 1 && args[0].attributes.argtype.value == "list") {
          try {
            taskArgs = utils.getTaskArgs(args[0].value);
          } catch (err) {
            utils.alertError('Invalid Arguments. Should be valid JSON string, e.g. [1, 2, "test"].');
            return;
          }
        } else {
          _.forEach(args, function(arg) {
            if (arg.attributes.argtype.value == "list") {
              try {
                arg.value = utils.getTaskArgs(arg.value);
              } catch (err) {
                utils.alertError('Invalid Arguments. Should be valid JSON string, e.g. [1, 2, "test"].');
                return;
              }
            } else if (arg.attributes.argtype.value == "bool") {
              arg.value = arg.is(":checked");
            } else if (arg.attributes.argtype.value == "range") {
              arg.value = parseInt(arg.value, 10);
            }
            taskArgs.push(arg.value);
          });
        }
        // TODO (wenbin): more checking for cron string
        this.collection.modifyJob(jobId, {
          job_class_string: jobTask,
          name: jobName,
          pub_args: taskArgs,
          month: month,
          day_of_week: dayOfWeek,
          day: day,
          hour: hour,
          minute: minute
        });
        jobAnchor.attr('title', jobTask+"("+JSON.stringify(taskArgs)+")");
        jobAnchor.attr('data-job-name', jobName);
        jobAnchor.attr('data-job-pubargs', JSON.stringify(taskArgs));
        $('#edit-job-modal').modal('hide');
        this.collection.trigger('reset');
      }, this));
    }
  });
});
