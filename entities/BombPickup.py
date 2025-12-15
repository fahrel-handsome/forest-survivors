import pygame
import math
import random
from entities.base_entity import BaseEntity

class BombPickup(BaseEntity):
    """
    BombPickup
    ----------
    Item pickup berupa bomb yang dapat:
    - mengambang (idle animation)
    - diambil player
    - ditempel ke player sebelum dilempar

    Kelas ini hanya bertanggung jawab sebagai pickup,
    bukan logika ledakan.
    """

    def __init__(self, x, y, bomb_img):
        super().__init__(x, y)


        # =========================
        # VISUAL & HITBOX
        # =========================
        self.image = bomb_img
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = self.rect.copy()

        # =========================
        # FLOATING ANIMATION
        # =========================
        self.base_y = y                         # posisi awal Y
        self.float_time = random.random() * 10
        self.float_speed = 2
        self.float_range = 5

        # =========================
        # PICKUP STATE
        # =========================
        self.attached = False               # sedang dibawa player
        self.player = None

    # ============================================================
    # UPDATE
    # ============================================================
    def update(self, dt):
        """
        Update perilaku BombPickup:
        - Jika attached → mengikuti posisi player
        - Jika idle     → animasi mengambang
        """

        # =========================
        # DIBAWA PLAYER
        # =========================
        if self.attached and self.player:
            self.rect.centerx = self.player.rect.centerx + 15
            self.rect.centery = self.player.rect.centery - 15
            return

        # =========================
        # FLOATING ANIMATION
        # =========================
        self.float_time += dt * self.float_speed
        self.rect.centery = self.base_y + math.sin(self.float_time) * self.float_range

    # ============================================================
    # DEBUG DRAW
    # ============================================================
    def draw_debug(self, screen, cam_x, cam_y):
        """Menampilkan hitbox untuk debugging"""
        pygame.draw.rect(
            screen, (255, 200, 0),
            pygame.Rect(
                self.rect.x - cam_x,
                self.rect.y - cam_y,
                self.rect.width,
                self.rect.height
            ),
            2
        )

    # ============================================================
    # SPAWN
    # ============================================================
    @staticmethod
    def spawn_random(game):
        """
        Spawn BombPickup secara acak di map.
        Hanya boleh ada satu bomb aktif di dunia.
        """
        if not game.bomb_available:
            return  # jangan spawn kalau bomb masih dipegang/dilempar

        # batas map
        # spawn kalo kosong
        map_w = game.map.map_width
        map_h = game.map.map_height

        # posisi random
        x = random.randint(50, map_w - 50)
        y = random.randint(50, map_h - 50)

        bomb_img = pygame.image.load("assets/bomb.png").convert_alpha()
        new_pickup = BombPickup(x, y, bomb_img)

        new_pickup.attached = False
        new_pickup.player = None

        game.pickups.add(new_pickup)
        game.current_bomb = new_pickup

        game.bomb_available = False  # sudah ada 1 bomb di dunia

        print("Bomb spawned!")

    # ============================================================
    # PICKUP INTERACTION
    # ============================================================
        
    def attach_to_player(self, player):
        """Tempelkan pickup ke player"""
        self.attached = True
        self.player = player

    def detach(self):
        """Lepaskan pickup dari player"""
        self.attached = False
        self.player = None

    def apply_effect(self, player):
        """
        Efek saat player mengambil bomb:
        - Player mendapatkan bomb
        - Pickup dihapus dari dunia
        """
        if player.can_pick_bomb():
            player.pick_bomb(self)
            self.kill()   # HAPUS PICKUP DARI MAP