function next(document) {
    const selected = document.querySelector('input[name="type"]:checked').value;
    if (selected === 'web'){
        alert('Простите, но этот раздел пока не готов');
        return;
    }
    window.location.replace('upload.html');
}

function main(){
    window.location.replace('index.html');
}
