$(document).ready(function() {
    $('.page__content img').wrap( function(){
        $(this).magnificPopup({
            type: 'image',
            closeOnContentClick: true,
            showCloseBtn: false,
            items: {
              src: $(this).attr('src')
            },
        });
        $(this).parent('p').css('overflow', 'auto');
        return (
            `<a href="${$(this).attr('src')}">
                <figure></figure>
                <figcaption style="text-align: center;" class="caption">
                    ${$(this).attr('alt')}
                </figcaption>
            </a>`
        );
    });
});