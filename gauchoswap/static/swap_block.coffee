(($) ->

  $('nav-tabs li').on('click', (e) ->
    $(@).tab('show')
  )

)(jQuery)

(($) ->

  $('#department-list').on('change', (e) ->
    department = $('#department-list').val()
    $.getJSON($SCRIPT_ROOT + '/lecture/' + department + '/', (data) -> 
        console.log(data)
        )
  )

)(jQuery)
