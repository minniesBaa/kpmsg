## import more stuff then you would ever think youd need
from flask import Flask, request, redirect, send_from_directory, Response
from markupsafe import escape
import template_parts as html
import random
import kpdraw
import ipaddress
from waitress import serve

## define the Flask app  and APScheduler instance
#scheduler = APScheduler()
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024 

msgs = []
sigs = []
mute = []
imgs = []
allowedimg = ["0","1","2","3","4","5","6","7","8","9","10","11"]
mid = 0
motds = html.motds.motds
lf = {
    "data": None,
    "mime": None
}
with open("static/img/default.png", "rb") as f:
    lf["data"] = f.read() # type: ignore
    lf["mime"] = "image/png" # type: ignore

## define some random snippets to shorten some lines
#IMG_SEL_MENU = "<select id=\"imgsel\" name=\"e\"><option value=\"3\">no emoji</option><option value=\"0\">cat</option><option value=\"1\">car</option><option value=\"2\">smiley face</option></select><img src=\"/img/3\" id=\"pre\">"
#TITLE_PAGE = "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><script src=client.js></script><h1>kp's message board</h1>"
#DARK_CSS = "<link href=\"/dark.css\" rel=\"stylesheet\">"

def get_ip():
    try:
        res = request.headers.getlist("X-Forwarded-For")[0]
    except:
        res = str(request.remote_addr)
    obj = ipaddress.ip_address(res)
    if obj.version == 6:
        return res[:15]
    return str(res)
@app.route("/favicon.ico")
def favicon():
    return send_from_directory("static/img", "kp_1.ico")
@app.route("/noalerticon.ico")
def noalerticon():
    return send_from_directory("static/img", "kp_0.ico")

## worlds jankiest code: appends a bunch of stuff together using f-strings and claims its HTML
@app.route("/")
def main():
    global mid
    posts = f"<head><link rel=\"icon\" href=\"/favicon.ico\" type=\"image/x-icon\"></head><body style=\"padding: 20px;\">{html.post.titlepage}{random.choice(motds)}<br><br>"
    i = -1
    for post in msgs:
        i = i + 1
        imgcode = f"<img alt=\"user post emoji\" src=\"img/{imgs[i]}\">"
        posts = posts + str(escape(post[0])) + ": " + str(escape(post[1])) + " " + imgcode + "<span style=\"color:grey\"> <i>" + str(escape(sigs[i])) + "</i></span><br>"
    posts = posts + f'{html.post.form}{html.post.emoji_selection}</form>{html.post.upload_file_form}{html.ip_finder.part_1}<br><br>Latest image:<br>{html.post.latest_image}<br>{html.styling.to_dark}<br><br>Posts this session: {mid}<a style="position:fixed;top:5px;right:5px;color:black;" href="https://github.com/minniesbaa/kpmsg">⭐ Star our GitHub repository!</a>'
    return posts
@app.route("/dark")
def main_dark():
    global mid
    posts = f"<head><link rel=\"icon\" href=\"/favicon.ico\" type=\"image/x-icon\"></head><body style=\"padding: 20px;\" class=\"dark\">{html.styling.darkmode_css}{html.post.titlepage}{random.choice(motds)}<br><br>"
    i = -1
    for post in msgs:
        i = i + 1
        imgcode = f"<img alt=\"user post emoji\" src=\"img/{imgs[i]}\">"
        posts = posts + str(escape(post[0])) + ": " + str(escape(post[1])) + " " + imgcode + "<span style=\"color:grey\"> <i>" + str(escape(sigs[i])) + "</i></span><br>"
    posts = posts + f'{html.post.darkform}{html.post.emoji_selection}</form>{html.post.upload_file_form}{html.ip_finder.part_1}<br><br>Latest image:<br>{html.post.latest_image}<br>{html.styling.to_light}<br><br>Posts this session: {mid}<a style="position:fixed;top:5px;right:5px;color:white;" href="https://github.com/minniesbaa/kpmsg">⭐ Star our GitHub repository!</a>'
    return posts
