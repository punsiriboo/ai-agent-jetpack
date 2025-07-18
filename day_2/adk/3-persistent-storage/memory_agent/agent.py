
# นำเข้า Agent สำหรับสร้างผู้ช่วย และ ToolContext สำหรับจัดการข้อมูลสถานะ
from google.adk.agents import Agent
from google.adk.tools.tool_context import ToolContext



# ฟังก์ชันสำหรับเพิ่มรายการเตือนความจำใหม่
def add_reminder(reminder: str, tool_context: ToolContext) -> dict:
    """เพิ่มรายการเตือนความจำใหม่ให้กับผู้ใช้"""
    print(f"--- Tool: add_reminder called for '{reminder}' ---")

    # ดึงรายการเตือนความจำปัจจุบันจาก state
    reminders = tool_context.state.get("reminders", [])

    # เพิ่มรายการใหม่เข้าไป
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
    """แสดงรายการเตือนความจำทั้งหมด"""
    print("--- Tool: view_reminders called ---")

    # ดึงรายการเตือนความจำจาก state
    reminders = tool_context.state.get("reminders", [])

    return {"action": "view_reminders", "reminders": reminders, "count": len(reminders)}



# ฟังก์ชันสำหรับแก้ไขรายการเตือนความจำ
def update_reminder(index: int, updated_text: str, tool_context: ToolContext) -> dict:
    """แก้ไขข้อความในรายการเตือนความจำที่เลือก"""
    print(
        f"--- Tool: update_reminder called for index {index} with '{updated_text}' ---"
    )

    # ดึงรายการเตือนความจำจาก state
    reminders = tool_context.state.get("reminders", [])

    # ตรวจสอบ index ว่าถูกต้องหรือไม่
    if not reminders or index < 1 or index > len(reminders):
        return {
            "action": "update_reminder",
            "status": "error",
            "message": f"ไม่พบรายการเตือนที่ตำแหน่ง {index} ขณะนี้มี {len(reminders)} รายการเตือนความจำ",
        }

    # แก้ไขข้อความในรายการเตือน (index เริ่มที่ 1)
    old_reminder = reminders[index - 1]
    reminders[index - 1] = updated_text

    # อัปเดตรายการเตือนใน state
    tool_context.state["reminders"] = reminders

    return {
        "action": "update_reminder",
        "index": index,
        "old_text": old_reminder,
        "updated_text": updated_text,
        "message": f"แก้ไขรายการเตือน {index} จาก '{old_reminder}' เป็น '{updated_text}'",
    }



# ฟังก์ชันสำหรับลบรายการเตือนความจำ
def delete_reminder(index: int, tool_context: ToolContext) -> dict:
    """ลบรายการเตือนความจำที่เลือก"""
    print(f"--- Tool: delete_reminder called for index {index} ---")

    # ดึงรายการเตือนความจำจาก state
    reminders = tool_context.state.get("reminders", [])

    # ตรวจสอบ index ว่าถูกต้องหรือไม่
    if not reminders or index < 1 or index > len(reminders):
        return {
            "action": "delete_reminder",
            "status": "error",
            "message": f"ไม่พบรายการเตือนที่ตำแหน่ง {index} ขณะนี้มี {len(reminders)} รายการเตือนความจำ",
        }

    # ลบรายการเตือน (index เริ่มที่ 1)
    deleted_reminder = reminders.pop(index - 1)

    # อัปเดตรายการเตือนใน state
    tool_context.state["reminders"] = reminders

    return {
        "action": "delete_reminder",
        "index": index,
        "deleted_reminder": deleted_reminder,
        "message": f"ลบรายการเตือน {index}: '{deleted_reminder}'",
    }



# ฟังก์ชันสำหรับแก้ไขชื่อผู้ใช้
def update_user_name(name: str, tool_context: ToolContext) -> dict:
    """แก้ไขชื่อของผู้ใช้"""
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



