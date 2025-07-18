from datetime import datetime

import yfinance as yf
from google.adk.agents import Agent


def get_stock_price(ticker: str) -> dict:
    """Retrieves current stock price and saves to session state."""
    print(f"--- Tool: get_stock_price called for {ticker} ---")

    try:
        # Fetch stock data
        stock = yf.Ticker(ticker)
        current_price = stock.info.get("currentPrice")

        if current_price is None:
            return {
                "status": "error",
                "error_message": f"Could not fetch price for {ticker}",
            }

        # Get current timestamp
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return {
            "status": "success",
            "ticker": ticker,
            "price": current_price,
            "timestamp": current_time,
        }

    except Exception as e:
        return {
            "status": "error",
            "error_message": f"Error fetching stock data: {str(e)}",
        }


# Create the root agent
stock_analyst = Agent(
    name="stock_analyst",
    model="gemini-2.0-flash",
    description="ตัวแทนที่สามารถค้นหาราคาหุ้นและติดตามราคาได้ตามช่วงเวลา",
    instruction="""
    คุณเป็นผู้ช่วยด้านตลาดหุ้นที่ช่วยผู้ใช้ติดตามหุ้นที่สนใจ

    เมื่อถูกถามเกี่ยวกับราคาหุ้น:
    1. ใช้เครื่องมือ get_stock_price เพื่อดึงราคาหุ้นล่าสุดของหุ้นที่ผู้ใช้ต้องการ
    2. จัดรูปแบบคำตอบเพื่อแสดงราคาปัจจุบันของแต่ละหุ้นและเวลาที่ดึงข้อมูล
    3. หากไม่สามารถดึงราคาหุ้นได้ ให้แจ้งในคำตอบ

    ตัวอย่างรูปแบบคำตอบ:
    "นี่คือราคาปัจจุบันของหุ้นที่คุณสนใจ:
    - GOOG: $175.34 (อัปเดตเมื่อ 2025-04-21 16:30:00)
    - TSLA: $156.78 (อัปเดตเมื่อ 2025-04-21 16:30:00)
    - META: $123.45 (อัปเดตเมื่อ 2025-04-21 16:30:00)"
    """,
    tools=[get_stock_price],
)
