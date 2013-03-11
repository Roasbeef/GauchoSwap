// Generated by CoffeeScript 1.4.0
(function() {

  (function($) {
    var $add_course_button, $class_type_button, $department_list, $offer_course_button, attach_delete_button_events, class_filter, class_offering_for, class_type, filtered_courses, flash_message, have_class, my_id, reset_add_modal, student_id;
    $class_type_button = $('.class_button');
    $department_list = $('.department-list');
    $add_course_button = $('.add-course');
    $offer_course_button = $('.verify-offer-course');
    student_id = parseInt($('.profile-title').data('student-id'));
    my_id = parseInt($('.profile-title').data('my-id'));
    flash_message = function(message) {
      var $flash;
      $flash = $("<div class='flash alert alert-success'><button type='button' class='close' data-dismiss='alert'>x</button><p>" + message + "</p></div>");
      $('.navbar').after($flash.fadeIn(2000));
      return console.log('flashed');
    };
    have_class = function() {
      return $('.swapblock-tab').eq(0).hasClass('active');
    };
    reset_add_modal = function() {
      var $class_options, $time_options;
      console.log('reset modal');
      $class_options = $('#classes');
      $class_options.hide();
      $time_options = $('#times');
      $time_options.hide();
      $department_list.val('None');
      $('.add-course').addClass('disabled');
      return $offer_course_button.addClass('disabled');
    };
    attach_delete_button_events = function() {
      $('.delete-course').off('click');
      return $('.delete-course').on('click', function(e) {
        var $container, class_id, class_type, delete_class_params;
        $container = $(this).closest('.user-class');
        class_id = $container.data('classId');
        class_type = $.trim($container.find('.class-badge').text().toLowerCase());
        delete_class_params = JSON.stringify({
          class_type: class_type,
          class_id: class_id,
          have_class: have_class(),
          student_id: student_id
        });
        console.log(delete_class_params);
        return $.post('/swapblock/drop', {
          params: delete_class_params
        }).then(function() {
          flash_message('Class deleted successfully!');
          console.log('deleted');
          return $container.fadeOut('2000');
        });
      });
    };
    class_offering_for = {};
    $('.offer-course').on('click', function(e) {
      var $container, class_id, class_type;
      console.log(student_id);
      $container = $(this).closest('.user-class');
      class_id = $container.data('classId');
      class_type = $.trim($container.find('.class-badge').text().toLowerCase());
      class_offering_for['class_type'] = class_type;
      class_offering_for['class_id'] = class_id;
      return console.log(class_offering_for['class_type']);
    });
    $('nav-tabs li').on('click', function(e) {
      $(this).tab('show');
    });
    $class_type_button.on('click', function(e) {
      console.log(my_id);
      return reset_add_modal();
    });
    class_filter = {};
    filtered_courses = [];
    class_type = '';
    $department_list.on('change', function(e) {
      var $class_type, department;
      class_filter = {};
      filtered_courses = [];
      class_type = '';
      console.log('here');
      department = $(this).val();
      class_filter['department'] = department;
      $class_type = $('.class_button.active');
      class_type = $class_type.val();
      if ($class_type.length) {
        $.getJSON("/" + ($class_type.val()) + "/" + department + "/", function(classes) {
          var $class_options, $class_select, $time_options, $time_select, course, teacher, _i, _len, _ref;
          console.log(classes);
          $class_options = $('#classes');
          $class_select = $class_options.find('.class-list');
          $time_options = $('#times');
          $time_select = $time_options.find('#inputTimes');
          $class_options.find('label').text("" + ($class_type.val()) + "s:");
          teacher = '';
          switch ($class_type.val()) {
            case 'lecture':
              teacher = 'professor';
              break;
            case 'section':
              teacher = 'ta';
              break;
            case 'lab':
              teacher = 'instructor';
          }
          $class_select.find('option').remove();
          $class_select.append($('<option />').val("None"));
          _ref = classes["" + ($class_type.val()) + "s"];
          for (_i = 0, _len = _ref.length; _i < _len; _i++) {
            course = _ref[_i];
            $class_select.append($('<option />').val(course.name).text("" + course.name + ": " + course[teacher]));
          }
          $class_options.show();
          $class_options.unbind().bind('change', function(e) {
            var _j, _len1;
            $time_options.hide();
            $time_select.find('option').remove();
            $time_select.append($('<option />').val("None"));
            class_filter[teacher] = $(this).find(':selected').text().split(':')[1].trim();
            class_filter['name'] = $(this).find(':selected').val();
            console.log(class_filter);
            filtered_courses = _.where(classes["" + ($class_type.val()) + "s"], class_filter);
            for (_j = 0, _len1 = filtered_courses.length; _j < _len1; _j++) {
              course = filtered_courses[_j];
              console.log("IN HERE");
              $time_select.append($('<option />').val(course.time).text("" + course.days + " at " + course.time));
            }
            return $time_options.show();
          });
          $time_options.on('change', function(e) {
            class_filter['time'] = $(this).find(':selected').val();
            filtered_courses = _.where(classes["" + ($class_type.val()) + "s"], class_filter);
            $('.add-course').removeClass('disabled');
            $offer_course_button.removeClass('disabled');
            console.log(class_filter);
            return console.log(filtered_courses);
          });
        });
      }
    });
    $add_course_button.on('click', function(e) {
      var add_class_params, selected_course;
      if ($(this).hasClass('disabled')) {
        return;
      }
      selected_course = filtered_courses[0];
      add_class_params = JSON.stringify({
        class_type: class_type,
        class_id: selected_course.id,
        have_class: have_class(),
        student_id: student_id
      });
      console.log(add_class_params);
      return $.post('/swapblock/add', {
        params: add_class_params
      }, function(data) {
        var $new_class;
        $('#myModal').modal('hide');
        flash_message('Class added to Swapblock!');
        class_filter = {};
        filtered_courses = [];
        class_type = '';
        $('#invisible_button').button('toggle');
        reset_add_modal();
        $new_class = $($.trim("" + data.class_html));
        $('.tab-pane.active').append($new_class.fadeIn(2000));
        return attach_delete_button_events();
      });
    });
    $offer_course_button.on('click', function(e) {
      var offer_class_params, selected_course;
      if ($(this).hasClass('disabled')) {
        return;
      }
      selected_course = filtered_courses[0];
      offer_class_params = JSON.stringify({
        offerer_class_id: selected_course.id,
        offeree_class_id: class_offering_for['class_id'],
        offer_type: class_offering_for['class_type'],
        offeree_id: student_id,
        offerer_id: my_id
      });
      console.log(offer_class_params);
      $.when($.when($.post('/offer/', {
        params: offer_class_params
      })).then(function() {
        return console.log('offered');
      }), $.when($('#myModal').modal('hide')).then(function() {
        return flash_message('Offer Placed!');
      })).then(function() {
        var $class_clone;
        $class_clone = $('.user-class').eq(0).clone(true);
        console.log('all donz');
        return console.log($class_clone);
      });
      class_filter = {};
      filtered_courses = [];
      class_type = '';
      class_offering_for = {};
      $('#invisible_button').button('toggle');
      return reset_add_modal();
    });
    return attach_delete_button_events();
  })(jQuery);

}).call(this);
