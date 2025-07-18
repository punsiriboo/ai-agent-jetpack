# นำเข้าไลบรารีสำหรับสร้างรหัส session แบบสุ่ม
import uuid

# โหลด environment variables จากไฟล์ .env
from dotenv import load_dotenv

# นำเข้า Runner สำหรับรัน agent, InMemorySessionService สำหรับจัดการ session, types สำหรับสร้างข้อความ และ agent ที่สร้างไว้
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent


# โหลด environment variables
load_dotenv("../.env", override=True)



# สร้าง session service สำหรับเก็บสถานะของผู้ใช้
session_service_stateful = InMemorySessionService()

# กำหนดชื่อผู้ใช้
user_name = "Beat AI Agent"

# กำหนดข้อมูลเริ่มต้นของ session (state) สำหรับตอบคำถามเกี่ยวกับผู้ใช้
initial_state = {
    "user_name": user_name,
    "user_preferences": """
        ฉันชอบเล่นกีฬา Pickleball, Disc Golf และ เทนนิส
        อาหารที่ชื่นชอบคืออาหารเม็กซิกัน
        รายการทีวีโปรดคือ Game of Thrones
        มีความสุขเมื่อมีคนกดไลก์และกดติดตามช่อง YouTube ของเขา
        (ข้อมูลนี้ใช้สำหรับตอบคำถามเกี่ยวกับความชอบของผู้ใช้)
    """,
}


# สร้าง session ใหม่สำหรับผู้ใช้
APP_NAME = user_name
USER_ID = user_name
SESSION_ID = str(uuid.uuid4())
stateful_session = session_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state,
)
print("CREATED NEW SESSION:")
print(f"\tSession ID: {SESSION_ID}")


# สร้าง Runner สำหรับรัน agent โดยใช้ session ที่สร้างขึ้น
runner = Runner(
    agent=question_answering_agent,
    app_name=APP_NAME,
    session_service=session_service_stateful,
)


# สร้างข้อความใหม่เพื่อถาม agent ว่า "Brandon ชอบดูรายการทีวีอะไร"
new_message = types.Content(
    role="user", parts=[types.Part(text="What is Brandon's favorite TV show?")]
)


# รัน agent เพื่อรับคำตอบจาก session และแสดงผลลัพธ์สุดท้าย
for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message,
):
    if event.is_final_response():
        if event.content and event.content.parts:
            print(f"Final Response: {event.content.parts[0].text}")


# สำรวจ session event และแสดงสถานะสุดท้ายของ session
print("==== Session Event Exploration ====")
session = session_service_stateful.get_session(
    app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
)

# แสดงข้อมูลสถานะสุดท้ายของ session
print("=== Final Session State ===")
for key, value in session.state.items():
    print(f"{key}: {value}")
