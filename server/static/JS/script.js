function next(document) {
    const selected = document.querySelector('input[name="type"]:checked').value;
    if (selected === 'web')  window.location.replace('web.html');
    else window.location.replace('upload.html');
}

function main(){
    window.location.replace('index.html');
}

let mediaRecorder, timerID, startTime;

function web_cam(document){
    const URL = 'http://localhost:8080/upload_web';
    const camVideo = document.getElementById('web-cam');

    navigator.mediaDevices.getUserMedia({ audio: true, video: true})
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            window.stream = stream;
            camVideo.srcObject = stream;

            let audioChunks = [];
            mediaRecorder.addEventListener("dataavailable",function(event) {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener("stop", function() {
                const audioBlob = new Blob(audioChunks, {
                    type: "video/webm"
                });

                let fd = new FormData();
                fd.append('voice', audioBlob);
                sendVoice(fd);
                audioChunks = [];
            });
        });

    async function sendVoice(form) {
        let promise = await fetch(URL, {
            method: 'POST',
            body: form});
        if (promise.ok) {
            let response = (await promise.text()).toString();
            if (response === '-') alert("Не удалось записать видео");
            else window.location.replace('upload?face=' + response);
        }
    }
}

function delta(){
    const d = Math.floor((new Date().getTime() - startTime) / 1000);
    if (d < 10) return "0" + d;
    return d
}

function update(out){
    out.textContent = 'Запись идёт 00:' + delta();
}

function web_cam_click(document){
    const button = document.getElementById('start-stop');
    const out = document.getElementById('out');

    if (button.textContent === 'Начать запись'){
        startTime = new Date().getTime();
        button.textContent = 'Останосить запись';
        mediaRecorder.start();
        timerID = setInterval(update, 1000, out);
        out.textContent = 'Запись идёт 00:00';
    } else {
        button.textContent = 'Начать запись';
        mediaRecorder.stop();
        clearInterval(timerID);
        out.textContent = 'Запись длилась 00:' + delta();
    }
}
