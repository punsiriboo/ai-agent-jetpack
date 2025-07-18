
# นำเข้าไลบรารีสำหรับจัดการ asynchronous
import asyncio

# โหลด environment variables จากไฟล์ .env
from dotenv import load_dotenv

# นำเข้า Runner สำหรับรัน agent, DatabaseSessionService สำหรับจัดการ session แบบถาวร
# นำเข้า memory_agent (Agent ที่สร้างไว้) และฟังก์ชัน call_agent_async สำหรับเรียกใช้งาน agent แบบ async
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from memory_agent.agent import memory_agent
from utils import call_agent_async


# โหลด environment variables
load_dotenv()


# ===== ส่วนที่ 1: สร้าง session service แบบ persistent =====
# ใช้ฐานข้อมูล SQLite สำหรับเก็บข้อมูลแบบถาวร
db_url = "sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)



# ===== ส่วนที่ 2: กำหนดข้อมูลเริ่มต้นของ session =====
# ใช้ข้อมูลนี้เมื่อสร้าง session ใหม่เท่านั้น
initial_state = {
    "user_name": "Beat AI Agent",
    "reminders": [],
}



async def main_async():
    # กำหนดค่าคงที่สำหรับชื่อแอปและผู้ใช้
    APP_NAME = "Neko Memory Agent"
    USER_ID = "beataiagent"

    # ===== ส่วนที่ 3: จัดการ session - ค้นหาหรือสร้างใหม่ =====
    # ตรวจสอบว่ามี session เดิมสำหรับผู้ใช้นี้หรือไม่
    existing_sessions = session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID,
    )

    # ถ้ามี session เดิมอยู่แล้ว ให้ใช้ session ล่าสุด ถ้าไม่มีก็สร้างใหม่
    if existing_sessions and len(existing_sessions.sessions) > 0:
        # ใช้ session ล่าสุด
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"ดำเนินการต่อกับ session เดิม: {SESSION_ID}")
    else:
        # สร้าง session ใหม่พร้อมข้อมูลเริ่มต้น
        new_session = session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state,
        )
        SESSION_ID = new_session.id
        print(f"สร้าง session ใหม่: {SESSION_ID}")

    # ===== ส่วนที่ 4: สร้าง runner สำหรับ agent =====
    runner = Runner(
        agent=memory_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # ===== ส่วนที่ 5: วนลูปสนทนาแบบโต้ตอบกับผู้ใช้ =====
    print("\nยินดีต้อนรับสู่ Memory Agent Chat!")
    print("รายการเตือนของคุณจะถูกจดจำข้ามการสนทนา")
    print("พิมพ์ 'exit' หรือ 'quit' เพื่อจบการสนทนา\n")

    while True:
        # รับข้อความจากผู้ใช้
        user_input = input("You: ")

        # ตรวจสอบว่าผู้ใช้ต้องการออกจากโปรแกรมหรือไม่
        if user_input.lower() in ["exit", "quit"]:
            print("จบการสนทนา ข้อมูลของคุณถูกบันทึกลงฐานข้อมูลแล้ว")
            break

        # ส่งข้อความของผู้ใช้ไปยัง agent เพื่อประมวลผล
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)



# จุดเริ่มต้นโปรแกรม
if __name__ == "__main__":
    asyncio.run(main_async())
