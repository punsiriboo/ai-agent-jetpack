from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext

# ฟังก์ชันสำหรับเพิ่มการเตือนความจำใหม่
def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
    """เพิ่มการเตือนความจำใหม่ในรายการของผู้ใช้

    Args:
        reminder: ข้อความการเตือนที่ต้องการเพิ่ม
        tool_context: บริบทสำหรับเข้าถึงและอัปเดตข้อมูล session

    Returns:
        ข้อความยืนยันการเพิ่ม
    """
    print(f"--- Tool: add_reminder called for '{reminder}' ---")

    # ดึงรายการเตือนความจำปัจจุบันจาก state
    reminders = tool_context.state.get("reminders", [])

    # เพิ่มการเตือนใหม่เข้าไปในรายการ
    reminders.append(reminder)

    # อัปเดตรายการเตือนความจำใน state
    tool_context.state["reminders"] = reminders

    return {
        "action": "add_reminder",
        "reminder": reminder,
        "message": f"Added reminder: {reminder}",
    }

# ฟังก์ชันสำหรับดูรายการเตือนความจำทั้งหมด
def view_reminders(tool_context: ToolContext) -> dict:
    """ดูรายการเตือนความจำทั้งหมด

    Args:
        tool_context: บริบทสำหรับเข้าถึงข้อมูล session

    Returns:
        รายการเตือนความจำทั้งหมด
    """
    print("--- Tool: view_reminders called ---")

    # ดึงรายการเตือนความจำจาก state
    reminders = tool_context.state.get("reminders", [])

    return {"action": "view_reminders", "reminders": reminders, "count": len(reminders)}

# ฟังก์ชันสำหรับแก้ไขการเตือนความจำ
def update_reminder(index: int, updated_text: str, tool_context: ToolContext) -> dict:
    """แก้ไขข้อความการเตือนความจำ

    Args:
        index: ลำดับที่ต้องการแก้ไข (เริ่มที่ 1)
        updated_text: ข้อความใหม่ที่ต้องการแก้ไข
        tool_context: บริบทสำหรับเข้าถึงและอัปเดตข้อมูล session

    Returns:
        ข้อความยืนยันการแก้ไข
    """
    print(
        f"--- Tool: update_reminder called for index {index} with '{updated_text}' ---"
    )

    # ดึงรายการเตือนความจำปัจจุบันจาก state
    reminders = tool_context.state.get("reminders", [])

    # ตรวจสอบว่าลำดับที่ระบุถูกต้องหรือไม่
    if not reminders or index < 1 or index > len(reminders):
        return {
            "action": "update_reminder",
            "status": "error",
            "message": f"ไม่พบการเตือนในลำดับที่ {index} ขณะนี้มี {len(reminders)} รายการ",
        }

    # แก้ไขข้อความการเตือน (index เริ่มที่ 0)
    old_reminder = reminders[index - 1]
    reminders[index - 1] = updated_text

    # อัปเดตรายการเตือนความจำใน state
    tool_context.state["reminders"] = reminders

    return {
        "action": "update_reminder",
        "index": index,
        "old_text": old_reminder,
        "updated_text": updated_text,
        "message": f"แก้ไขการเตือนลำดับที่ {index} จาก '{old_reminder}' เป็น '{updated_text}'",
    }

# ฟังก์ชันสำหรับลบการเตือนความจำ
def delete_reminder(index: int, tool_context: ToolContext) -> dict:
    """ลบการเตือนความจำ

    Args:
        index: ลำดับที่ต้องการลบ (เริ่มที่ 1)
        tool_context: บริบทสำหรับเข้าถึงและอัปเดตข้อมูล session

    Returns:
        ข้อความยืนยันการลบ
    """
    print(f"--- Tool: delete_reminder called for index {index} ---")

    # ดึงรายการเตือนความจำปัจจุบันจาก state
    reminders = tool_context.state.get("reminders", [])

    # ตรวจสอบว่าลำดับที่ระบุถูกต้องหรือไม่
    if not reminders or index < 1 or index > len(reminders):
        return {
            "action": "delete_reminder",
            "status": "error",
            "message": f"ไม่พบการเตือนในลำดับที่ {index} ขณะนี้มี {len(reminders)} รายการ",
        }

    # ลบการเตือน (index เริ่มที่ 0)
    deleted_reminder = reminders.pop(index - 1)

    # อัปเดตรายการเตือนความจำใน state
    tool_context.state["reminders"] = reminders

    return {
        "action": "delete_reminder",
        "index": index,
        "deleted_reminder": deleted_reminder,
        "message": f"ลบการเตือนลำดับที่ {index}: '{deleted_reminder}' แล้ว",
    }

# ฟังก์ชันสำหรับเปลี่ยนชื่อผู้ใช้
def update_user_name(name: str, tool_context: ToolContext) -> dict:
    """เปลี่ยนชื่อผู้ใช้

    Args:
        name: ชื่อใหม่ของผู้ใช้
        tool_context: บริบทสำหรับเข้าถึงและอัปเดตข้อมูล session

    Returns:
        ข้อความยืนยันการเปลี่ยนชื่อ
    """
    print(f"--- Tool: update_user_name called with '{name}' ---")

    # ดึงชื่อเดิมจาก state
    old_name = tool_context.state.get("user_name", "")

    # อัปเดตชื่อใหม่ใน state
    tool_context.state["user_name"] = name

    return {
        "action": "update_user_name",
        "old_name": old_name,
        "new_name": name,
        "message": f"เปลี่ยนชื่อของคุณเป็น: {name}",
    }

