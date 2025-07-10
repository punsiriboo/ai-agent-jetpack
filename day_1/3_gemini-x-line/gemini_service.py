from google import genai
from google.genai import types
import os, io
from PIL import Image as PILImage
from dotenv import load_dotenv

load_dotenv("../.env")

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL="gemini-2.0-flash"
AI_INSTRUCTION_PROMPT = """
คุณคือผู้ช่วยร้านอาหารชื่อ 'เนโกะ' 🐱
คุณพูดจาน่ารัก สุภาพ ใช้คำลงท้ายว่า 'เมี๊ยว~'
หน้าที่ของคุณคือช่วยลูกค้าร้านหาร
เมื่อลูกค้าถามถึงเมนู ให้ดููข้อมูลจากระบบเพื่อตอบ ถ้าไม่รู้ ให้ตอบอย่างสุภาพว่าไม่รู้
เมื่อลูกค้าต้องการของคิว เช็กคิวว่างจากระบบเพื่อจองโต๊ะให้ลูกค้า ถ้าไม่รู้ว่ามีคิวว่าเวลาไหนบ้าง ให้ตอบอย่างสุภาพว่าไม่รู้
"""

def generate_text(text):
    response = client.models.generate_content(
        model=MODEL,
        contents=[text],
        config=types.GenerateContentConfig(
            system_instruction=AI_INSTRUCTION_PROMPT,
            max_output_tokens=200,
        ),
    )
    print(f"Gemini response: {response.text}")
    return response.text


def image_understanding(image_content):
    image_data = PILImage.open(io.BytesIO(image_content))

    prompt = "What is shown in this image in Thai?"
    response = client.models.generate_content(
        model=MODEL,
        system_instruction=AI_INSTRUCTION_PROMPT,
        contents=[prompt, image_data],
        config=types.GenerateContentConfig(
            max_output_tokens=200,
        ),
    )
    print(f"Gemini response: {response.text}")
    return response.text


def document_understanding(file_content):
    prompt = "Summarize this document in Thai"
    pdf_data = types.Part.from_bytes(data=file_content, mime_type="application/pdf")
    response = client.models.generate_content(
        model=MODEL,
        system_instruction=AI_INSTRUCTION_PROMPT,
        contents=[pdf_data,prompt],
        config=types.GenerateContentConfig(
            max_output_tokens=200,
        ),
    )
    print(f"Gemini response: {response.text}")
    return response.text
