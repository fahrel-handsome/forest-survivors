import pygame

def load_spritesheet(path, frame_width, frame_height, scale=1):
    """
    Memuat spritesheet berbasis grid (baris x kolom).

    Digunakan untuk:
    - Animasi sederhana
    - Spritesheet dengan ukuran frame seragam
    """

    sheet = pygame.image.load(path).convert_alpha()
    sheet_w, sheet_h = sheet.get_size()

    frames = []
    rows = sheet_h // frame_height
    cols = sheet_w // frame_width

    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x * frame_width, y * frame_height, frame_width, frame_height)
            frame = sheet.subsurface(rect)
            frame = pygame.transform.scale(
                frame, (frame_width * scale, frame_height * scale)
            )
            frames.append(frame)

    return frames


# ==========================================================
# ATTACK SPRITESHEET (FRAME WIDTH TIDAK SERAGAM)
# ==========================================================
def load_attack_frames(path):

    """
    Loader khusus untuk animasi attack.

    Karakteristik:
    - Setiap frame memiliki lebar berbeda
    - Frame dipisahkan oleh area kosong (transparan)

    Teknik:
    1. Deteksi kolom yang berisi pixel (non-transparan)
    2. Crop frame secara dinamis
    3. Pad semua frame ke lebar yang sama

    Tujuan:
    - Mencegah kaki / posisi sprite bergeser saat animasi
    """

    sheet = pygame.image.load(path).convert_alpha()
    w, h = sheet.get_width(), sheet.get_height()

    # ============================
    # 1. DETEKSI SEGMENT FRAME
    # ============================
    segments = []
    started = False
    start = 0

    for x in range(w):
        column = sheet.subsurface((x, 0, 1, h))
        if column.get_bounding_rect() != pygame.Rect(0,0,0,0):
            if not started:
                start = x
                started = True
        else:
            if started:
                segments.append((start, x))
                started = False
    if started:
        segments.append((start, w))

    frames = []

    # ============================
    # 2. CROP TIAP FRAME
    # ============================
    raw_frames = []
    max_width = 0

    for (a, b) in segments:
        frame = sheet.subsurface((a, 0, b - a, h)).copy()
        frame = frame.subsurface(frame.get_bounding_rect())  # crop kosong
        raw_frames.append(frame)
        max_width = max(max_width, frame.get_width())

    # ============================
    # 3. PAD KE UKURAN SERAGAM
    # ============================
    for frame in raw_frames:
        surface = pygame.Surface((max_width, h), pygame.SRCALPHA)
        # center-bottom align biar kaki tidak geser
        x = (max_width - frame.get_width()) // 2
        y = h - frame.get_height()
        surface.blit(frame, (x, y))
        frames.append(surface)

    return frames

# ==========================================================
# STABLE SPRITESHEET LOADER (TIDAK CROP)
# ==========================================================
def load_spritesheet_stable(path, frame_width, frame_height, scale=1):
    """
    Loader spritesheet versi stabil.

    Ciri utama:
    - Tidak melakukan cropping
    - Setiap frame memiliki ukuran identik
    - Posisi sprite konsisten di semua frame

    Digunakan untuk:
    - Enemy movement (slime, skeleton)
    - Animasi looping
    - Hitbox yang harus stabil

    Alasan dibuat:
    - Menghindari bug collision & jitter visual
    """

    sheet = pygame.image.load(path).convert_alpha()
    sheet_w, sheet_h = sheet.get_size()

    rows = sheet_h // frame_height
    cols = sheet_w // frame_width

    frames = []

    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(
                x * frame_width,
                y * frame_height,
                frame_width,
                frame_height
            )

            # ambil tile exact tanpa cropping
            frame = sheet.subsurface(rect).copy()

            # scale konsisten
            if scale != 1:
                frame = pygame.transform.scale(
                    frame, (frame_width * scale, frame_height * scale)
                )

            frames.append(frame)

    return frames