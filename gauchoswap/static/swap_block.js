// Generated by CoffeeScript 1.4.0
(function() {

  (function($) {
    return $('nav-tabs li').on('click', function(e) {
      $(this).siblings().removeClass('active');
      return $(this).addClass('active');
    });
  })(jQuery);

}).call(this);
