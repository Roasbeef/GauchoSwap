(($) ->

  $class_type_button = $('.class_button')
  $department_list = $('.department-list')
  $add_course_button = $('.add-course')
  $offer_course_button = $('.verify-offer-course')
  student_id = parseInt( $('.profile-title').data('student-id') )
  my_id = parseInt( $('.profile-title').data('my-id') )

  flash_message = (message) ->
    $flash = $("<div class='flash alert alert-success'><button type='button' class='close' data-dismiss='alert'>x</button><p>#{message}</p></div>")

    $('.navbar').after( $flash.fadeIn(2000) )
    console.log 'flashed'

  have_class = ->
    $('.swapblock-tab').eq(0).hasClass('active')

  reset_add_modal = ->
    console.log 'reset modal'
    $class_options = $('#classes')
    $class_options.hide()
    $time_options = $('#times')
    $time_options.hide()
    $department_list.val('None')
    $('.add-course').addClass('disabled')
    $offer_course_button.addClass('disabled')
    

  attach_delete_button_events = ->
    $('.delete-course').off 'click'
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

  class_offering_for = {}
  $('.offer-course').on 'click', (e) ->
    console.log student_id
    $container = $(@).closest('.well')
    class_id = $container.data('classId')
    class_type = $.trim( $container.find('.class-badge').text().toLowerCase() )

    class_offering_for['class_type'] = class_type
    class_offering_for['class_id'] = class_id
    console.log class_offering_for['class_type']

  $('nav-tabs li').on 'click', (e) ->
    $(@).tab('show')
    return

  $class_type_button.on 'click', (e) ->
    console.log my_id
    reset_add_modal()

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
          $offer_course_button.removeClass('disabled')

          console.log class_filter
          console.log filtered_courses  


        return
    return
            
  $add_course_button.on 'click', (e) ->
    if $(@).hasClass('disabled')
      return

    selected_course = filtered_courses[0]
    add_class_params = JSON.stringify(class_type: class_type, class_id: selected_course.id, have_class: have_class(), student_id: student_id)

    console.log add_class_params
    $.post('/swapblock/add', params: add_class_params, (data) ->
      $('#myModal').modal('hide')
      flash_message('Class added to Swapblock!')

      class_filter = {}
      filtered_courses = []
      class_type = ''
      $('#invisible_button').button 'toggle'
      reset_add_modal()

      $new_class = $( $.trim("#{data.class_html}") )
      $('.swapblock-body').append( $new_class.fadeIn(2000) )
      attach_delete_button_events()
    )


  $offer_course_button.on 'click', (e) ->
    if $(@).hasClass('disabled')
      return

    selected_course = filtered_courses[0]
    offer_class_params = JSON.stringify(offerer_class_id: selected_course.id, offeree_class_id: class_offering_for['class_id'], offer_type: class_offering_for['class_type'], offeree_id: student_id, offerer_id: my_id)

    console.log offer_class_params
    $.when(
      $.when( $.post('/offer/', params: offer_class_params) ).then ->
        console.log 'offered'
      
      $.when( $('#myModal').modal('hide') ).then ->
        flash_message('Offer Placed!')
    ).then ->
      $class_clone = $('.user-class').eq(0).clone(true)
      console.log 'all donz'
      console.log $class_clone

    class_filter = {}
    filtered_courses = []
    class_type = ''
    class_offering_for = {}
    $('#invisible_button').button 'toggle'
    reset_add_modal()

  attach_delete_button_events()

)(jQuery)
