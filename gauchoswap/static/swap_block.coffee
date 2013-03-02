(($) ->

  $('nav-tabs li').on('click', (e) ->
    $(@).tab('show')
  )

)(jQuery)