@app.route("/dark/msg")
## route for message posting, containing length checks that redirect back to /dark#<hash> for alerts on page
def post_message_dark():
    global mid
    # if len(request.args.get("p")) > 100:
    #     return redirect("/dark#long")
    # if len(request.args.get("p")) == 0:
    #     return redirect("/dark#0")
    # if len(request.args.get("s")) > 40:
    #     return redirect("/dark#long2")
    thing = request.args.get('id')
    if not(thing.isdigit() and len(thing)) == 4: # type: ignore
        return redirect("/dark")
    mid = mid + 1
    tmp = []
    name = f"{get_ip().partition(',')[0]} #{request.args.get('id')}"
    tmp.append(name)
    tmp.append(request.args.get("p"))
    sigs.append(request.args.get("s"))
    msgs.append(tmp)
    if request.args.get("e") in allowedimg:
        imgs.append(request.args.get("e"))
    else:
        imgs.append("3")
    if len(msgs) > 16:
        del msgs[0]
        del sigs[0]
        del imgs[0]
    return redirect("/dark")
@app.route("/msg")
## route for message posting, containing length checks that redirect back to /#<hash> for alerts on page
def post_message():
    global mid
    # if len(request.args.get("p")) > 100:
    #     return redirect("/#long")
    # if len(request.args.get("p")) == 0:
    #     return redirect("/#0")
    # if len(request.args.get("s")) > 40:
    #     return redirect("/#long2")
    thing = request.args.get('id')
    if not(thing.isdigit() and len(thing)) == 4: # type: ignore
        return redirect("/")
    mid = mid + 1
    tmp = []
    name = f"{get_ip().partition(',')[0]} #{request.args.get('id')}"
    tmp.append(name)
    tmp.append(request.args.get("p"))
    sigs.append(request.args.get("s"))
    msgs.append(tmp)
    if request.args.get("e") in allowedimg:
        imgs.append(request.args.get("e"))
    else:
        imgs.append("3")
    if len(msgs) > 16:
        del msgs[0]
        del sigs[0]
        del imgs[0]
    return redirect("/")
@app.route("/upload", methods=["POST"])
def upload():
    fi = request.files['image']
    lf["data"] = fi.read()
    lf["mime"] = fi.mimetype # type: ignore
    global mid
    mid=mid+1
    return "o\n\nk"
@app.route("/latest")
def latest():
    return Response(lf["data"],mimetype=lf["mime"])
@app.route("/kpdrawing")
def drawing():
    if request.args.get("dark") is not None:
        return kpdraw.drawing(True)
    else:
        return kpdraw.drawing(False)
@app.route("/kpface.png")
def dingus_face():
    return send_from_directory("static/img", "kp_face.png")
## route to get the CLIENT.JS file
@app.route("/client.js")
def clientjs():
    return send_from_directory("static/script", "client.js")
## get css
@app.route("/dark.css")
def dark():
    return "BLOP. /dark.css is no longer here!", 410
    #return send_from_directory("static/css", "dark.css")
## returns the emoji for site use
@app.route("/img/<img_id>")
def img(img_id):
    return send_from_directory("static/img", f"kp_{img_id}.png")
## route to get the post ID for automatic refresh
@app.route("/api/id")
def getid():
    global mid
    return str(mid)
@app.route("/meow.mp3")
def meow():
    return send_from_directory("static/mp3", "meow.mp3")
## error handling
@app.errorhandler(404)
def fourohfour(e):
    return "<h1>Where did he go? Who knows!</h1><br>KP disappeared!", 404
@app.errorhandler(403)
def fourohthree(e):
    return "<h1>Please leave. NOW.</h1><br>please 🙏", 403
@app.errorhandler(500)
def fivehundred(e):
    return "<h1>beep boop. KP is malfunctioning!<br><br><br>We are working on fixing the KP.", 500
## run the Flask app on start
if __name__ == "__main__":
    serve(app, port=80)