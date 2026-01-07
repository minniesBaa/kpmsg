var id;
const hash = window.location.hash;
let minutes = 0;
let seconds = 0;
let state = true;
let nowid = -1;
let supressReloads = false;
async function getid(){
    try {
        const res = await fetch("/api/id")
        if (!res.ok){
            return null
        }
        return res.text()
    } catch {
        return null
    }
}
async function checkID() {
    if (nowid == null) {
        location.reload(true)
    }
    nowid = await getid()
    if (!nowid) {
        document.body.innerHTML = "Unable to connect to server. Retrying..."
        nowid = null;
        return null;
    }
    if(nowid !== id && !supressReloads){
        location.reload(true);
    }
}

async function check(){
    if (document.visibilityState == "visible"){
        await checkID();
        minutes = 0;
        setTimeout(check, 1000)
        seconds = 0;
    } else {
        seconds++;
        if (minutes < 60 && seconds == 15){
            seconds = 0;
            await checkID();
            minutes += 0.25;
            setTimeout(check, 60000)
        } else {
            setTimeout(check, 1000)
        }
    }
}
function updatetextbox(){
    const inputbox = document.getElementById('post_text');
    const currentUrl = new URL(window.location.href);
    const urlParams = currentUrl.searchParams;
    urlParams.set('p', inputbox.value);
    history.replaceState(null, '', currentUrl.toString());
}
function savesig(){
    const sig = document.getElementById('signature');
    localStorage.setItem("sig", sig.value);
}
function preview(){
    const pre = document.getElementById('pre');
    const imgsel = document.getElementById('imgsel');
    pre.src = `/img/${imgsel.value}`;
    const currentUrl = new URL(window.location.href);
    const urlParams = currentUrl.searchParams;
    urlParams.set('e', imgsel.value);
    history.replaceState(null, '', currentUrl.toString());
}
function rint(m,x) {
  return Math.floor(Math.random()*(x-m+1))+m;
}
function onload(){
    if (localStorage.getItem("uid") == null){
        localStorage.setItem("uid", rint(1000,9999))
    }
    document.getElementById("num").value=localStorage.getItem("uid")
    const inputbox = document.getElementById('post_text');
    const sig = document.getElementById('signature');
    const imgsel = document.getElementById('imgsel');
    imgsel.addEventListener("change", preview)
    sig.value = localStorage.getItem("sig");
    inputbox.focus()
    getid()
        .then(nowid => {
            id = nowid;
        });
    inputbox.addEventListener('input', updatetextbox);
    sig.addEventListener('input', savesig);
    const fileInput = document.getElementById('imageFile');
    
    setTimeout(check, 1000);

    const initialUrl = new URL(window.location.href);
    const initialSearchParams = initialUrl.searchParams;
    if (initialSearchParams.has("p")) {
        inputbox.value = initialSearchParams.get("p");
        inputbox.selectionStart = inputbox.value.length;
        inputbox.selectionEnd = inputbox.value.length;
    }
    if (initialSearchParams.has("e")) {
        imgsel.value = initialSearchParams.get("e");
        preview()
    }
    fileInput.addEventListener('click', ()=>{
        supressReloads = true;
    });
    fileInput.addEventListener('cancel', ()=>{
        supressReloads = false;
    });
    fileInput.addEventListener('change', ()=>{
        upload();
    });
}

async function upload() {
    const fileInput = document.getElementById("imageFile")
    const file = fileInput.files[0];
    if (!file) {
        alert("kp doesn't see your file. maybe add one first?")
        return;
    }

    if (file.size > 5*1024*1024) {
        alert("that file is bigger than kp himself! pick one smaller than 5 megabytes.")
        return;
    }

    const formData = new FormData();
    formData.append('image', file);

    try {
        await fetch('/upload', {
            method: 'POST',
            body: formData,
        });
    } catch (error) {
        console.log(error)
    }
    supressReloads = false;
}

document.addEventListener('DOMContentLoaded', onload);