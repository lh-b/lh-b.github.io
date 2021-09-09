/* ==========================================================================
   jQuery plugin settings and other scripts
   ========================================================================== */

$(document).ready(function () {
  // Image popups
  $('.page__content img').wrap(function () {

    $(this).magnificPopup({
      delegate: 'a',
      type: 'image',
      removalDelay: 250, //delay removal by X to allow out-animation
      callbacks: {
        beforeOpen: function () {
          // just a hack that adds mfp-anim class to markup 
          this.st.image.markup = this.st.image.markup.replace('mfp-figure', 'mfp-figure mfp-with-anim');
          this.st.mainClass = this.st.el.attr('data-effect');
        }
      },
    });

    return '<a href="' + $(this).attr('src') + '" style="width:' + $(this).attr('width') + 'px;"><figure> </figure>' + '<figcaption style="text-align: center;" class="caption">' + $(this).attr('alt') + '</figcaption>' + '</a>';
  });

});