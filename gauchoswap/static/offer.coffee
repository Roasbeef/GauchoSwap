(($) ->

  $accept_offer_button = $('.accept-offer')
  $decline_offer_button = $('.decline-offer')

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
       console.log e

       

)(jQuery)
