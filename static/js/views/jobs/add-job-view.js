require.config({
  paths: {
    'jquery': 'vendor/jquery',
    'underscore': 'vendor/underscore',
    'backbone': 'vendor/backbone',
    'bootstrap': 'vendor/bootstrap',
    'select2': 'vendor/select2',
    'utils': 'utils',
    'config': 'config',
    'text': 'vendor/text',
    'add-job-modal': 'templates/add-job.html',
    'job-class-notes': 'templates/job-class-notes.html',
    'job-class-args': 'templates/job-class-args.html'
  },
  shim: {
    'bootstrap': {
      deps: ['jquery']
    },
    'select2': {
      deps: ['jquery']
    },
    'backbone': {
      deps: ['underscore', 'jquery'],
      exports: 'Backbone'
    }
  }
});

define(['utils', 'config', 'text!add-job-modal', 'text!job-class-notes', 'text!job-class-args', 'backbone', 'bootstrap',
        'select2'], function(utils, config, AddJobModalHtml, JobClassNotesHtml, JobClassArgsHtml) {
  'use strict';
  return Backbone.View.extend({
    initialize: function() {
      $('body').append(AddJobModalHtml);
      this.bindAddJobConfirmClickEvent();
      var jobsMetaInfo = $.parseJSON($('#jobs-meta-info').html());
      var data = [];
      _.forEach(jobsMetaInfo, function(job) {
        data.push({
          id: job.job_class_string,
          text: job.job_class_name,
          job: job
        })
      });
      $('#add-job-button').on('click', _.bind(function(e) {
        // reset modal elements
        $('#input-job-task-class').select2({
          placeholder: "Please select a job",
          data: data
        });
        $("#input-job-name").val("");
        $("#input-job-task-class").select2("val", "");
        $('#input-job-task-args').html("Please select a job class first");
        $('#add-job-class-notes').html("");
      }, this));
      $('#input-job-task-class').select2({
        placeholder: "Please select a job",
        data: data
      }).on("select2-selecting", function(e) {
        $('#add-job-class-notes').html(_.template(JobClassNotesHtml)({
          job: e.choice.job
        }));
        $('#input-job-task-args').html(_.template(JobClassArgsHtml)({
          job: e.choice.job,
          files: config.files_list,
          data: []
        }));
      });
    },
    bindAddJobConfirmClickEvent: function() {
      $('#add-job-confirm-button').on('click', _.bind(function(e) {
        e.preventDefault();
        var jobName = $('#input-job-name').val();
        var jobTask = $('#input-job-task-class').val();
        var month = $('#input-job-month').val();
        var dayOfWeek = $('#input-job-day-of-week').val();
        var day = $('#input-job-day').val();
        var hour = $('#input-job-hour').val();
        var minute = $('#input-job-minute').val();
        var args = $('#input-job-task-args').find(':input');
        if (!$.trim(jobName)) {
          utils.alertError('Please fill in job name');
          return;
        }
        if (!$.trim(jobTask)) {
          utils.alertError('Please fill in job task class');
          return;
        }
        // In order to pass space via command line arguments, we replace space
        // with $, and replace $ back to space. So, '$' is reserved and can't
        // be used in user input.
        if (jobName.indexOf('$') != -1 || jobTask.indexOf('$') != -1) {
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
          var error = false;
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
            if (!$.trim(arg.value)) {
              var descr = arg.attributes.placeholder.value;
              utils.alertError('Please fill in a '+descr[0].toLowerCase()+descr.slice(1));
              error = true;
            }
            taskArgs.push(arg.value);
          });
        }
        if (error) return;
        this.collection.addJob({
          job_class_string: jobTask,
          name: jobName,
          pub_args: taskArgs,
          month: month,
          day_of_week: dayOfWeek,
          day: day,
          hour: hour,
          minute: minute
        });
        $('#add-job-modal').modal('hide');
      }, this));
    }
  });
});
