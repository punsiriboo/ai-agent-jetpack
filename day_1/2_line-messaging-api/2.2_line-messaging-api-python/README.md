# [R2GAI] การสร้าง AI Agent ด้วย Gemini และ LINE Messaging API

1. ไปยังไดเรกทอรีของโปรเจกต์:
   ```bash
   cd 2.2_line-messaging-api-python
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
    LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
    LINE_CHANNEL_SECRET=your_line_channel_secret
    LINE_USER_ID=your_line_user_id
    ```
