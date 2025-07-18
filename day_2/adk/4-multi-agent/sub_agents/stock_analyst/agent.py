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


# สร้าง agent สำหรับวิเคราะห์หุ้น
stock_analyst = Agent(
    name="stock_analyst",
    model="gemini-2.0-flash",
    description="Agent สำหรับดูราคาหุ้นและติดตามข้อมูลหุ้น",
    instruction="""
    คุณคือผู้ช่วยวิเคราะห์หุ้นที่ช่วยผู้ใช้ติดตามราคาหุ้นที่สนใจ
    เมื่อมีคำถามเกี่ยวกับราคาหุ้น:
    1. ใช้เครื่องมือ get_stock_price เพื่อดึงข้อมูลราคาหุ้นล่าสุด
    2. จัดรูปแบบคำตอบให้แสดงราคาหุ้นแต่ละตัวพร้อมเวลาที่อัปเดต
    3. หากไม่สามารถดึงราคาหุ้นได้ ให้แจ้งในคำตอบ
    ตัวอย่างรูปแบบคำตอบ:
    "นี่คือราคาหุ้นล่าสุดที่คุณสนใจ:
    - GOOG: 175.34 USD (อัปเดตเมื่อ 2024-04-21 16:30:00)
    - TSLA: 156.78 USD (อัปเดตเมื่อ 2024-04-21 16:30:00)
    - META: 123.45 USD (อัปเดตเมื่อ 2024-04-21 16:30:00)"
    กรุณาตอบกลับเป็นภาษาไทยเสมอ
    """,
    tools=[get_stock_price],
)
