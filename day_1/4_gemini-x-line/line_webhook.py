# Import libraries ที่ใช้
import os, base64
import functions_framework
from dotenv import load_dotenv

# LINE SDK
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3 import WebhookHandler
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    ImageMessageContent,
    FileMessageContent,
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    TextMessage,
    ShowLoadingAnimationRequest,
)

# โหลด .env สำหรับตั้งค่าคีย์ลับจากไฟล์
load_dotenv("../.env")

# ดึงค่าจาก environment
CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

# เตรียม configuration สำหรับ LINE Messaging API
configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)
api_client = ApiClient(configuration)
line_bot_api = MessagingApi(api_client)
line_bot_blob_api = MessagingApiBlob(api_client)

# import ฟังก์ชันจาก service ที่เรียก Gemini API
from gemini_service import generate_text, image_understanding, document_understanding

# Function สำหรับรับ webhook จาก LINE
@functions_framework.http
def webhook_listening(request):
    # ดึงค่า Signature จาก header
    signature = request.headers["X-Line-Signature"]

    # แปลง request body เป็น text
    body = request.get_data(as_text=True)
    print("Request body: " + body)

    # ตรวจสอบและส่งให้ handler จาก LINE SDK จัดการ
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")

    return "OK"

# กรณีข้อความเป็นประเภท Text
@handler.add(MessageEvent, message=TextMessageContent)
def handle_text_message(event):
    # แสดง animation ระหว่างประมวลผล (LINE Premium Function)
    line_bot_api.show_loading_animation(
        ShowLoadingAnimationRequest(chat_id=event.source.user_id)
    )

    # ส่งข้อความไปให้ Gemini ประมวลผล
    gemini_reponse = generate_text(event.message.text)

    # ตอบกลับข้อความที่ได้จาก Gemini
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=gemini_reponse)],
        )
    )

# กรณีข้อความเป็นรูปภาพ
@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image_message(event):
    # แสดง animation ระหว่างประมวลผล
    line_bot_api.show_loading_animation_with_http_info(
        ShowLoadingAnimationRequest(chat_id=event.source.user_id)
    )

    # ดึง binary ของภาพจาก LINE server
    message_content = line_bot_blob_api.get_message_content(message_id=event.message.id)

    # ส่งไปให้ Gemini วิเคราะห์ภาพ
    gemini_reponse = image_understanding(message_content)

    # ตอบกลับผลลัพธ์จาก Gemini
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=gemini_reponse)],
        )
    )

# กรณีข้อความเป็นไฟล์เอกสาร
@handler.add(MessageEvent, message=FileMessageContent)
def handle_file_message(event):
    # ดึง binary ของไฟล์จาก LINE server
    doc_content = line_bot_blob_api.get_message_content(message_id=event.message.id)

    # ส่งไปให้ Gemini วิเคราะห์เนื้อหาในเอกสาร
    gemini_reponse = document_understanding(doc_content)

    # ตอบกลับผลลัพธ์จาก Gemini
    line_bot_api.reply_message(
        ReplyMessageRequest(
            reply_token=event.reply_token,
            messages=[TextMessage(text=gemini_reponse)],
        )
    )
