dark_css = '<style>.dark {background-color: #262626;color: white;}</style>'
def drawing(dark):
    page = f"<head>{dark_css if dark else ''}"
    page += """
<title>kp drawing | for doing all your drawing things</title>
    <link rel="icon" href="/noalerticon.ico" type="image/x-icon">
    <script>
        let draw = false
        let canvas;
        let ctx;
        function updateColor(){
            const picker = document.getElementById("colorPicker");
            const label = document.getElementById("pickerLabel");
            label.textContent = picker.value;
            ctx.strokeStyle = picker.value
        }
        function updateSize(){
            const slide = document.getElementById("penSlider");
            const label = document.getElementById("sliderLabel");
            label.textContent = slide.value;
            ctx.lineWidth = slide.value / 2;
        }
        function mousedown(event){
            draw = true;
            ctx.beginPath();
            ctx.moveTo(event.offsetX, event.offsetY);
        }
        function mousemove(event){
            if (draw){
                ctx.lineTo(event.offsetX, event.offsetY);
                ctx.stroke();
            }
        }
        function mouseup(event){
            draw = false;
            ctx.closePath();
        }
        function tokp(){
            stat = document.getElementById("status");
            stat.textContent = "converting...";
            canvas.toBlob((blob) => {
                stat.textContent = "uploading...";
                if (!blob){
                    stat.textContent = "";
                    return;
                }
                const form = new FormData();
                form.append("image", blob, "kpdrawing.png");
                fetch('/upload', {
                    method: 'POST',
                    body: form,
                })
                stat.textContent = "uploaded!"
                setTimeout(function(){
                    stat.textContent = "";
                }, 1000);
            })
        }
        function setup(){
            canvas = document.getElementById("canvas");
            ctx = canvas.getContext("2d");
            
            canvas.addEventListener("mousedown", mousedown)
            canvas.addEventListener("mousemove", mousemove)
            canvas.addEventListener("mouseup", mouseup)
        }
        
        document.addEventListener('DOMContentLoaded', setup);
    </script>
</head>
<body class="dark" style="text-align: center;">
    <h1>kp drawing</h1>
        <input
        type="color" id="colorPicker" oninput="updateColor()"
        ><label
        for="colorPicker" id="pickerLabel"> #000000</label>
        <input type="range" min="1" max="30" value="8" id="penSlider" oninput="updateSize()"> 
        <label for="penSlider" id="sliderLabel">8
        </label><button onclick="ctx.clearRect(0, 0, canvas.width, canvas.height);">
            clear
        </button>
    <br>
    <canvas id="canvas" width=300 height="200" style="border: 1px solid darkslategray;"></canvas>
    <br><button onclick="tokp()">send to kp message board</button>
    <br><p id="status"></p>
</body>
"""
    return page