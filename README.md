# Forest Survivors — README

Deskripsi singkat

Forest Survivors adalah game sederhana 2D top-down buatan Python (Pygame) untuk tugas akhir mata kuliah Pemrograman Berbasis Objek. README ini berisi cara menjalankan, penjelasan struktur proyek, serta ringkasan fungsi dan kelas utama untuk memudahkan pembelajaran dan pengembangan lebih lanjut.

Persyaratan

- Python 3.8+
- Pygame (versi yang kompatibel)

Instalasi

1. (Opsional) Buat virtual environment:

```bash
python -m venv venv
venv\Scripts\activate
```

2. Instal dependensi:

```bash
pip install pygame
```

Menjalankan game

Di folder proyek, jalankan:

```bash
python main.py
```

Kontrol dasar (umum)

- Panah / WASD: Gerakkan pemain
- Spasi / tombol aksi: Serang / Interaksi

Struktur proyek (ringkas)

- [main.py](main.py): Entrypoint aplikasi; inisialisasi Pygame dan loop utama.
- [core/game.py](core/game.py): Logika game utama, update loop, manajemen entitas dan rendering.
- [core/settings.py](core/settings.py): Konfigurasi (resolusi, fps, tile size, dsb.).
- [core/camera.py](core/camera.py): Kamera untuk mengikuti pemain dan mengubah koordinat render.
- [core/spritesheet_loader.py](core/spritesheet_loader.py): Utilitas memuat sprite sheet.
- [entities/](entities/): Kelas entitas game seperti `player`, `slime`, `skeleton`, `bomb`, dll.
  - [entities/player.py](entities/player.py): Logika pemain (gerak, animasi, input).
  - [entities/slime.py](entities/slime.py): Contoh musuh dengan perilaku sederhana.
  - [entities/bomb.py](entities/bomb.py): Objek bom dan interaksinya.
- [world/map_loader.py](world/map_loader.py): Memuat peta (Tiled .tmx) dan menyiapkan layer/lokasi spawn.
- [assets/](assets/): Berisi suara, font, tilesets, peta, dan sprite.

Penjelasan kode — poin penting per modul

1. `main.py`
- Inisialisasi Pygame, membuat instance `Game` dari `core/game.py`, dan menjalankan loop utama.

2. `core/game.py`
- Bertanggung jawab atas:
  - Menjalankan loop `while running` (handle events, update, draw).
  - Memuat world dan entitas melalui `map_loader` dan modul entitas.
  - Mengelola grup sprite (mis. Pygame `Sprite` groups) dan urutan render.
- Fungsi/pola umum: `update()` memanggil update tiap entitas; `draw()` merender world lalu entitas.

3. `core/settings.py`
- Menyimpan konstanta global seperti `WIDTH`, `HEIGHT`, `FPS`, `TILE_SIZE`.
- Gunakan untuk menyesuaikan tampilan dan perilaku tanpa mengubah banyak file.

4. `core/camera.py`
- Kamera biasanya menyimpan offset (x, y) berdasarkan posisi target (pemain).
- Saat merender, posisi world dikurangi offset kamera sehingga pemain tampak di tengah layar.

5. `core/spritesheet_loader.py`
- Fungsi utilitas untuk memotong gambar sprite sheet menjadi frame-frame animasi.
- Biasanya menyediakan method `get_image(x, y, width, height)` atau `load_strip(...)`.

6. `world/map_loader.py`
- Memuat file Tiled (`.tmx`) menggunakan library seperti `pytmx` (jika digunakan),
  lalu membuat surface untuk layer, mengekstrak objek spawn, collision, dan properti lain.
- Menghasilkan data tile dan posisi entitas berdasarkan object layer.

7. `entities/player.py` (ringkas)
- Kelas `Player(pygame.sprite.Sprite)` menangani:
  - Input dari keyboard.
  - Perhitungan vektor gerak dan deteksi tabrakan (collision) dengan world dan musuh.
  - Pemicu animasi berdasarkan state (idle, walk, attack).
- Pisahkan logika update, input handling, dan rendering/animasi untuk keterbacaan.

8. Entitas musuh & objek (slime, skeleton, bomb, pickup)
- Setiap entitas mengikuti pola Sprite Pygame: implementasi `update()` dan atribut `rect`.
- Musuh sederhana sering menggunakan state machine kecil (patrol, chase, attack).
- Bom menggunakan timer untuk meledak dan memberi damage di radius tertentu.

Panduan belajar / pengembangan

- Mulai dari `main.py` → buka `core/game.py` → telusuri bagaimana peta dimuat (`world/map_loader.py`).
- Lihat `entities/player.py` untuk memahami input, gerak, dan animasi.
- Untuk menambahkan fitur baru (mis. item, musuh): buat kelas baru di `entities/`, daftarkan spawn di editor peta, lalu muat di `map_loader`.

Tips debugging

- Cetak posisi pemain dan offset kamera jika tampilan tidak mengikuti pemain.
- Jika sprite tidak muncul, periksa path di `assets/` dan pemotongan frame di `spritesheet_loader`.
- Periksa layer collision pada file `.tmx` jika pemain bisa berjalan di area yang seharusnya terblokir.

Kontribusi

Jika ingin mengembangkan lebih lanjut:
- Buat branch baru untuk fitur/bugfix.
- Tambah dokumentasi singkat pada modul yang diubah.

Lisensi

Gunakan sesuai kebutuhan tugas/pendidikan; jika akan dipublikasikan, tambahkan lisensi yang sesuai.

--

Jika mau, saya bisa:
- Menambahkan contoh screenshot atau GIF ke `README.md`.
- Menjelaskan file tertentu lebih mendetail (mis. `entities/player.py`) dengan potongan kode.
- Membuat `requirements.txt` otomatis berisi `pygame`.

Beritahu saya opsi mana yang Anda inginkan selanjutnya.

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