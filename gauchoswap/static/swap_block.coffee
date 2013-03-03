(($) ->

  $('nav-tabs li').on('click', (e) ->
    $(@).tab('show')
  )

)(jQuery)

(($) ->

  $('#department-list').on('change', (e) ->
    department = $('#department-list').val()
    class_type = $('.class_button.active').val() 
    class_type_index = class_type + 's'
    if class_type == 'lecture' or class_type == 'section' or class_type == 'lab'
        $.getJSON($SCRIPT_ROOT + '/' + class_type + '/' + department + '/', (data) -> 
            $('#class-list').empty()
            for cl in data[class_type_index]
                class_list = document.getElementById('class-list')
                option = document.createElement('option')
                option.text = cl.name + ' ' + cl.title
                option.value = cl.name
                try
                    class_list.add(option, null)
                catch error
                    class_list.add(option)
            )
    else
        alert("Choose Class Type First")
        document.getElementById('department-list').selectedIndex = 0
    
  )

)(jQuery)

(($) ->

  $('.class_button').on('click', (e) ->
    document.getElementById('department-list').selectedIndex = 0
    $('#class-list').empty()
  )

)(jQuery)

(($) ->

  $('.modal-button').on('click', (e) ->
    document.getElementById('department-list').selectedIndex = 0
    $('#class-list').empty()
  )

)(jQuery)


