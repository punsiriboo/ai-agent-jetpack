import os
import functions_framework
from dotenv import load_dotenv


from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3 import WebhookHandler
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    StickerMessageContent,
    LocationMessageContent,
    ImageMessageContent,
    VideoMessageContent,
    AudioMessageContent,
    FileMessageContent,
)

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    ShowLoadingAnimationRequest,
    LocationMessage,
)

load_dotenv()
CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]


configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
api_client = ApiClient(configuration)
line_bot_api = MessagingApi(api_client)


@functions_framework.http
def callback(request):
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    print("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print(
            "Invalid signature. Please check your channel access token/channel secret."
        )

    return "OK"


@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    line_bot_api.show_loading_animation(
        ShowLoadingAnimationRequest(chat_id=event.source.user_id)
    )
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=event.message.text)],
        )
    )


@handler.add(MessageEvent, message=StickerMessageContent)
def handle_sticker_message(event):
    line_bot_api.show_loading_animation_with_http_info(
        ShowLoadingAnimationRequest(chat_id=event.source.user_id)
    )
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text="Got sticker message")],
        )
    )


@handler.add(MessageEvent, message=LocationMessageContent)
def handle_location_message(event):
    line_bot_api.show_loading_animation_with_http_info(
        ShowLoadingAnimationRequest(chat_id=event.source.user_id)
    )
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[
                TextMessage(text="Got location message {},{}"),
                LocationMessage(
                    title="Location",
                    address=event.message.address,
                    latitude=event.message.latitude,
                    longitude=event.message.longitude,
                ),
            ],
        )
    )


@handler.add(
    MessageEvent,
    message=(ImageMessageContent, VideoMessageContent, AudioMessageContent),
)
def handle_content_message(event):
    line_bot_api.show_loading_animation_with_http_info(
        ShowLoadingAnimationRequest(chat_id=event.source.user_id)
    )
    if isinstance(event.message, ImageMessageContent):
        ftype = "image"
    elif isinstance(event.message, VideoMessageContent):
        ftype = "viedio"
    elif isinstance(event.message, AudioMessageContent):
        ftype = "audio"
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[
                TextMessage(text=f"Thank for sending {ftype} file"),
            ],
        )
    )


@handler.add(MessageEvent, message=FileMessageContent)
def handle_file_message(event):
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[
                TextMessage(text="Thank for sending the file."),
            ],
        )
    )
