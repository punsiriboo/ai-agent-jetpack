from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext


def get_nerd_joke(topic: str, tool_context: ToolContext) -> dict:
    """Get a nerdy joke about a specific topic."""
    print(f"--- Tool: get_nerd_joke called for topic: {topic} ---")

    # สร้างตัวอย่างมุกตลก - ในการใช้งานจริง อาจใช้ API
    jokes = {
        "python": "ทำไมนักเขียนโปรแกรม Python ไม่ชอบใช้ inheritance? เพราะเขาไม่ชอบรับมรดกอะไรทั้งนั้น!",
        "javascript": "ทำไมนักพัฒนา JavaScript ถึงหมดตัว? เพราะเขาใช้ cache หมดเกลี้ยง!",
        "java": "ทำไมนักพัฒนา Java ถึงต้องใส่แว่น? เพราะเขามองไม่เห็น C#!",
        "programming": "ทำไมนักเขียนโปรแกรมถึงชอบโหมดมืด? เพราะแสงดึงดูดบั๊ก!",
        "math": "ทำไมเครื่องหมายเท่ากับถึงถ่อมตัว? เพราะมันรู้ว่าตัวเองไม่มากกว่าหรือน้อยกว่าใคร!",
        "physics": "ทำไมโฟตอนถึงเข้าพักโรงแรม? เพราะมันเดินทางแบบเบา!",
        "chemistry": "ทำไมกรดถึงไปออกกำลังกาย? เพื่อเป็นสารบัฟเฟอร์!",
        "biology": "ทำไมเซลล์ถึงไปบำบัด? เพราะมันมีปัญหาเยอะ!",
        "default": "ทำไมคอมพิวเตอร์ถึงไปหาหมอ? เพราะมันติดไวรัส!",
    }

    joke = jokes.get(topic.lower(), jokes["default"])

    # Update state with the last joke topic
    tool_context.state["last_joke_topic"] = topic

    return {"status": "success", "joke": joke, "topic": topic}


# Create the funny nerd agent
funny_nerd = Agent(
    name="funny_nerd",
    model="gemini-2.0-flash",
    description="Agent ที่เล่าเรื่องตลกเนิร์ดเกี่ยวกับหัวข้อต่าง ๆ",
    instruction="""
    คุณคือ agent เนิร์ดตลกที่เล่าเรื่องตลกเนิร์ดเกี่ยวกับหัวข้อต่าง ๆ

    เมื่อถูกขอให้เล่าเรื่องตลก:
    1. ใช้เครื่องมือ get_nerd_joke เพื่อดึงเรื่องตลกเกี่ยวกับหัวข้อที่ร้องขอ
    2. หากไม่มีการระบุหัวข้อ ให้ถามผู้ใช้ว่าต้องการเรื่องตลกเนิร์ดเกี่ยวกับอะไร
    3. จัดรูปแบบคำตอบให้มีทั้งเรื่องตลกและคำอธิบายสั้น ๆ หากจำเป็น

    หัวข้อที่มีให้เลือก ได้แก่:
    - python
    - javascript
    - java
    - programming
    - math
    - physics
    - chemistry
    - biology

    ตัวอย่างรูปแบบคำตอบ:
    "นี่คือเรื่องตลกเนิร์ดเกี่ยวกับ <TOPIC>:
    <JOKE>

    คำอธิบาย: {คำอธิบายสั้น ๆ หากจำเป็น}"

    หากผู้ใช้ถามเรื่องอื่น
    คุณควรมอบหมายงานให้กับ manager agent
    """,
    tools=[get_nerd_joke],
)
