import pygame
import math
from core.spritesheet_loader import load_spritesheet_stable
from entities.base_entity import BaseEntity

def line_blocked(start, end, walls):

    # Mengecek apakah garis antara dua titik terhalang wall.
    # Digunakan untuk AI agar slime tidak menabrak tembok secara lurus.

        x1, y1 = start
        x2, y2 = end

        steps = int(max(abs(x2-x1), abs(y2-y1)))
        if steps == 0:
            return False

        dx = (x2 - x1) / steps
        dy = (y2 - y1) / steps

        x, y = x1, y1
        for _ in range(steps):
            x += dx
            y += dy
            point = pygame.Rect(x, y, 2, 2)
            for w in walls:
                if point.colliderect(w):
                    return True
        return False

class Slime(BaseEntity):

    """
    Slime Enemy
    -----------
    Enemy dasar yang mengejar player.

    Konsep OOP:
    - Inheritance  : Slime ← BaseEntity
    - Encapsulation: HP disimpan dalam variabel private (_hp)
    - Polymorphism : override method update() dan die()
    """

    def __init__(self, x, y, target, walls):
        # Panggil constructor BaseEntity
        super().__init__(x, y, image_path=None, speed=80)


        # =========================
        # STATUS & ATRIBUT
        # =========================

        # posisi float
        self.pos_x = float(x)
        self.pos_y = float(y)

        self._hp = 1

        # walls diterima dari Game (NO CIRCULAR IMPORT)
        self.walls = walls

        # ==================================
        # LOAD ANIMATION
        # ==================================
        raw_frames = load_spritesheet_stable(
            "assets/enemy/slime (1).png",
            32, 32, scale=2
        )

        self.frames_right = raw_frames
        self.frames_left = [pygame.transform.flip(f, True, False) for f in raw_frames]

        self.frames = self.frames_right
        self.frame_index = 0
        self.anim_timer = 0
        self.anim_interval = 0.12

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=(x, y))

        # ==================================
        # HITBOX
        # ==================================
        w, h = self.rect.size
        self.hitbox = pygame.Rect(0, 0, int(w * 0.55), int(h * 0.45))
        self.hitbox.midbottom = self.rect.midbottom

        # FOLLOW PLAYER
        self.target = target

        # =========================
        # MOVEMENT
        # =========================
        self.vel_x = 0
        self.vel_y = 0


        # =========================
        # COMBAT
        # =========================
        self.damage_delay = 0.6
        self.damage_cooldown = 0

    # =========================================
    # COLLISION X
    # =========================================
    def collide_x(self):
        """Handle collision horizontal dengan wall"""
        for wall in self.walls:
            if self.hitbox.colliderect(wall):

                if self.vel_x > 0:
                    self.hitbox.right = wall.left
                elif self.vel_x < 0:
                    self.hitbox.left = wall.right

                 # hentikan drift posisi float
                self.pos_x = self.hitbox.centerx

        self.rect.midbottom = self.hitbox.midbottom

    # ==================================================
    # COLLISION Y
    # ==================================================
    def collide_y(self):
        """Handle collision vertikal dengan wall"""
        for wall in self.walls:
            if self.hitbox.colliderect(wall):

                if self.vel_y > 0:
                    self.hitbox.bottom = wall.top
                elif self.vel_y < 0:
                    self.hitbox.top = wall.bottom

                # STOP drifting
                self.pos_y = self.hitbox.centery

        self.rect.midbottom = self.hitbox.midbottom

    # ==================================
    def update(self, dt):
        """
        Update perilaku slime:
        - mengejar player
        - menghindari wall
        - animasi
        - memberi damage saat kontak
        """

        # FOLLOW PLAYER
        tx, ty = self.target.hitbox.center
        ex, ey = self.hitbox.center

        angle = math.atan2(ty - ey, tx - ex)

        # ==========================
        # FACE PLAYER (Flip)
        # ==========================
        if tx > ex:
            self.frames = self.frames_right
        else:
            self.frames = self.frames_left

        self.vel_x = math.cos(angle) * self.speed
        self.vel_y = math.sin(angle) * self.speed

        # ===== MOVE X =====
        self.pos_x += self.vel_x * dt
        self.hitbox.centerx = int(self.pos_x)
        self.collide_x()

        # ===== MOVE Y =====
        self.pos_y += self.vel_y * dt
        self.hitbox.centery = int(self.pos_y)
        self.collide_y()

        # update sprite position
        old_center = self.rect.center
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=old_center)
        self.hitbox.midbottom = self.rect.midbottom

        # =========================
        # ANIMATION
        # =========================
        self.anim_timer += dt
        if self.anim_timer >= self.anim_interval:
            self.anim_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.frames)


        # =========================
        # DAMAGE PLAYER
        # =========================
        if self.damage_cooldown > 0:
            self.damage_cooldown -= dt

        if self.hitbox.colliderect(self.target.hitbox):
            if self.damage_cooldown <= 0:
                self.target.take_damage(1)
                print("Player kena! HP:", self.target.get_hp())
                self.damage_cooldown = self.damage_delay
        
        tx, ty = self.target.hitbox.center
        ex, ey = self.hitbox.center

        # =========================
        # OBSTACLE AVOIDANCE
        # =========================

        blocked = line_blocked((ex, ey), (tx, ty), self.walls)

        if not blocked:
            # cari jalur alternatif
            angle = math.atan2(ty - ey, tx - ex)
            self.vel_x = math.cos(angle) * self.speed
            self.vel_y = math.sin(angle) * self.speed

        else:
            # muter: coba geser horizontal / vertical
            if abs(tx - ex) > abs(ty - ey):
                self.vel_x = self.speed if tx > ex else -self.speed
                self.vel_y = 0
            else:
                self.vel_y = self.speed if ty > ey else -self.speed
                self.vel_x = 0

# =========================
# ENCAPSULATION - HP
# =========================

    def get_hp(self):
        return self._hp
    
    def take_damage(self, amount):
        self._hp -= amount
        if self._hp <= 0:
            self._hp = 0
            self.die()

    # =========================
    # POLYMORPHISM - DIE
    # =========================

    def die(self):
        """
        Override die() dari BaseEntity.
        Menambahkan efek/log khusus slime,
        lalu memanggil die() milik parent.
        """
        
        print("Slime hancur")
        super().die()