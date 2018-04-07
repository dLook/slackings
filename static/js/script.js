$(document).ready(function () {

    function emojify() {
        var emojiCodes = $('.emoji-code'),
            img;
        emojiCodes.each(function () {
            img = emojione.toImage($(this).html());
            if ( img.startsWith(':') ) {
                img = handleUnknown(img);
            }
            $(img).addClass('emoji-custom');
            $(this).replaceWith(img);
        });

        function handleUnknown(emojiCode) {
            return '<img class="emojione" alt="unknown" ' +
                'title="' + emojiCode + '" src="/static/img/emojis/question-sign.png"/>'
        }
    }

    function getUserInfo() {
        var elements = $('.js_getUserInfo');
        elements.each(function () {
            var slackUserId = $(this).data('slack-id');
            // console.log(slackUserId);
        });

    }

    emojify();
    getUserInfo();
});
