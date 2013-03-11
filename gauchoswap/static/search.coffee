(($) ->

  $search_buttons = $('.search_buttons')
  $search_bar = $('.search-bar')
  
  $.fn.typeahead.Constructor::blur = ->
    that = this
    setTimeout (->
      that.hide()
    ), 250
  
  
  students = {}
  lectures = {}
  sections = {}
  labs = {}
  $search_buttons.on 'click', (e) ->
    if $(@).text() == 'User'
       $('.search_class.active').button 'toggle'
       $('.search-bar').typeahead(
         source: (query, process) ->
           $.getJSON('/search/student', (data) ->
             console.log data
             students = data
             results = _.map(data, (student) -> "#{student.name}")
             console.log results
             console.log students
             process results
             return
           )
         highlighter: (name) ->
           "#{name}"
         updater: (name) ->
           student = _.where students, name: name
           location.href = "/student/#{student[0].id}"
           name
       )
       return
    else
       $('#user-search.active').button 'toggle'
       if $(@).text() == 'Lecture'
         $('.search-bar').typeahead(
           source: (query, process) ->
             $.getJSON("/search/lecture?q=#{query}", (data) ->
               console.log data
               lectures = data

               results = _.map(data, (lecture) -> "#{lecture.name}")

               console.log results
               process results
             )
           highlighter: (text) ->
             lecture = _.where lectures, {name: text}
             "#{lecture[0].name}"
           updater: (text) ->
             lecture = _.where lectures, {name: text}
             "#{lecture[0].name}"
         )

    return
    

)(jQuery)
