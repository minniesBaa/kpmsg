class motds_:
    def __init__(self):
        self.motds = ["extremely inefficent!", "for doing your message board things", "kp approves", "BLOP.", "now with emojis!", "now featuring an unhealthy amount of f-strings", "time to redeploy! AGAIN"]
class styling_:
    def __init__(self):
        self.darkmode_css = "<style>.dark {background-color: #262626;color: white;}</style>"
        self.to_dark ="<br><a href=\"/dark\">dark mode</a><br><a href='/kpdrawing' target='_blank'>kp drawing editor</a></body>"
        self.to_light = '<br><a href="/" style="color:white;">light mode</a></body><br><a href="/kpdrawing?dark" target="_blank" style="color:white;">kp drawing editor</a>'
class ip_finder_:
    def __init__(self):
        self.part_2 = '\')">click to show</button>'
        self.part_1 = '<br>Chat messages show your IP. Do not post if you wish to hide your IP.<br>Your IP is: <button type="button" onclick="w=open(\'\',\'ip\',\'popup,width=200,height=100\');w.document.write(\'your ip is: '
class post_:
    def __init__(self):
        self.form = '<br><head><link rel="icon" href="/favicon.ico" type="image/x-icon"><title>kp\'s message board | for doing message board things</title></head><form action="/msg" method="GET"><input placeholder="post text" type="text" id="post_text" name="p"><button type="submit">post</button><br><input placeholder="signature" type="text" id="signature" name="s"><input id="num" type="hidden" name=id>'
        self.darkform = '<br><head><link rel="icon" href="/favicon.ico" type="image/x-icon"><title>kp\'s message board | for doing message board things</title></head><form action="/dark/msg" method="GET"><input placeholder="post text" type="text" id="post_text" name="p"><button type="submit">post</button><br><input placeholder="signature" type="text" id="signature" name="s"><input id="num" type="hidden" name=id>'
        self.titlepage = "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\"><script src=client.js></script><h1><img src=\"/kpface.png\" width=38 height=30>kp's message board</h1>"
        self.emoji_selection = "<select id=\"imgsel\" name=\"e\">\
        <option value=\"3\">no emoji</option>\
        <option value=\"0\">cat</option>\
        <option value=\"1\">car</option>\
        <option value=\"2\">smiley face</option>\
        <option value=\"4\">sad face</option>\
        <option value=\"5\">bread loaf</option>\
        <option value=\"6\">kibble bag</option>\
        <option value=\"7\">yummy grass</option>\
        <option value=\"8\">musical note</option>\
        <option value=\"9\">cheese wedge</option>\
        <option value=\"10\">chocolate bar</option>\
        </select><img src=\"/img/3\" id=\"pre\">"
        self.upload_file_form = '<br><label for="imageFile">Select an image to upload: </label>\
            <input type="file" id="imageFile" accept="image/*">\
            <button id="upload">post</button><br>\
            '
        self.latest_image = '<img src="/latest" width=150>'
post = post_()
motds = motds_()
styling = styling_()
ip_finder = ip_finder_()