
## โฟลเดอร์ n8n Integration

โฟลเดอร์นี้ประกอบด้วยทรัพยากรและสคริปต์สำหรับการเชื่อมต่อ n8n ซึ่งเป็นเครื่องมือโอเพ่นซอร์สสำหรับการทำงานอัตโนมัติ กับโปรเจกต์ AI agent คุณจะพบไฟล์คอนฟิก ตัวอย่าง workflow และสคริปต์อรรถประโยชน์สำหรับช่วยให้งานอัตโนมัติและเชื่อมต่อบริการต่าง ๆ ได้ง่ายขึ้น

### โครงสร้างโฟลเดอร์

- **docker-compose.yaml**: ไฟล์ Docker Compose สำหรับติดตั้ง n8n และบริการที่เกี่ยวข้อง
- **instruction-promps.txt**: ตัวอย่าง prompt และคำแนะนำสำหรับ workflow automation
- **nginx.conf**: ไฟล์คอนฟิก NGINX สำหรับ reverse proxy n8n หรือบริการที่เกี่ยวข้อง
- **scripts/**: สคริปต์ shell สำหรับจัดการ container n8n (เช่น `compose_up.sh`, `compose_down.sh`)
- **workflow-results/**: ผลลัพธ์และ log จาก workflow ที่รันแล้ว
- **workflows/**: ตัวอย่างไฟล์ workflow JSON สำหรับ n8n ในสถานการณ์อัตโนมัติต่าง ๆ

### วิธีเริ่มต้นใช้งาน

1. ตรวจสอบไฟล์ `docker-compose.yaml` และปรับ environment variables ตามต้องการ
2. ใช้สคริปต์ในโฟลเดอร์ `scripts/` เพื่อเริ่มหรือหยุดบริการ docker ของ n8n
3. workflow ตัวอย่างจากโฟลเดอร์ `workflows/` สามารถนำไปใช้ บน n8n instance ของคุณ
4. ดู `instruction-promps.txt` เพื่อไอเดียและเทมเพลตสำหรับสร้าง AI Agent ของคุณเอง

### แหล่งข้อมูลเพิ่มเติม

- [เอกสาร n8n](https://docs.n8n.io/)
- [n8n GitHub](https://github.com/n8n-io/n8n)


