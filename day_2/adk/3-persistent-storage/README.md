# การจัดเก็บข้อมูลแบบถาวรใน ADK

ตัวอย่างนี้สาธิตวิธีการใช้งานการจัดเก็บข้อมูลแบบถาวรสำหรับ Agent ใน ADK เพื่อให้ Agent สามารถจดจำข้อมูลและประวัติการสนทนาได้ข้ามหลาย session, การรีสตาร์ทแอปพลิเคชัน หรือแม้แต่การย้ายเซิร์ฟเวอร์

## Persistent Storage ใน ADK คืออะไร?

ตัวอย่างก่อนหน้านี้ใช้ `InMemorySessionService` ซึ่งเก็บข้อมูล session ไว้ในหน่วยความจำเท่านั้น ข้อมูลจะหายไปเมื่อปิดแอปพลิเคชัน สำหรับการใช้งานจริง คุณต้องการให้ Agent จดจำข้อมูลผู้ใช้และประวัติการสนทนาได้ระยะยาว ซึ่ง Persistent Storage จะช่วยในส่วนนี้

ADK มี `DatabaseSessionService` ที่ช่วยให้คุณเก็บข้อมูล session ในฐานข้อมูล SQL โดยมีข้อดีดังนี้:

1. **จดจำข้อมูลระยะยาว**: ข้อมูลไม่หายแม้รีสตาร์ทแอป
2. **ประสบการณ์ผู้ใช้ต่อเนื่อง**: ผู้ใช้สามารถกลับมาคุยต่อจากเดิมได้
3. **รองรับหลายผู้ใช้**: ข้อมูลแต่ละคนแยกกันและปลอดภัย
4. **ขยายระบบได้**: รองรับฐานข้อมูลสำหรับงานขนาดใหญ่

ตัวอย่างนี้จะแสดงการสร้าง Agent เตือนความจำที่จดจำชื่อและรายการเตือนของคุณข้ามการสนทนา โดยใช้ฐานข้อมูล SQLite

## โครงสร้างโปรเจกต์

```
5-persistent-storage/
│
├── memory_agent/               # โค้ด Agent
│   ├── __init__.py             # สำหรับให้ ADK ค้นหา agent
│   └── agent.py                # นิยาม agent และเครื่องมือเตือนความจำ
│
├── main.py                     # จุดเริ่มต้นโปรแกรมและตั้งค่าฐานข้อมูล
├── utils.py                    # ฟังก์ชันช่วยสำหรับ UI และ agent
├── .env                        # ตัวแปร environment
├── my_agent_data.db            # ไฟล์ฐานข้อมูล SQLite (สร้างเมื่อรันครั้งแรก)
└── README.md                   # เอกสารนี้
```

## ส่วนสำคัญ

### 1. DatabaseSessionService

ส่วนหลักที่ใช้จัดเก็บข้อมูลแบบถาวร คือ `DatabaseSessionService` ซึ่งต้องกำหนด URL ฐานข้อมูล:

```python
from google.adk.sessions import DatabaseSessionService

db_url = "sqlite:///./my_agent_data.db"
session_service = DatabaseSessionService(db_url=db_url)
```

บริการนี้ช่วยให้ ADK สามารถ:
- เก็บข้อมูล session ลงในไฟล์ฐานข้อมูล SQLite
- ดึงข้อมูล session ก่อนหน้าได้
- จัดการ schema ฐานข้อมูลโดยอัตโนมัติ

### 2. การจัดการ Session

ตัวอย่างนี้แสดงการจัดการ session อย่างถูกต้อง:

```python
# ตรวจสอบ session เดิมของผู้ใช้
existing_sessions = session_service.list_sessions(
    app_name=APP_NAME,
    user_id=USER_ID,
)

# ถ้ามี session เดิม ใช้ session ล่าสุด ถ้าไม่มีก็สร้างใหม่
if existing_sessions and len(existing_sessions.sessions) > 0:
    # ใช้ session ล่าสุด
    SESSION_ID = existing_sessions.sessions[0].id
    print(f"ดำเนินการต่อกับ session เดิม: {SESSION_ID}")
else:
    # สร้าง session ใหม่พร้อมสถานะเริ่มต้น
    session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID,
        state=initialize_state(),
    )
```

