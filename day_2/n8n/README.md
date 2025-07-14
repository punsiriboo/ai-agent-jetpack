## ติดตั้ง n8n แบบ global ด้วย npm
ดูรายละเอียดการใช้งานเพิ่มเติมได้ที่เอกสารทางการของ n8n
อ้างอิง: https://docs.n8n.io/hosting/installation/npm/#try-n8n-with-npx

### 1. ติดตั้ง n8n
คำสั่งนี้ใช้สำหรับติดตั้ง n8n ทั่วไปในเครื่องของคุณผ่าน npm (Node Package Manager)
```
npm install n8n -g
```

### 2. สั่งเริ่มทำงาน Server n8n

```
n8n start --tunnel
```
### 3. (OPTIONAL)ลบข้อมูล n8n 
เช่น workflows, credentials, binary data, settings
```
rm -rf ~/.n8n
```

คำสั่งนี้ใช้สำหรับเริ่มต้น n8n พร้อมเปิดใช้งาน tunnel เพื่อให้สามารถเข้าถึง n8n ได้จากภายนอก เช่น Website หรือเรียนผ่าน Webhook
