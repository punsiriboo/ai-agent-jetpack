from google.adk.agents import Agent

# Create the root agent
root_agent = Agent(
    name="question_answering_agent",
    model="gemini-2.0-flash",
    description="Question answering agent",
    instruction="""
    คุณคือน้องเนโกะ ผู้ช่วยแมวสุดน่ารักที่คอยช่วยค้นหาข้อมูลและตอบคำถามเกี่ยวกับความชอบของผู้ใช้

    นี่คือข้อมูลเกี่ยวกับผู้ใช้:
    ชื่อ: 
    {user_name}
    ความชอบ: 
    {user_preferences}
    """,
)
