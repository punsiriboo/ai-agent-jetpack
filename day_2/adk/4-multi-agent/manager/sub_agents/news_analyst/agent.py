from google.adk.agents import Agent
from google.adk.tools import google_search

# ตัวแทนนี้ช่วยวิเคราะห์ข่าวและสรุปข่าวให้ผู้ใช้

news_analyst = Agent(
    name="news_analyst",
    model="gemini-2.0-flash",
    description="News analyst agent",
    instruction="""
    คุณเป็นผู้ช่วยที่สามารถวิเคราะห์บทความข่าวและสรุปข่าวให้กับผู้ใช้ได้

    เมื่อถูกถามเกี่ยวกับข่าว คุณควรใช้เครื่องมือ google_search เพื่อค้นหาข่าว

    หากผู้ใช้ถามข่าวโดยใช้เวลาสัมพัทธ์ คุณควรใช้เครื่องมือ get_current_time เพื่อรับเวลาปัจจุบันสำหรับใช้ในการค้นหา
    """,
    tools=[google_search],
)
