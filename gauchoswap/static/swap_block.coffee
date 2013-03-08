(($) ->

  $class_type_button = $('.class_button')
  $department_list = $('.department-list')
  $add_course_button = $('.add-course')
  student_id = parseInt( $('.profile-title').data('studentId') )

  flash_message = (message) ->
    $flash = $("<div class='flash alert alert-success'><button type='button' class='close' data-dismiss='alert'>x</button><p>#{message}</p></div>")

    $('.navbar').after( $flash.fadeIn(2000) )
    console.log 'flashed'

  have_class = ->
    $('.swapblock-tab').eq(0).hasClass('active')

  $('.delete-course').on 'click', (e) ->
    $container = $(@).closest('.well')
    class_id = $container.data('classId')
    class_type = $.trim( $container.find('.class-badge').text().toLowerCase() )

    delete_class_params = JSON.stringify(class_type: class_type, class_id: class_id, have_class: have_class(), student_id: student_id)

    console.log delete_class_params

    $.post('/swapblock/drop', params: delete_class_params)
     .then ->
       flash_message('Class deleted successfully!')
       console.log 'deleted'
       $container.fadeOut('2000')


  $('nav-tabs li').on 'click', (e) ->
    $(@).tab('show')
    return

  $class_type_button.on 'click', (e) ->
    console.log 'reset modal'
    $class_options = $('#classes')
    $class_options.hide()
    $time_options = $('#times')
    $time_options.hide()
    $department_list.val('None')

  class_filter = {}
  filtered_courses = []
  class_type = ''
  $department_list.on 'change', (e) ->
    class_filter = {}
    filtered_courses = []
    class_type = ''
    console.log 'here'
    department = $(@).val()
    class_filter['department'] = department
    $class_type = $('.class_button.active')
    class_type = $class_type.val()

    if $class_type.length
      $.getJSON "/#{$class_type.val()}/#{department}/", (classes) ->
        console.log classes
        $class_options = $('#classes')
        $class_select = $class_options.find('.class-list')
        $time_options = $('#times')
        $time_select = $time_options.find('#inputTimes')
        $class_options.find('label').text "#{$class_type.val()}s:"
        teacher = ''

        switch $class_type.val()
          when 'lecture' then teacher = 'professor'
          when 'section' then teacher = 'ta'
          when 'lab' then teacher = 'instructor'
        
        $class_select.find('option').remove()
        $class_select.append $('<option />').val("None")
        for course in classes["#{$class_type.val()}s"]
          $class_select.append $('<option />').val(course.name).text("#{course.name}: #{course[teacher]}")

        $class_options.show()
    
        $class_options.unbind().bind 'change', (e) ->
          $time_options.hide()
          $time_select.find('option').remove()
          $time_select.append $('<option />').val("None")

          class_filter[teacher] = $(@).find(':selected').text().split(':')[1].trim()
          class_filter['name'] = $(@).find(':selected').val()
          console.log class_filter
          filtered_courses = _.where classes["#{$class_type.val()}s"], class_filter
          for course in filtered_courses
            console.log "IN HERE"
            $time_select.append $('<option />').val(course.time).text("#{course.days} at #{course.time}")
          $time_options.show()
        
        $time_options.on 'change', (e) ->
          class_filter['time'] = $(@).find(':selected').val()
          filtered_courses = _.where classes["#{$class_type.val()}s"], class_filter

          $('.add-course').removeClass('disabled')

          console.log class_filter
          console.log filtered_courses  


        return
    return
            
  $add_course_button.on 'click', (e) ->
    if $(@).hasClass('disabled')
      return

    selected_course = filtered_courses[0]
    add_class_params = JSON.stringify(class_type: class_type, class_id: selected_course.id, have_class: have_class(), student_id: student_id)

    class_filter = {}
    filtered_courses = []
    class_type = ''

    console.log add_class_params
    $.when( $.post('/swapblock/add', params: add_class_params) ).then ->
      console.log 'po'

    $('#myModal').modal('hide')

)(jQuery)