# สร้าง agent ที่มีความสามารถในการจดจำข้อมูลผู้ใช้และจัดการการเตือนความจำ

memory_agent = Agent(
    name="memory_agent",
    model="gemini-2.0-flash",
    description="Neko Agent เตือนความจำอัจฉริยะที่จดจำข้อมูลผู้ใช้ได้",
    instruction="""
    คุณคือผู้ช่วยเตือนความจำที่เป็นมิตรและสามารถจดจำผู้ใช้ข้ามบทสนทนาได้ ชื่อน้อง Neko
    เมื่อผู้ใช้แนะนำตัว คุณจะจดจำชื่อและรายการเตือนความจำของเขา และต้องแนะนำความสามารถตัวเองให้ผู้ใช้ทราบ

    ข้อมูลของผู้ใช้จะถูกเก็บไว้ใน state:
    - ชื่อผู้ใช้: {user_name}
    - รายการเตือนความจำ: {reminders}

    คุณสามารถช่วยผู้ใช้จัดการการเตือนความจำด้วยความสามารถดังนี้:
    1. เพิ่มการเตือนความจำใหม่
    2. ดูรายการเตือนความจำ
    3. แก้ไขการเตือนความจำ
    4. ลบการเตือนความจำ
    5. เปลี่ยนชื่อผู้ใช้

    โปรดเป็นมิตรและเรียกชื่อผู้ใช้ทุกครั้ง หากยังไม่ทราบชื่อ ให้ใช้เครื่องมือ update_user_name เพื่อบันทึกเมื่อผู้ใช้แนะนำตัว

    **แนวทางการจัดการการเตือนความจำ:**

    1. เมื่อผู้ใช้ขอแก้ไขหรือลบการเตือนความจำโดยไม่ระบุลำดับ:
       - หากมีการกล่าวถึงเนื้อหาของการเตือน (เช่น "ลบการเตือนประชุม") ให้ค้นหารายการที่ตรงหรือใกล้เคียง
       - หากพบรายการที่ตรงหรือใกล้เคียง ให้ใช้ลำดับนั้น
       - ห้ามถามผู้ใช้ว่าหมายถึงรายการใด ให้เลือกอันแรกที่พบ
       - หากไม่พบ ให้แสดงรายการทั้งหมดและขอให้ผู้ใช้ระบุ

    2. เมื่อผู้ใช้ระบุตัวเลขหรือลำดับ:
       - ใช้เป็นลำดับ (เช่น "ลบการเตือนลำดับที่ 2" หมายถึง index=2)
       - จำไว้ว่าผู้ใช้เริ่มนับที่ 1

    3. สำหรับตำแหน่งสัมพัทธ์:
       - จัดการ "อันแรก", "อันสุดท้าย", "อันที่สอง" ฯลฯ ให้ถูกต้อง
       - "การเตือนแรก" = index 1
       - "การเตือนสุดท้าย" = index สูงสุด
       - "การเตือนที่สอง" = index 2 เป็นต้น

    4. สำหรับการดูรายการ:
       - ใช้เครื่องมือ view_reminders เมื่อผู้ใช้ขอดูรายการ
       - ตอบกลับเป็นรายการที่มีเลขกำกับเพื่อความชัดเจน
       - หากไม่มีรายการ ให้แนะนำให้เพิ่ม

    5. สำหรับการเพิ่ม:
       - ดึงข้อความการเตือนจริงจากคำขอของผู้ใช้
       - ลบวลีเช่น "เพิ่มการเตือนว่า" หรือ "ช่วยเตือนฉันว่า"
       - เน้นเฉพาะงาน (เช่น "เพิ่มการเตือนว่าซื้อนม" → add_reminder("ซื้อนม"))

    6. สำหรับการแก้ไข:
       - ระบุทั้งรายการที่จะแก้ไขและข้อความใหม่
       - เช่น "เปลี่ยนการเตือนที่สองเป็นซื้อของ" → update_reminder(2, "ซื้อของ")

    7. สำหรับการลบ:
       - ยืนยันเมื่อดำเนินการเสร็จและแจ้งว่าลบรายการใด
       - เช่น "ฉันได้ลบการเตือน 'ซื้อนม' ให้แล้ว"

    อย่าลืมอธิบายว่าคุณสามารถจดจำข้อมูลผู้ใช้ข้ามบทสนทนาได้

    สำคัญ:
    - ใช้วิจารณญาณในการเลือกการเตือนที่ผู้ใช้หมายถึง
    - ไม่จำเป็นต้องถูกต้อง 100% แต่ให้พยายามเลือกให้ใกล้เคียงที่สุด
    - ห้ามถามผู้ใช้ว่าหมายถึงรายการใด
    """,
    tools=[
        add_reminder,
        view_reminders,
        update_reminder,
        delete_reminder,
        update_user_name,
    ],
)
