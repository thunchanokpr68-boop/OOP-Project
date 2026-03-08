# 🃏 Emoji Flip Master: OOP Project

![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-orange?style=for-the-badge)

โปรเจกต์เกมจับคู่ภาพอีโมจิ 20 ระดับความยาก (20 Levels Challenge) พัฒนาด้วยภาษา Python และไลบรารี Pygame โดยเน้นการออกแบบสถาปัตยกรรมซอฟต์แวร์ตามหลัก **Object-Oriented Programming (OOP)** และ **Modularity** เพื่อให้โค้ดอ่านง่าย บำรุงรักษาได้ และสามารถนำไปต่อยอดได้ในอนาคต

---

## 📑 สารบัญ (Table of Contents)
1. [สมาชิกในทีม (Team Members)](#-สมาชิกในทีม-team-members)
2. [วิธีเล่นเกม (How to Play)](#-วิธีเล่นเกม-how-to-play)
3. [ฟีเจอร์เด่น (Key Features)](#-ฟีเจอร์เด่น-key-features)
4. [โครงสร้างสถาปัตยกรรม OOP (OOP Architecture)](#-โครงสร้างสถาปัตยกรรม-oop-oop-architecture)
5. [โครงสร้างไฟล์ (Project Structure)](#-โครงสร้างไฟล์-project-structure)
6. [การติดตั้งและรันโปรแกรม (Installation & Usage)](#-การติดตั้งและรันโปรแกรม-installation--usage)

---

## 👥 สมาชิกในทีม (Team Members)
**ชื่อทีม:** [ใส่ชื่อทีมของคุณที่นี่ เช่น ทีมนอนน้อยแต่นอนนะ]

| รหัสนักศึกษา | ชื่อ-นามสกุล | หน้าที่ความรับผิดชอบ (Responsibility) |
| :--- | :--- | :--- |
| 68114540540 | **นางสาวลลิดา ดิ้นทอง** | ออกแบบ Game Logic, พัฒนา `class Card`, ระบบแอนิเมชันพลิกไพ่ 3D |
| ` | **** | พัฒนา UI/UX, สร้าง `class Button`, ระบบ Particle Effect และการตั้งค่า Project |

---

## 🎮 วิธีเล่นเกม (How to Play)
1. ผู้เล่นจะต้องเปิดการ์ดเพื่อจับคู่อีโมจิที่เหมือนกันให้ครบ 8 คู่ (16 ใบ) ภายในเวลาที่กำหนด
2. **ความท้าทาย:** เกมมีทั้งหมด 20 ด่าน โดยยิ่งด่านสูงขึ้น เวลา (Time Limit) ที่ให้ในการจับคู่จะยิ่งลดน้อยลง
3. หากเปิดไพ่ผิด ไพ่จะคว่ำกลับไป หากเปิดถูก ไพ่จะหงายค้างไว้และมีเอฟเฟกต์ฉลองความสำเร็จ
4. ต้องจับคู่ให้ครบทุกใบก่อนเวลาจะหมด (Time Up) เพื่อปลดล็อกด่านต่อไป

---

## ✨ ฟีเจอร์เด่น (Key Features)
* **Progressive Difficulty:** ระบบคำนวณเวลาถอยหลังแบบไดนามิก `max(8, 45 - (level * 2))` เพื่อเพิ่มความกดดัน
* **3D Card Flip Animation:** ใช้ฟังก์ชันตรีโกณมิติ (`math.cos`) คำนวณความกว้างและมุมของการ์ดแบบเฟรมต่อเฟรม ทำให้เกิดภาพลวงตาแบบ 3 มิติขณะพลิกไพ่
* **State Machine Pattern:** ใช้การจัดการ State ของเกมที่ชัดเจน เช่น `START_MENU`, `LEVEL_SELECT`, `PLAYING`, `WON`, `GAMEOVER`
* **Particle Physics System:** ระบบจำลองเอฟเฟกต์อนุภาค (Particles) ที่มีการคำนวณทิศทางการกระจายแบบสุ่มและอายุขัย (Lifespan)
* **Configurable UI:** ระบบปุ่มกด (Button) ที่มี Hover Effect โต้ตอบกับเมาส์ของผู้เล่น

---

## 🧩 โครงสร้างสถาปัตยกรรม OOP (OOP Architecture)
โปรเจกต์นี้เขียนด้วยโครงสร้างแบบ Best Practice โดยประยุกต์ใช้หลักการเขียนโปรแกรมเชิงวัตถุอย่างลึกซึ้ง:

1. **Classes and Objects (คลาสและออบเจกต์):**
   * `Card`: ตัวแทนของการ์ดแต่ละใบ เก็บข้อมูลพิกัด (Rect), รูปอีโมจิ, และสถานะการเปิด/ปิด
   * `Button`: ออบเจกต์สำหรับสร้างปุ่ม UI พร้อมระบบตรวจจับการชนของเมาส์ (`collidepoint`)
   * `ParticleSystem`: คลาสจัดการเอฟเฟกต์ทั้งหมด (Creation & Updating)
   * `Game`: คลาสศูนย์กลาง (Game Manager) ที่ควบคุมลูปหลัก รวบรวมออบเจกต์อื่นๆ ไว้ด้วยกัน

2. **Encapsulation (การห่อหุ้มข้อมูล):**
   * ลอจิกการอัปเดตแอนิเมชันและรูปภาพถูกซ่อนไว้ในฟังก์ชัน `update()` และ `draw()` ของแต่ละคลาส 
   * ไฟล์ `main.py` ทำหน้าที่เพียงแค่สร้างออบเจกต์ `Game` และเรียกฟังก์ชันรัน ไม่ต้องรับรู้ความซับซ้อนของการคำนวณด้านใน

3. **Modularity (การแบ่งส่วนประกอบ):**
   * แยกโค้ดออกจากกันตามหน้าที่อย่างชัดเจน เช่น เก็บค่าคงที่ (สี, ตัวอักษร, ขนาดจอ) ไว้ใน `config.py` เพื่อให้แก้ไขได้ง่ายโดยไม่ต้องยุ่งกับระบบหลัก

---

## 📂 โครงสร้างไฟล์ (Project Structure)
```text
OOP-PROJECT/
├── src/                    # โฟลเดอร์เก็บ Source Code หลัก
│   ├── entities/           # ออบเจกต์ที่มีปฏิสัมพันธ์ในเกม
│   │   ├── __init__.py
│   │   └── card.py         # คลาสจัดการการ์ด
│   ├── systems/            # ระบบเสริมและ UI
│   │   ├── __init__.py
│   │   └── ui.py           # คลาสจัดการปุ่มและ Particle 
│   ├── __init__.py
│   └── game.py             # ระบบจัดการ Game State หลัก
├── assets/                 # โฟลเดอร์สำหรับทรัพยากร (รูป, เสียง)
├── config.py               # ตั้งค่าตัวแปรคงที่ (Constants)
├── main.py                 # ไฟล์เริ่มต้นรันโปรแกรม (Entry Point)
├── pyproject.toml          # ไฟล์คอนฟิกของแพ็กเกจ (uv)
└── requirements.txt        # รายการไลบรารีที่ต้องติดตั้ง