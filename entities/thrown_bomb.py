import pygame
import math
from entities.base_entity import BaseEntity

class ThrownBomb(BaseEntity):

    """
    ThrownBomb
    ----------
    Bomb yang sudah dilempar oleh player.

    Tanggung jawab:
    - bergerak lurus
    - menunggu fuse time
    - menampilkan animasi ledakan
    - memberi damage area (AOE)

    Kelas ini terpisah dari BombPickup
    untuk menjaga Single Responsibility.
    """

    def __init__(self, x, y, direction):
        super().__init__(x, y)

        # =========================
        # VISUAL & HITBOX
        # =========================
        self.image = pygame.image.load("assets/bomb.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = self.rect.copy()

        # bomb lurus
        self.vel_x = 150 * direction
        self.vel_y = 0

        # timer
        self.timer = 0
        self.explode_time = 1.2

        # =========================
        # LOAD EXPLOSION SPRITESHEET
        # =========================
        sheet = pygame.image.load("assets/explosion.png").convert_alpha()

        # tinggi frame = tinggi image
        frame_h = sheet.get_height()

        # lebar frame = tinggi (karena per frame itu kotak)
        frame_w = frame_h

        self.explosion_frames = []

        for i in range(6):
            frame = sheet.subsurface(pygame.Rect(i * frame_w, 0, frame_w, frame_h))
            self.explosion_frames.append(frame)

        # =========================
        # EXPLOSION STATE
        # =========================
        self.exploding = False
        self.explosion_index = 0
        self.explosion_speed = 0.07     # kecepatan animasi
        self.explosion_timer = 0

        # ukuran ledakan (scale visual)
        self.explosion_scale = 3

    # ============================================================
    # UPDATE
    # ============================================================
    def update(self, dt):
        """
        Update perilaku bomb:
        - Mode normal   : bergerak + hitung fuse
        - Mode ledakan  : animasi explosion
        """

        # =========================
        # MODE NORMAL (TERBANG)
        # =========================
        if not self.exploding:

            self.rect.x += self.vel_x * dt
            self.hitbox.center = self.rect.center

            self.timer += dt
            if self.timer >= self.explode_time:
                self.start_explode()

            return

        # =========================
        # MODE LEDAKAN
        # =========================
        self.explosion_timer += dt

        if self.explosion_timer >= self.explosion_speed:
            self.explosion_timer = 0
            self.explosion_index += 1

            if self.explosion_index >= len(self.explosion_frames):
                from core.game import Game
                Game.instance.bomb_available = True
                self.kill()
                return

            # update frame ledakan dengan scale
            center = self.rect.center
            frame = self.explosion_frames[self.explosion_index]

            scale = self.explosion_scale
            frame_big = pygame.transform.scale(
                frame,
                (frame.get_width() * scale, frame.get_height() * scale)
            )

            self.image = frame_big
            self.rect = self.image.get_rect(center=center)

    # ============================================================
    # START EXPLOSION
    # ============================================================
    def start_explode(self):
        """Memulai ledakan bomb dan memberi damage area"""
        if self.exploding:
            return

        self.exploding = True
        self.explosion_timer = 0
        self.explosion_index = 0

        # set frame awal ledakan
        center = self.rect.center
        self.image = self.explosion_frames[0]
        self.rect = self.image.get_rect(center=center)

        print("BOOM!")

        # =========================
        # DAMAGE AREA (AOE)
        # =========================
        DAMAGE_RADIUS = 90  # radius ledakan

        from core.game import Game

        # Loop semua enemy
        for enemy in list(Game.instance.enemies):

            # Ambil posisi musuh
            ex, ey = enemy.rect.center

            # hitung jarak
            dist = math.hypot(
                ex - self.rect.centerx,
                ey - self.rect.centery
            )

            if dist <= DAMAGE_RADIUS:
                enemy.take_damage(1)   # atau damage bom