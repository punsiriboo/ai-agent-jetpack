#  การสร้าง AI Chatbot ด้วย Gemini และ LINE Messaging API

## LAB3: เชื่อมต่อ LINE เข้ากับ Gemini
1. ไปยังไดเรกทอรีของโปรเจกต์:
   ```bash
   cd 3_gemini-x-line
   ```

2. ติดตั้ง dependency ที่จำเป็น:
   ```bash
   pip install -r requirements.txt
   ```

3. ตั้งค่าตัวแปรสภาพแวดล้อม (environment variables):
- คัดลอกไฟล์ตัวอย่าง environment:
    ```bash
    cp .env.example .env
    ```
- เปิดไฟล์ `.env` และอัปเดตด้วยค่าการกำหนดค่าของคุณ:
    ```
      LINE_CHANNEL_ID="your_channel_id"
      LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token
      LINE_CHANNEL_SECRET=your_channel_secret
      LINE_USER_ID=your_user_id
      GEMINI_API_KEY=your_gemini_api_key
    ```