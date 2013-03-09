(($) ->

  $search_buttons = $('.search_buttons')
  $search_bar = $('.search_bar')

  $search_buttons.on 'click', (e) ->
    if $(@).text() == 'User'
       $('.search_class.active').button 'toggle'
    else
       $('#user-search.active').button 'toggle'
    

)(jQuery)