### 3. การจัดการ State ด้วย Tools

Agent มีเครื่องมือสำหรับอัปเดตข้อมูลแบบ persistent:

```python
def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
    # ดึงรายการเตือนปัจจุบันจากสถานะ
    reminders = tool_context.state.get("reminders", [])
    
    # เพิ่มรายการเตือนใหม่
    reminders.append(reminder)
    
    # อัปเดตสถานะด้วยรายการเตือนใหม่
    tool_context.state["reminders"] = reminders
    
    return {
        "action": "add_reminder",
        "reminder": reminder,
        "message": f"Added reminder: {reminder}",
    }
```

ทุกครั้งที่เปลี่ยนแปลง `tool_context.state` ข้อมูลจะถูกบันทึกลงฐานข้อมูลโดยอัตโนมัติ

## เริ่มต้นใช้งาน

### สิ่งที่ต้องมี

- Python 3.9 ขึ้นไป
- Google API Key สำหรับ Gemini
- SQLite (มากับ Python)

### การตั้งค่า

1. เปิดใช้งาน virtual environment จากโฟลเดอร์ root:
```bash
# macOS/Linux:
source ../.venv/bin/activate
# Windows CMD:
..\.venv\Scripts\activate.bat
# Windows PowerShell:
..\.venv\Scripts\Activate.ps1
```

2. ตรวจสอบว่าใส่ Google API Key ในไฟล์ `.env` แล้ว:
```
GOOGLE_API_KEY=your_api_key_here
```

### การรันตัวอย่าง

รันตัวอย่างการจัดเก็บข้อมูลแบบถาวร:

```bash
python main.py
```

สิ่งที่จะเกิดขึ้น:
1. เชื่อมต่อกับฐานข้อมูล SQLite (หรือสร้างใหม่ถ้ายังไม่มี)
2. ตรวจสอบ session เดิมของผู้ใช้
3. เริ่มสนทนากับ Agent น้อง Neko
4. บันทึกทุกการสนทนาลงฐานข้อมูล

### ตัวอย่างการสนทนา

ลองพิมพ์ข้อความเหล่านี้เพื่อทดสอบความสามารถในการจดจำของ Agent:

1. **รอบแรก:**
   - "ชื่อฉันคืออะไร?"
   - "ฉันชื่อ John"
   - "เพิ่มรายการเตือนซื้อของ"
   - "เพิ่มรายการเตือนส่งรายงาน"
   - "มีรายการเตือนอะไรบ้าง?"
   - ออกจากโปรแกรมด้วย "exit"

2. **รอบสอง:**
   - "ชื่อฉันคืออะไร?"
   - "มีรายการเตือนอะไรบ้าง?"
   - "แก้ไขรายการที่สองเป็นส่งรายงานภายในวันศุกร์"
   - "ลบรายการแรก"

Agent จะจดจำชื่อและรายการเตือนของคุณข้ามการรันโปรแกรม!

## การใช้งานฐานข้อมูลในระบบจริง

ตัวอย่างนี้ใช้ SQLite เพื่อความง่าย แต่ `DatabaseSessionService` รองรับฐานข้อมูลอื่น ๆ ผ่าน SQLAlchemy:

- PostgreSQL: `postgresql://user:password@localhost/dbname`
- MySQL: `mysql://user:password@localhost/dbname`
- MS SQL Server: `mssql://user:password@localhost/dbname`

สำหรับการใช้งานจริง:
1. เลือกฐานข้อมูลที่เหมาะกับงานของคุณ
2. ตั้งค่าการเชื่อมต่อและ pooling ให้มีประสิทธิภาพ
3. ดูแลความปลอดภัยของข้อมูลและรหัสผ่าน
4. สำรองข้อมูลฐานข้อมูลเป็นประจำ

## แหล่งข้อมูลเพิ่มเติม

- [ADK Sessions Documentation](https://google.github.io/adk-docs/sessions/session/)
- [Session Service Implementations](https://google.github.io/adk-docs/sessions/session/#sessionservice-implementations)
- [State Management in ADK](https://google.github.io/adk-docs/sessions/state/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/) สำหรับการตั้งค่าฐานข้อมูลขั้นสูง
