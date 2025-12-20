var id;
const hash = window.location.hash;
function getid(){
    return fetch("/api/id")
        .then(response =>{
            if(response.ok){
                return response.text();
            }
        });
}
async function check(){
    let nowid;
    nowid = await getid()
    if(nowid !== id){
        location.reload(true);
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
function updatefavicon(){
    var link = document.querySelector("link[rel~='icon']");
    if (!link) {
        link = document.createElement('link');
        link.rel = 'icon';
        document.head.appendChild(link);
}
link.href = `/noalerticon.ico?force-no-cache=${Math.round(Math.random() * 10000)}`;
}
function rint(m,x) {
  return Math.floor(Math.random()*(x-m+1))+m;
}
setTimeout(updatefavicon, 1000);
function onload(){
    //darkmode testing
    //dbody = document.body
    //dbody.classList.toggle("dark");
    //dhead = document.head
    //dhead.classList.toggle("dark");
    //
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
            //if(id === "0"){
            //    const doc = document.body;
            //    doc.innerHTML += '<div style="background-color: lightgray; color: white; padding: 5px; border: 2px darkgray; text-align: center; font-family: sans-serif; font-size: 24px;">kp\'s message board just restarted!</div>'
            //}
        });
    inputbox.addEventListener('input', updatetextbox);
    sig.addEventListener('input', savesig);
    const fileInput = document.getElementById('imageFile');
    
    setInterval(check, 1000);
    // if(hash === "#0"){
    // const doc = document.body;
    // doc.innerHTML += '<div style="background-color: lightgray; color: white; padding: 5px; border: 2px solid red; text-align: center; font-family: sans-serif; font-size: 24px;">Put some text in the box before posting!</div>'
    // }
    // if(hash === "#long"){
    // const doc = document.body;
    // doc.innerHTML += '<div style="background-color: lightgray; color: white; padding: 5px; border: 2px solid red; text-align: center; font-family: sans-serif; font-size: 24px;">Your message was too long, so it has not been posted. Try to keep messages less than 100 characters!</div>'
    // }
    // if(hash === "#long2"){
    // const doc = document.body;
    // doc.innerHTML += '<div style="background-color: lightgray; color: white; padding: 5px; border: 2px solid red; text-align: center; font-family: sans-serif; font-size: 24px;">Your signature is too long. Make sure it\'s less than 40 characters!</div>'
    // }
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
        const uploadButton = document.getElementById('upload');
        const restoredImage = document.getElementById('restoredImage');
        uploadButton.addEventListener('click', async () => {
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
                const response = await fetch('/upload', {
                    method: 'POST',
                    body: formData,
                });

                restoredImage.src = `/latest?t=${new Date().getTime()}`;
            } catch (error) {
                console.log(error)
            }
        });
}

document.addEventListener('DOMContentLoaded', onload);