$(document).ready(function($) {
    if (typeof flask_pagedown_converter === "undefined") {
        flask_pagedown_converter = Markdown.getSanitizingConverter().makeHtml;
        mark_down = flask_pagedown_converter($("#text_content").val());
        $("#pagedown-preview").html(mark_down);
    }

    $("#text_content").keyup(function() {
        mark_down = flask_pagedown_converter(this.value);
        $("#pagedown-preview").html(mark_down);
    });
});