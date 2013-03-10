(($) ->

  $accept_offer_button = $('.accept-offer')
  $decline_offer_button = $('.decline-offer')

  flash_message = (message) ->
    $flash = $("<div class='flash alert alert-success'><button type='button' class='close' data-dismiss='alert'>x</button><p>#{message}</p></div>")

    $('.navbar').after( $flash.fadeIn(2000) )
    console.log 'flashed'

  $accept_offer_button.on 'click', (e) ->
    if $(@).hasClass('disabled')
      return
    $container = $(@).closest('.well')
    offer_id = $container.data('offer-id')   
    console.log offer_id
    $.ajax 
      url: '/offer/accept', 
      data: {offer_id: offer_id},
      type: 'PUT',
      success: (e) -> 
        flash_message("Offer Accepted!")
        console.log e
    $(@).addClass('disabled')
    $container.find('.decline-offer').addClass('disabled')

  $decline_offer_button.on 'click', (e) ->
    if $(@).hasClass('disabled')
      return
    $container = $(@).closest('.well')
    offer_id = $container.data('offer-id')   
    $.ajax 
      url: '/offer/reject', 
      data: {offer_id: offer_id}
      type: 'PUT'
      success: (e) -> 
       flash_message("Offer Declined!")
       console.log e
    $(@).addClass('disabled')
    $container.find('.accept-offer').addClass('disabled')

       

)(jQuery)
