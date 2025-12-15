import pygame
import math
from entities.slime import Slime

class Skeleton(Slime):

    """
    Skeleton Enemy
    --------------
    Enemy turunan dari Slime.
    Mewarisi perilaku dasar (movement, collision, target tracking)
    lalu menambahkan:
    - animasi skeleton
    - jarak serang khusus
    - damage ke player

    Konsep OOP:
    - Inheritance : Skeleton ← Slime
    - Polymorphism: override update() dan die()
    """

    def __init__(self, x, y, target, walls):
        # Panggil constructor parent (Slime)
        super().__init__(x, y, target, walls)

        SCALE = 2

        # ============================
        # WALK ANIMATION
        # ============================
        sheet = pygame.image.load("assets/enemy/skeleton_walk.png").convert_alpha()
        FRAMES = 8
        FW = sheet.get_width() // FRAMES
        FH = sheet.get_height()

        self.frames_right = []
        for i in range(FRAMES):
            frame = sheet.subsurface((i * FW, 0, FW, FH))
            frame = pygame.transform.scale(frame, (FW * SCALE, FH * SCALE))
            self.frames_right.append(frame)

        self.frames_left = [pygame.transform.flip(f, True, False) for f in self.frames_right]

        # ============================
        # STATE & STATUS
        # ============================
        self.frame_index = 0
        self.walk_speed = 9

        self.facing_right = True

        # Attack cooldown
        self.attack_cooldown = 1.0
        self.attack_timer = 0

        # Set sprite awal
        self.image = self.frames_right[0]
        self.rect = self.image.get_rect(center=(x, y))

        # ============================
        # DISTANCE RULES
        # ============================
        self.stop_distance = 25     # berhenti mendekat
        self.attack_distance = 35   # jarak serang

        # ============================
        # HITBOX
        # ============================
        w, h = self.rect.size

        self.hitbox = pygame.Rect(0, 0, int(w * 0.45), int(h * 0.55))

        # Offset hitbox agar sejajar dengan kaki sprite
        self.hitbox_offset_y = -20   

        self.hitbox.center = (self.rect.centerx, self.rect.centery + self.hitbox_offset_y)

        # ============================
        # MOVEMENT
        # ============================
        self.speed = 90 
        self.vel_x = 0
        self.vel_y = 0

    # ==================================================
    # COLLISION x
    # ==================================================
    def collide_x(self):
        """Handle collision horizontal dengan wall"""
        for wall in self.walls:
            if self.hitbox.colliderect(wall):
                if self.vel_x > 0:
                    self.hitbox.right = wall.left
                elif self.vel_x < 0:
                    self.hitbox.left = wall.right

        self.rect.centerx = self.hitbox.centerx
        self.rect.centery = self.hitbox.centery - self.hitbox_offset_y

    # ==================================================
    # COLLISION x
    # ==================================================
    def collide_y(self):
        """Handle collision vertikal dengan wall"""
        for wall in self.walls:
            if self.hitbox.colliderect(wall):
                if self.vel_y > 0:
                    self.hitbox.bottom = wall.top
                elif self.vel_y < 0:
                    self.hitbox.top = wall.bottom

        self.rect.centerx = self.hitbox.centerx
        self.rect.centery = self.hitbox.centery - self.hitbox_offset_y

    # ==================================================
    # UPDATE
    # ==================================================
    def update(self, dt):
        """
        Update behavior Skeleton:
        - mengejar player
        - menyerang jika dekat
        - update animasi
        """

        # cooldown
        if self.attack_timer > 0:
            self.attack_timer -= dt

        # posisi player
        px, py = self.target.hitbox.center
        ex, ey = self.hitbox.center
        dist = math.hypot(px - ex, py - ey)

        # ============================
        # MOVEMENT (CHASE PLAYER)
        # ============================
        if dist > self.stop_distance:
            angle = math.atan2(py - ey, px - ex)
            self.vel_x = math.cos(angle) * self.speed
            self.vel_y = math.sin(angle) * self.speed
        else:
            self.vel_x = 0
            self.vel_y = 0

        # Hadap ke arah player
        self.facing_right = (px - ex) >= 0

        # apply movement x
        self.hitbox.centerx += self.vel_x * dt
        self.collide_x()

        # apply movement y
        self.hitbox.centery += self.vel_y * dt
        self.collide_y()

        # ============================
        # ATTACK
        # ============================
        if dist < self.attack_distance:
            if self.attack_timer <= 0:
                self.target.take_damage(1)
                self.attack_timer = self.attack_cooldown

        # ============================
        # ANIMATION
        # ============================
        if abs(self.vel_x) > 1 or abs(self.vel_y) > 1:
            self.frame_index += self.walk_speed * dt
        else:
            self.frame_index = 0

        anim = self.frames_right if self.facing_right else self.frames_left

        if self.frame_index >= len(anim):
            self.frame_index = 0

        old_center = self.rect.center
        self.image = anim[int(self.frame_index)]
        self.rect = self.image.get_rect(center=old_center)

        # sync hitbox
        self.hitbox.center = (self.rect.centerx, self.rect.centery + self.hitbox_offset_y)

    # ==================================================
    # DIE (POLYMORPHISM)
    # ==================================================
    def die(self):
        """
        Override method die() dari parent (Slime).
        Menambahkan behavior khusus Skeleton,
        lalu memanggil die() milik parent.
        """
        print("Skeleton hancur")
        super().die()