#TODO:
## attach votes to new posts
(($) ->
  
  scrollLoad = () ->
    return if not $('.page_info').length

    page_num = $('.page_info').data('page')
    console.log page_num
    $('.page_info').remove()

    $new_posts    = $('<div>')
    speed         = 2000
    url           = "/?page=#{page_num+1}"

    $new_posts.load "#{url} .offer-stream > ", () ->
      $loading_gif.detach()
      $new_posts.children().hide().appendTo('.offer-stream').fadeIn(speed)


  $loading_gif = $("<img src='static/ajax-loader.gif' /> Grabbing more stuff....")
  $(window).on 'scroll', () ->
    
    if $(@).scrollTop() == $(document).height() - $(@).height()
      if scrollTimeout
        clearTimeout(scrollTimeout)
                                                                     
      $loading_gif.appendTo('.offer-stream')
      scrollTimeout = setTimeout(scrollLoad, 500)
      console.log 'starting'

)(jQuery)