# สร้าง Agent สำหรับจัดการเตือนความจำแบบ persistent
neko_agent = Agent(
    name="neko_agent",
    model="gemini-2.0-flash",
    description="น้อง Neko ผู้ช่วยเตือนความจำสุดน่ารักที่จดจำข้อมูลผู้ใช้ได้",
    instruction="""
    คุณคือน้อง Neko ผู้ช่วยเตือนความจำสุดน่ารักที่เป็นมิตรและสามารถจดจำข้อมูลผู้ใช้ได้ตลอดการสนทนา

    ข้อมูลของผู้ใช้จะถูกเก็บไว้ใน state:
    - ชื่อผู้ใช้: {user_name}
    - รายการเตือนความจำ: {reminders}

    คุณสามารถช่วยผู้ใช้จัดการรายการเตือนความจำได้ดังนี้:
    1. เพิ่มรายการเตือนใหม่
    2. ดูรายการเตือนที่มีอยู่
    3. แก้ไขรายการเตือน
    4. ลบรายการเตือน
    5. เปลี่ยนชื่อผู้ใช้

    ควรพูดคุยกับผู้ใช้อย่างเป็นมิตรและเรียกชื่อผู้ใช้ทุกครั้ง หากยังไม่ทราบชื่อให้ใช้เครื่องมือ update_user_name เพื่อบันทึกเมื่อผู้ใช้แนะนำตัว

    **แนวทางการจัดการรายการเตือนความจำ:**

    1. เมื่อผู้ใช้ขอแก้ไขหรือลบรายการเตือนโดยไม่ระบุหมายเลข:
       - หากมีการกล่าวถึงเนื้อหา ให้ค้นหารายการที่ตรงหรือใกล้เคียงที่สุด
       - หากพบ ให้ใช้ index นั้น
       - ไม่ต้องถามผู้ใช้เพื่อยืนยัน ให้ใช้รายการแรกที่ตรง
       - หากไม่พบ ให้แสดงรายการทั้งหมดและขอให้ผู้ใช้ระบุ

    2. เมื่อผู้ใช้ระบุหมายเลขหรือตำแหน่ง:
       - ใช้หมายเลขนั้นเป็น index (เช่น "ลบรายการเตือนหมายเลข 2" หมายถึง index=2)
       - จำไว้ว่าผู้ใช้เริ่มนับที่ 1

    3. ตำแหน่งสัมพัทธ์:
       - "รายการแรก" = index 1
       - "รายการสุดท้าย" = index สูงสุด
       - "รายการที่สอง" = index 2 เป็นต้น

    4. การดูรายการ:
       - ใช้ view_reminders เมื่อผู้ใช้ขอดูรายการเตือน
       - แสดงผลเป็นลำดับหมายเลขเพื่อความชัดเจน
       - หากไม่มีรายการ ให้แนะนำให้เพิ่ม

    5. การเพิ่ม:
       - ดึงข้อความเตือนจริงจากคำขอของผู้ใช้
       - ตัดคำว่า "เพิ่มรายการเตือน" หรือ "เตือนฉันให้" ออก
       - เน้นเฉพาะงานที่ต้องทำ เช่น "เพิ่มรายการเตือนซื้อของ" → add_reminder("ซื้อของ")

    6. การแก้ไข:
       - ระบุทั้งรายการที่จะแก้ไขและข้อความใหม่
       - เช่น "เปลี่ยนรายการที่สองเป็นรับของที่ร้าน" → update_reminder(2, "รับของที่ร้าน")

    7. การลบ:
       - ยืนยันการลบและแจ้งว่ารายการใดถูกลบ
       - เช่น "ลบรายการเตือน 'ซื้อของ' ให้แล้ว"

    อย่าลืมอธิบายว่าคุณสามารถจดจำข้อมูลผู้ใช้ได้ตลอดการสนทนา

    สำคัญ:
    - ใช้ดุลยพินิจในการเลือกว่าผู้ใช้หมายถึงรายการใด
    - ไม่จำเป็นต้องถูกต้อง 100% แต่ควรใกล้เคียงที่สุด
    - ไม่ต้องถามผู้ใช้เพื่อยืนยันรายการ
    """,
    tools=[
        add_reminder,
        view_reminders,
        update_reminder,
        delete_reminder,
        update_user_name,
    ],
)
