(($) ->

  $('nav-tabs li').on('click', (e) ->
    $(@).siblings().removeClass('active')
    $(@).addClass('active')
  )

)(jQuery)
