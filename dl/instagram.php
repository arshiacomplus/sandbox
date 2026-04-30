
<html>

<head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>

<body>
<p><code>aria2/1.37.0</code></p>
    <p>Copy below link and send to @UploadBot</p>

    <textarea id="uploadbot"></textarea>
    <button id="copyButton">Click here to copy</button>
</body>
<script>
document.getElementById("copyButton").addEventListener("click", function() {
    alert('Download link copied');
    copyToClipboard(document.getElementById("uploadbot"));
});

function copyToClipboard(elem) {
	  // create hidden text element, if it doesn't already exist
    var targetId = "_hiddenCopyText_";
    var isInput = elem.tagName === "INPUT" || elem.tagName === "TEXTAREA";
    var origSelectionStart, origSelectionEnd;
    if (isInput) {
        // can just use the original source element for the selection and copy
        target = elem;
        origSelectionStart = elem.selectionStart;
        origSelectionEnd = elem.selectionEnd;
    } else {
        // must use a temporary form element for the selection and copy
        target = document.getElementById(targetId);
        if (!target) {
            var target = document.createElement("textarea");
            target.style.position = "absolute";
            target.style.left = "-9999px";
            target.style.top = "0";
            target.id = targetId;
            document.body.appendChild(target);
        }
        target.textContent = elem.textContent;
    }
    // select the content
    var currentFocus = document.activeElement;
    target.focus();
    target.setSelectionRange(0, target.value.length);
    
    // copy the selection
    var succeed;
    try {
    	  succeed = document.execCommand("copy");
    } catch(e) {
        succeed = false;
    }
    // restore original focus
    if (currentFocus && typeof currentFocus.focus === "function") {
        currentFocus.focus();
    }
    
    if (isInput) {
        // restore prior selection
        elem.setSelectionRange(origSelectionStart, origSelectionEnd);
    } else {
        // clear temporary content
        target.textContent = "";
    }
    return succeed;
}
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            data = this.responseText;
            try {
                data = JSON.parse(data)
                let url = null
                if (data.graphql.shortcode_media.is_video === true) {
                    url = data.graphql.shortcode_media.video_url
                } else {
                    url = data.graphql.shortcode_media.display_url

                }
                document.getElementById("uploadbot").value = url;
                var copyText = document.getElementById("uploadbot");
                copyText.select();
                copyText.setSelectionRange(0, 99999)
                document.execCommand("copy");


            } catch (e) {
                console.log(e)
                document.getElementById("uploadbot").value = JSON.stringify(e);
                alert('something went wrong' + e.type)
                

            }


        }
    };
    xhttp.open("GET", "https://www.instagram.com/reel/DGvL5YFqxHH/?__a=1", true);
    xhttp.send();
</script>

</html>