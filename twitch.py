
import json
import urllib.request
import urllib.error
import urllib.parse
import os.path


# Settings
TWITCH_USERNAME = "enter-your-username-here"
CLIENT_ID = "enter-your-client-id-here"

# Let's fetch and parse data from twitch
R = urllib.request.urlopen("https://api.twitch.tv/kraken/users/" + TWITCH_USERNAME + "/follows/channels?client_id="+ CLIENT_ID +"&limit=75").read()
RAW_DATA = json.loads(R)
OUTPUT = ""

PAGES = (RAW_DATA["_total"] - 1) // 75
for PAGE in range(0, PAGES+1):
    if (PAGE != 0):
        R = urllib.request.urlopen("https://api.twitch.tv/kraken/users/"+ TWITCH_USERNAME + "/follows/channels?client_id="+ CLIENT_ID +"&direction=DESC&limit=75&offset=%d&sortby=created_at" % (75 * page)).read()
        RAW_DATA = json.loads(R)

# Get followed channels
FOLLOWED_CHANNELS = []
for channel in RAW_DATA["follows"]:
    FOLLOWED_CHANNELS.append(channel["channel"]["name"])

  # Get live streams
R = urllib.request.urlopen("https://api.twitch.tv/kraken/streams?client_id="+ CLIENT_ID + "&channel=%s" % ','.join(FOLLOWED_CHANNELS))
LIVE_STREAMS = json.loads(R.read())

for stream in LIVE_STREAMS["streams"]:
    channel_name = stream["channel"]["display_name"]

    # For some strange reason channel status and game sometimes temporarily
    # disappears from Twitch API, causing problems in this script. It this case,
    # we don't show status/game in conky at all.
    try:
        channel_title = stream["channel"]["status"]
    except KeyError:
        channel_title = ""

    try:
        channel_game = stream["channel"]["game"]
    except KeyError:
        channel_game = ""

    # Build OUTPUT string
    OUTPUT += "${color black}" + channel_name + " is ${color LawnGreen}LIVE"

    if channel_title != "":
        OUTPUT += "\n${color black}" + channel_title

    if channel_game != "":
        OUTPUT += "\n${color yellow}" + channel_game

    OUTPUT += "\n\n"

# No live channels?
if OUTPUT == "":
    OUTPUT = "No live channels"

# Write OUTPUT to file
OUTPUT = OUTPUT.replace("#", "\\#") # Preventing twitch titles from messing with conky config
PATH = os.path.dirname(__file__) + "/"

if PATH == "/":
    PATH = ""

F = open(PATH + "streams-test.txt", "wb")
F.write(OUTPUT.encode('utf8'))
F.close()
