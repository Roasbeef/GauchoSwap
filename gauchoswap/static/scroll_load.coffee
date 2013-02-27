#TODO:
## attach votes to new posts
(($) ->
  
  scrollLoad = ->
    page_num      = ($('.offer-stream >').length / 10) + 1
    console.log page_num
    $new_posts    = $('<div>')
    speed         = 3000
    url           = "/?page=#{page_num}"

    $new_posts.load "#{url} .offer-stream > ", () ->
      $new_posts.children().hide().appendTo('.offer-stream').fadeIn(speed)


  $(window).on 'scroll', () ->
    
    if $(@).scrollTop() == $(document).height() - $(@).height()
      if scrollTimeout
        clearTimeout(scrollTimeout)
                                                                     
      scrollTimeout = setTimeout(scrollLoad, 2000)
      console.log 'starting'

)(jQuery)
