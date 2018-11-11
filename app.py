from __future__ import unicode_literals

import errno, os, sys, tempfile, urllib, json
import urllib.request
import requests

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    PostbackTemplateAction, DatetimePickerTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)

import json
app = Flask(__name__)

# get variables from your environment variable
channel_secret = os.environ.get('LINE_CHANNEL_SECRET', None)
channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)
allowed_groupid = os.environ.get('ALLOWED_GROUPID', None)
admin_id = os.environ.get('ADMIN_ID', None)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

try:
    profile = line_bot_api.get_profile('<user_id>')
    print(profile.display_name)
    print(profile.user_id)
    print(profile.picture_url)
    print(profile.status_message)
except LineBotApiError as e:
    # error handle
    ...
# function for create tmp dir for download content
def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise
#def add_groupwhitelist(group_id):
 #   global dbfb
  #  ref = db.reference('/whitelist_groups'. dbfb)
   # group = ref.get()
   # if group == None:
    #    group = []
   # ref.child(str(len(group))).set(str(group_id))
   # message = "group {} has been whitelisted.".format(str(group_id))
   # return message

def jokes():
    jokesurl = 'http://api.icndb.com/jokes/random'
    req = urllib.request.urlopen(jokesurl)
    jokes = json.loads(req.read())
    content = jokes['value']['joke']
    return content

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    ImageSendMessage = event.message.image
    if text == '/bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextMessage(text='Dadah beb :*'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextMessage(text='Dadah beb :*'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token, TextMessage(text="NGGAK BISALAH BAMBANG"))
    if '/joke' and '/j' in text:
        content = jokes()
        line_bot_api.reply_message(
            event.reply_token, TextMessage(text='Danes ganteng ya'))
   # if '/main' and '/m' in text:    
    #    line_bot_api.reply_message(
    #       event.reply_token, ImageSendMessage(id="file:///C:/Users/VivoBook/Desktop/baymax/1.jpg"))

    #if '/main' and '/m' in text:
     #   ImageMessage = ImageSendMessage(
    #ImageMessage='file:///C:/Users/VivoBook/Desktop/baymax/1.jpg')
       
    if '/ping' and '/p' in text:
        line_bot_api.reply_message(
            event.reply_token, TextMessage(text='pong!'))

    elif '/help' and '/h' in text:
        content = 'Available commands:\n/m - gambar.\n/j - Ada deh.\n/h - mau tau aja.\n/ping - pong.'
        line_bot_api.reply_message(
            event.reply_token, TextMessage(text=content))

@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Hi, I'm Baymax. Your personal Bot. Thanks for inviting me to this "+ event.source.type + " I love you :*" ))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
