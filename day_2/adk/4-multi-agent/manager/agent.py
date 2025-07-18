from google.adk.agents import Agent
from google.adk.tools.agent_tool import AgentTool

from .sub_agents.funny_nerd.agent import funny_nerd
from .sub_agents.news_analyst.agent import news_analyst
from .sub_agents.stock_analyst.agent import stock_analyst
from .tools.tools import get_current_time

# ตัวแทนนี้เป็นผู้จัดการที่คอยดูแลและมอบหมายงานให้กับตัวแทนอื่น ๆ

root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="ตัวแทนผู้จัดการ ชื่อ น้อง Neko",
    instruction="""
    คุณเป็นตัวแทนผู้จัดการที่รับผิดชอบในการดูแลและควบคุมการทำงานของตัวแทนอื่น ๆ
    เมื่อทักทาย คุณจะต้องแนะนำตัวเองและอธิบายหน้าที่ของคุณให้ชัดเจน
    คุณต้องมอบหมายงานให้กับตัวแทนที่เหมาะสมเสมอ โดยใช้วิจารณญาณของคุณในการเลือกตัวแทนที่ควรมอบหมายงาน

    คุณรับผิดชอบในการมอบหมายงานให้กับตัวแทนดังต่อไปนี้:
    - stock_analyst
    - funny_nerd

    คุณยังสามารถเข้าถึงเครื่องมือดังต่อไปนี้:
    - news_analyst
    - get_current_time
    """,
    sub_agents=[stock_analyst, funny_nerd],
    tools=[
        AgentTool(news_analyst),
        get_current_time,
    ],
)
