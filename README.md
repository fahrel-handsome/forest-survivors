# Forest Survivors — README

Deskripsi

Forest Survivors adalah game 2D top-down sederhana yang dibuat dengan Python dan Pygame untuk tugas akhir. Dokumentasi ini dibuat supaya teman-teman bisa cepat menjalankan game, memahami struktur proyek, dan tahu di mana mencari logika utama.

Persyaratan

- Python 3.8 atau lebih baru
- pygame

Instalasi

1. (Opsional) Buat virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Instal dependensi:

```bash
pip install -r requirements.txt
```

Menjalankan game

Jalankan perintah ini di folder proyek:

```bash
python main.py
```

Kontrol dasar

- WASD / Panah: bergerak
- Spasi: aksi/serang (tergantung implementasi)

Struktur proyek (singkat)

- `main.py`: titik masuk, inisialisasi Pygame dan loop utama.
- `core/game.py`: logika game, loop update/draw, manajemen grup sprite.
- `core/settings.py`: pengaturan seperti resolusi, FPS, ukuran tile.
- `core/camera.py`: menghitung offset kamera untuk rendering.
- `core/spritesheet_loader.py`: utilitas memotong sprite sheet menjadi frame animasi.
- `world/map_loader.py`: memuat file `.tmx` (Tiled), mengolah layer, spawn, dan collision.
- `entities/`: berisi entitas game (pemain, musuh, item, bom, dll.).
- `assets/`: sprites, tilesets, peta, suara, font.

Penjelasan singkat per modul

1. `main.py`
- Membuat objek `Game` (dari `core/game.py`) dan menjalankan loop utama.

2. `core/game.py`
- Mengatur event handling, update semua entitas, dan rendering.
- Mengelola grup sprite dan urutan gambar agar draw berjalan benar.

3. `core/settings.py`
- Menyimpan konstanta agar mudah dikonfigurasi.

4. `core/camera.py`
- Menyimpan offset berdasarkan posisi pemain sehingga tampilan mengikuti pemain.

5. `core/spritesheet_loader.py`
- Berisi fungsi untuk memotong sprite sheet dan mengambil frame animasi.

6. `world/map_loader.py`
- Memuat peta Tiled (`.tmx`), membaca objek spawn dan layer collision, lalu menyiapkan data untuk game.

7. `entities/*`
- Setiap file entitas biasanya turunan `pygame.sprite.Sprite` yang punya `update()` dan `rect`.

Penjelasan lebih detail: `entities/player.py`

- Kelas utama: `Player(pygame.sprite.Sprite)` — mengurus input, pergerakan, animasi, dan deteksi tabrakan.
- Inisialisasi: memuat frame animasi, mengatur `rect`, kecepatan, dan status seperti health.
- Metode penting: `handle_input()` untuk membaca keyboard, `move()` atau langsung ubah `rect` untuk berpindah, `update()` untuk menggabungkan input, gerak, dan animasi, serta fungsi collision tile.

Contoh pola sederhana:

```py
class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, spritesheet):
        super().__init__(groups)
        self.image = spritesheet.get_image(0,0,32,32)
        self.rect = self.image.get_rect(topleft=pos)
        self.vx, self.vy = 0, 0
        self.speed = 200

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vx = keys[pygame.K_d] - keys[pygame.K_a]
        self.vy = keys[pygame.K_s] - keys[pygame.K_w]

    def update(self, dt):
        self.handle_input()
        self.rect.x += self.vx * self.speed * dt
        self.rect.y += self.vy * self.speed * dt
        self.animate()
```

Tips singkat

- Gunakan `dt` (delta time) agar kecepatan gerak konsisten di semua frame rate.
- Pisahkan logika input, gerak, dan animasi supaya kode lebih rapi.
- Gunakan `rect`/`mask` untuk deteksi tabrakan.

Panduan cepat buat belajar kode

- Buka `main.py` dulu, lalu telusuri ke `core/game.py` untuk memahami loop utama.
- Lanjut ke `world/map_loader.py` untuk lihat bagaimana peta dan spawn dimuat.
- Untuk logika karakter, lihat `entities/player.py`.

Debugging umum

- Jika kamera tidak mengikuti pemain, cek posisi pemain dan offset kamera.
- Kalau sprite tidak muncul, cek path file di `assets/` dan pemotongan frame di `spritesheet_loader`.
- Periksa layer collision di `.tmx` bila pemain bisa melewati area yang seharusnya terblokir.

Opsi pengembangan

- Tambah musuh atau item baru dengan menambah file di `entities/` dan menandai spawn di editor peta.
- Tambah screenshot atau dokumentasi fungsi tertentu bila perlu.

Kontribusi

- Buat branch terpisah untuk fitur/bugfix dan tambahkan catatan singkat di commit.

Lisensi

Proyek ini dibuat untuk tugas/pembelajaran. Tambahkan lisensi jika ingin dipublikasikan.

**Penjelasan detail: `entities/player.py`**

- **Kelas utama:** `Player(pygame.sprite.Sprite)` — menangani input, gerak, animasi, dan collision.
- **Inisialisasi:** memuat image/animasi, mengatur `rect`, kecepatan, health, state.
- **Metode penting:** `handle_input()` memproses keyboard; `move(dx, dy)` mengubah posisi; `update()` menyatukan input->gerak->animasi; `check_collisions()` untuk tile collisions.
- **Contoh pola kode (singkat):**

```py
class Player(pygame.sprite.Sprite):
  def __init__(self, pos, groups, spritesheet):
    super().__init__(groups)
    self.image = spritesheet.get_image(0,0,32,32)
    self.rect = self.image.get_rect(topleft=pos)
    self.vx, self.vy = 0, 0
    self.speed = 200

  def handle_input(self):
    keys = pygame.key.get_pressed()
    self.vx = keys[pygame.K_d] - keys[pygame.K_a]
    self.vy = keys[pygame.K_s] - keys[pygame.K_w]

  def update(self, dt):
    self.handle_input()
    self.rect.x += self.vx * self.speed * dt
    self.rect.y += self.vy * self.speed * dt
    self.animate()
```

- **Tips implementasi:** gunakan `dt` (delta time) untuk gerak frame-rate independent; gunakan mask/rect untuk collision; simpan state (`'idle'`, `'walk'`, `'attack'`) untuk memilih animasi.

Jika ingin, saya bisa membuat penjelasan serupa untuk `entities/slime.py` atau menambahkan `requirements.txt` sekarang.