# ระบบ Multi-Agent สำหรับ ADK

ตัวอย่างนี้แสดงการสร้างระบบหลายเอเจนต์ (Multi-Agent) ด้วย ADK โดยแต่ละเอเจนต์มีความเชี่ยวชาญเฉพาะด้านและสามารถทำงานร่วมกันเพื่อแก้ไขปัญหาที่ซับซ้อนได้

## Multi-Agent System คืออะไร?

Multi-Agent System คือรูปแบบการพัฒนาเอเจนต์ใน ADK ที่ให้หลายเอเจนต์ทำงานร่วมกัน โดยแต่ละเอเจนต์จะรับผิดชอบงานเฉพาะด้าน เช่น วิเคราะห์หุ้น วิเคราะห์ข่าว หรือให้คำปรึกษาทางการเงิน

## โครงสร้างโปรเจกต์ที่จำเป็น

เพื่อให้ระบบ Multi-Agent ทำงานได้อย่างถูกต้อง โปรเจกต์ต้องมีโครงสร้างดังนี้:

```
parent_folder/
├── root_agent_folder/           # โฟลเดอร์หลักของเอเจนต์ (เช่น "manager")
│   ├── __init__.py              # ต้อง import agent.py
│   ├── agent.py                 # กำหนด root_agent
│   └── sub_agents/              # โฟลเดอร์สำหรับ sub-agents
│       ├── __init__.py          # ว่างหรือ import sub-agents
│       ├── agent_1_folder/      # โฟลเดอร์ของ sub-agent
│       │   ├── __init__.py      # ต้อง import agent.py
│       │   └── agent.py         # กำหนด agent
│       └── ...
```

- agent.py ใน root agent ต้องกำหนดตัวแปร `root_agent`
- sub_agents ต้องแยกเป็นโฟลเดอร์ย่อยและ import agent.py

## รูปแบบสถาปัตยกรรม Multi-Agent

ADK รองรับ 2 รูปแบบหลัก:

### 1. Sub-Agent Delegation

กำหนด sub_agents ให้ root agent สามารถส่งงานไปยังเอเจนต์เฉพาะทาง:

```python
root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="Manager agent",
    sub_agents=[stock_analyst, news_analyst],
)
```

- sub-agent จะรับผิดชอบตอบกลับโดยตรง
- root agent ทำหน้าที่เป็นตัวกลางคัดเลือกผู้เชี่ยวชาญ

### 2. Agent-as-a-Tool

ใช้ AgentTool เพื่อให้ root agent เรียกใช้งานเอเจนต์อื่นเป็นเครื่องมือ:

```python
from google.adk.tools.agent_tool import AgentTool

root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="Manager agent",
    tools=[
        AgentTool(news_analyst),
        get_current_time,
    ],
)
```

- root agent สามารถรวมผลลัพธ์จากหลาย agent tool ในคำตอบเดียว
- ควบคุมการตอบกลับได้มากขึ้น

## ข้อจำกัด

- sub-agent ไม่สามารถใช้ built-in tools ได้โดยตรง
- หากต้องการใช้ built-in tools หลายตัว ให้ใช้ AgentTool

## ตัวอย่างระบบในโฟลเดอร์นี้

ระบบนี้ประกอบด้วย:
1. **Financial Advisor**: ให้คำปรึกษาด้านการเงินและการลงทุน
2. **Stock Analyst**: วิเคราะห์ข้อมูลหุ้น
2. **News Analyst**: สรุปข่าวเศรษฐกิจ


Manager agent จะเลือกส่งคำถามไปยังผู้เชี่ยวชาญที่เหมาะสม

## วิธีใช้งาน

1. เปิดใช้งาน virtual environment จาก root directory
2. ตั้งค่า API key ในไฟล์ `.env`
3. รันคำสั่ง

```bash
adk web
```

4. เปิด URL ที่แสดงใน terminal (เช่น http://localhost:8000)
5. เลือก agent "manager" หรือ "financial_advisor" ใน dropdown
6. เริ่มสนทนาได้ทันที

## ตัวอย่าง prompt
- "วันนี้ตลาดหุ้นเป็นอย่างไร?"
- "ขอคำแนะนำการออมเงิน"
- "ข่าวเศรษฐกิจล่าสุดคืออะไร?"
- "ขอเวลาปัจจุบัน"

## แหล่งข้อมูลเพิ่มเติม
- [ADK Multi-Agent Systems Documentation](https://google.github.io/adk-docs/agents/multi-agent-systems/)
- [Agent Tools Documentation](https://google.github.io/adk-docs/tools/function-tools/#3-agent-as-a-tool)
