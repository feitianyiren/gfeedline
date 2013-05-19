function append(text, is_append, is_scroll_paused, margin) {
    var parent = document.getElementById("messages");
    var entry = document.createElement("div");
    entry.innerHTML = text;

    if (is_append) {
        parent.appendChild(entry);
    } 
    else { // is_prepend
        parent.insertBefore(entry, parent.childNodes[0]);

        if (is_scroll_paused) {
            if (typeof margin === 'undefined') margin = 0;
            var body = $('body');
            body.scrollTop(body.scrollTop() + $(entry).height() + margin); 
        }
        else {
            $(entry).hide().slideDown(300);
        }
    }
}

function insertReplyed(text, entry_id) {
         var entry = document.createElement("div");
         entry.innerHTML = text;

//         $('#' + entry_id).css("background", "red");
         $('#' + entry_id  + ' .child').append(entry);
}

function scrollToBottom(is_bottom) {
    var target = is_bottom ? '#end' : '#top';
    scrollsmoothly.setScroll(target);
}

function jumpToBottom(is_bottom) {
    var target = is_bottom ? document.height : 0;
    window.scrollTo(0, target);
}

function changeCSS(id, css) {
    document.getElementById(id).href = css
}

function clearBuffer() {
    document.getElementById("messages").innerHTML = ""
}

function changeFont(font) {
     $('body').css("font", font);
}
