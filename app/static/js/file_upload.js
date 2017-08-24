var dropZone = document.getElementById('drop-zone');
var uploadForm = document.getElementById('js-upload-form');
var progrssBar = document.getElementById('progress-bar');

var alertBox = $('#alert-box');
var alertMsg = $('#alert-msg');
var challenge = $('#challenge')
var challengeBox = $('#challenge-box');

challenge.on("input", function(){
    if (challenge.val() == "") {
        challengeBox.addClass("has-error")
    } else {
        console.log("asd")
        challengeBox.removeClass("has-error")
    }
})

if (typeof(window.FileReader) == 'undefined') {
    dropZone.innerHTML = "Not supported browser"
}

function uploadProgress(event) {
    var percent = parseInt(event.loaded / event.total * 100);
    progrssBar.style.width = percent + "%"
}

function showError(msg) {
    alertMsg.html(msg);
    alertBox.removeClass("alert-success")
    alertBox.addClass("alert-danger")
    alertBox.show()
}

function showOK(msg) {
    alertMsg.html(msg);
    alertBox.removeClass("alert-danger")
    alertBox.addClass("alert-success")
    alertBox.show()
}

function stateChange(event) {
    if (event.target.readyState == 4) if (event.target.status == 200) {
        var ans = JSON.parse(event.target.responseText);
        if (ans.hasOwnProperty('Error')) {
            if (ans.hasOwnProperty('Challenge')) {
                challenge.text(ans['Challenge'])
            }
            showError(ans['Error'])
        } else {
           showOK(ans['Body'])
        }
    } else {
        showError("Unknown error happened!");
    }
}

// Upload file using HTML5
var startUpload = function (files) {
    var formData = new FormData();

    var challText = challenge.val()
    if (challText == '') {
        challengeBox.addClass("has-error")
        showError("Challenge answer is not provided!");
        return
    }
    formData.append("challenge", challText)

    var file = files[0];
    formData.append("file", file);

    var xhr = new XMLHttpRequest();
    xhr.upload.addEventListener('progress', uploadProgress, false);
    xhr.onreadystatechange = stateChange;
    xhr.open('POST', '/api/upload');
    xhr.setRequestHeader('X-FILE-NAME', file.name);
    xhr.send(formData);
};


uploadForm.addEventListener('submit', function (e) {
    if (typeof(window.FileReader) != 'undefined') {
        e.preventDefault();
        var uploadFiles = document.getElementById('js-upload-files').files;
        startUpload(uploadFiles)
    }
});


dropZone.ondrop = function (e) {
    e.preventDefault();
    this.className = 'upload-drop-zone';

    if (typeof(window.FileReader) == 'undefined') {
        return
    }
    startUpload(e.dataTransfer.files)
};

dropZone.ondragover = function () {
    this.className = 'upload-drop-zone drop';
    return false;
};

dropZone.ondragleave = function () {
    this.className = 'upload-drop-zone';
    return false;
};