(($) ->

  $search_buttons = $('.search_buttons')
  $search_bar = $('.search-bar')
  
  $.fn.typeahead.Constructor::blur = ->
    that = this
    setTimeout (->
      that.hide()
    ), 250
  
  
  $search_buttons.on 'click', (e) ->
    if $(@).text() == 'User'
       $('.search_class.active').button 'toggle'
       $('.search-bar').typeahead(
         source: (query, process) ->
           $.getJSON('/search/student', (data) ->
             console.log data
             process data
             return
           )
           return
       )
       return
    else
       $('#user-search.active').button 'toggle'
       return
    return
    

)(jQuery)
