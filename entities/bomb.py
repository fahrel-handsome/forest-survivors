import pygame
import time

class Bomb(pygame.sprite.Sprite):
    """
    Bomb Entity
    -----------
    Bomb dapat:
    - ditempel ke player (pickup)
    - dilempar
    - meledak setelah fuse time

    Alur state:
    attached → thrown → exploded → destroy
    """

    def __init__(self, x, y):
        super().__init__()

        # =========================
        # LOAD IMAGE
        # =========================
        
        self.image_default = pygame.image.load("assets/bomb.png").convert_alpha()
        self.image_explosion = pygame.image.load("assets/explosion.png").convert_alpha()

        self.image = self.image_default
        self.rect = self.image.get_rect(center=(x, y))

        # =========================
        # STATE
        # =========================
        self.attached = False       # bomb menempel ke player
        self.thrown = False         # bomb sudah dilempar
        self.exploded = False       # bomb sudah meledak

        self.player = None          # referensi player (saat attached)

        # =========================
        # MOVEMENT
        # =========================
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.35

        # =========================
        # TIMER
        # =========================
        self._throw_start_time = 0
        self._explosion_start_time = 0
        self._throw_timer_started = False


        self.fuse_time = 1.0            # ledak setelah 1 detik dilempar
        self.explosion_duration = 0.25  # animasi ledakan

    # ============================================================
    # TIMER CONTROL
    # ============================================================
    def start_throw_timer(self):
        """Mulai timer saat bomb dilempar"""
        self._throw_start_time = time.time()

    def _start_explosion_timer(self):
        """Mulai timer animasi ledakan"""
        self._explosion_start_time = time.time()


    # ============================================================
    # UPDATE
    # ============================================================
    def update(self, dt):
        """
        Update bomb berdasarkan state:
        1. Attached  → mengikuti posisi player
        2. Thrown    → bergerak & menunggu ledakan
        3. Exploded  → tampil ledakan lalu dihapus
        """

        # ============================================================
        # 1. BOMB MASIH DITEMPEL KE PLAYER
        # ============================================================
        if self.attached and self.player:
            offset_x = 15
            offset_y = -10
            self.rect.centerx = self.player.rect.centerx + offset_x
            self.rect.centery = self.player.rect.centery + offset_y
            return

        # ============================================================
        # 2. BOMB TERLEMPAR (VISUAL TETAP ADA)
        # ============================================================
        if self.thrown and not self.exploded:

            # mulai hitung timer meledak saat dilempar
            if not self._throw_timer_started:
                self.start_throw_timer()
                self._throw_timer_started = True

            if time.time() - self._throw_start_time >= self.fuse_time:
                self.explode()
                return

            # BOM LURUS
            self.rect.x += self.vel_x * dt
            self.rect.y += self.vel_y * dt

            return

        # ============================================================
        # 3. SEDANG MELEDAK
        # ============================================================
        if self.exploded:
            if time.time() - self._explosion_start_time >= self.explosion_duration:
                self.kill()

            return

    # ============================================================
    # EXPLOSION
    # ============================================================
    def explode(self):
        """Ubah bomb menjadi ledakan"""
        if self.exploded:
            return

        self.exploded = True
        self.thrown = False

        self.image = self.image_explosion
        self.rect = self.image.get_rect(center=self.rect.center)

        self._start_explosion_timer()

    # ============================================================
    # ATTACH
    # ============================================================

    def attach_to_player(self, player):
        """Tempelkan bomb ke player"""
        self.attached = True
        self.player = player