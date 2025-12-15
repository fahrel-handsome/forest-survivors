# Forest Survivors
Top-Down Action RPG Game using Python & Pygame

Forest Survivors adalah game 2D **Top-Down Action RPG** yang dikembangkan menggunakan **Python** dan **Pygame**. Game ini dibuat sebagai project pembelajaran untuk menerapkan konsep **Object Oriented Programming (OOP)** dalam pengembangan game interaktif.

---

## Gameplay Overview
Pemain mengendalikan karakter utama dari sudut pandang atas (top-down) dan harus bertahan hidup dari serangan musuh yang terus muncul di arena permainan. Pemain dapat bergerak, menyerang musuh menggunakan pedang, melempar bom, serta mengambil item makanan untuk memulihkan HP.

---

## Fitur Utama
- Top-down movement (W, A, S, D)
- Serangan pedang (melee attack)
- Serangan bom (area damage)
- Dua tipe monster dengan perilaku berbeda
- Musuh spawn secara berkala
- Sistem HP (3 nyawa)
- Item pemulihan HP (ayam goreng dan semangka)
- Sistem score
- UI sederhana (HP dan score)

---

## Kontrol Game
| Tombol | Fungsi |
|------|------|
| W, A, S, D | Menggerakkan player |
| Space | Serangan pedang |
| E | Melempar bom |
| Shift | Lari cepat |

---

## Object Oriented Programming (OOP)
Game ini dirancang menggunakan pendekatan **Object Oriented Programming** agar struktur kode lebih rapi dan mudah dikembangkan.

- **Encapsulation**  
  Setiap entitas game seperti player, enemy, item, dan UI dibungkus dalam class masing-masing yang menyimpan data dan method terkait.

- **Inheritance**  
  Digunakan untuk membuat beberapa tipe monster dari satu class dasar sehingga mengurangi duplikasi kode.

- **Polymorphism**  
  Method seperti `update()` dan `draw()` digunakan oleh berbagai objek game dengan perilaku yang berbeda sesuai class masing-masing.

- **List / Collection**  
  Struktur data list digunakan untuk mengelola banyak objek game seperti musuh, bom, dan item secara dinamis di dalam game loop.

---

## 🗂️ Struktur Project
forest-survivors/
├── main.py
├── README.md
├── requirements.txt
├── assets/
│   ├── audio/
│   ├── enemy/
│   ├── font/
│   ├── food/
│   ├── maps/
│   │   └── mainMap.tmx
│   └── tilesets/
│       ├── TX Plant.tsx
│       ├── TX Props.tsx
│       ├── TX Shadow Plant.tsx
│       ├── TX Shadow.tsx
│       ├── TX Struct.tsx
│       ├── TX Tileset Grass.tsx
│       ├── TX Tileset Stone Ground.tsx
│       └── TX Tileset Wall.tsx
├── player/
├── ui/
├── core/
│   ├── camera.py
│   ├── game.py
│   ├── settings.py
│   └── spritesheet_loader.py
├── entities/
│   ├── __init__.py
│   ├── base_entity.py
│   ├── bomb.py
│   ├── BombPickup.py
│   ├── health.py
│   ├── player.py
│   ├── skeleton.py
│   ├── slime.py
│   └── thrown_bomb.py
└── world/
  ├── __init__.py
  └── map_loader.py

---

## ▶️ Cara Menjalankan Game
1. Pastikan Python sudah terinstall
2. Install Pygame:
   ```bash
   pip install pygame
3. Jalankan game nya:
   ```bash
   python main.py
