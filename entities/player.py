import pygame
from entities.base_entity import BaseEntity
from entities.thrown_bomb import ThrownBomb
from entities.BombPickup import BombPickup

class Player(BaseEntity):

    """
    Player entity.
    Mengatur:
    - Movement (jalan & roll)
    - Animasi (idle, run, attack, roll)
    - Combat (attack & bomb)
    - HP (encapsulation)
    - Collision dengan map
    """

    def __init__(self, x, y, game):
        # Referensi ke Game (untuk map, projectiles, state)
        self.game = game
        super().__init__(x, y, speed=150)

        SCALE = 2

# ==================================================
# LOAD ANIMATIONS
# ==================================================

        # ============================
        # LOAD RUN
        # ============================
        run_sheet = pygame.image.load("assets/player/run.png").convert_alpha()
        RUN_FRAMES = 8
        RUN_W = run_sheet.get_width() // RUN_FRAMES
        RUN_H = run_sheet.get_height()

        self.run_right = [
            pygame.transform.scale(
                run_sheet.subsurface((i * RUN_W, 0, RUN_W, RUN_H)),
                (RUN_W * SCALE, RUN_H * SCALE)
            ) for i in range(RUN_FRAMES)
        ]
        self.run_left = [pygame.transform.flip(f, True, False) for f in self.run_right]

        # ============================
        # LOAD IDLE
        # ============================
        idle_sheet = pygame.image.load("assets/player/idle.png").convert_alpha()
        IDLE_FRAMES = 9
        IDLE_W = idle_sheet.get_width() // IDLE_FRAMES
        IDLE_H = idle_sheet.get_height()

        self.idle_right = [
            pygame.transform.scale(
                idle_sheet.subsurface((i * IDLE_W, 0, IDLE_W, IDLE_H)),
                (IDLE_W * SCALE, IDLE_H * SCALE)
            ) for i in range(IDLE_FRAMES)
        ]
        self.idle_left = [pygame.transform.flip(f, True, False) for f in self.idle_right]

        # ============================
        # LOAD ATTACK
        # ============================
        atk_sheet = pygame.image.load("assets/player/attack.png").convert_alpha()
        ATK_FRAMES = 10
        ATK_W = atk_sheet.get_width() // ATK_FRAMES
        ATK_H = atk_sheet.get_height()

        self.atk_right = [
            pygame.transform.scale(
                atk_sheet.subsurface((i * ATK_W, 0, ATK_W, ATK_H)),
                (ATK_W * SCALE, ATK_H * SCALE)
            ) for i in range(ATK_FRAMES)
        ]
        self.atk_left = [pygame.transform.flip(f, True, False) for f in self.atk_right]

        # ============================
        # LOAD ROLL (10 FRAMES)
        # ============================
        roll_sheet = pygame.image.load("assets/player/roll.png").convert_alpha()
        ROLL_FRAMES = 10   # <-- perbaikan utama
        ROLL_W = roll_sheet.get_width() // ROLL_FRAMES
        ROLL_H = roll_sheet.get_height()

        self.roll_right = [
            pygame.transform.scale(
                roll_sheet.subsurface((i * ROLL_W, 0, ROLL_W, ROLL_H)),
                (ROLL_W * SCALE, ROLL_H * SCALE)
            ) for i in range(ROLL_FRAMES)
        ]
        self.roll_left = [pygame.transform.flip(f, True, False) for f in self.roll_right]

# ============================
# STATE & STATUS
# ============================

        # ==================================================
        # ENCAPSULATION: BOMB
        # ==================================================
        self._held_bomb = None

        self.bombs = 0

        self.attack_delay = 0.30
        self.attack_timer = 0
        self.attacking = False

        self.state = "idle"
        self.facing_right = True
        self.frame_index = 0
        self.animation_speed = 10

        self.image = self.idle_right[0]
        self.rect = self.image.get_rect(center=(x, y))

        # Roll
        self.rolling = False
        self.roll_duration = 0.3     # lamanya roll
        self.roll_timer = 0
        self.roll_speed = 450        # kecepatan saat roll


        # ============================
        # HITBOX
        # ============================
        w = self.rect.width
        h = self.rect.height

        self.hitbox = pygame.Rect(0, 0, int(w * 0.15), int(h * 0.25))
        self.hitbox.center = self.rect.center

        # ==================================================
        # ENCAPSULATION: HP
        # ==================================================
        self._max_hp = 3
        self._hp = self._max_hp

    # ==================================
    def roll(self):
        if not self.rolling and not self.attacking:
            self.rolling = True
            self.roll_timer = self.roll_duration
            self.state = "roll"
            self.frame_index = 0

            keys = pygame.key.get_pressed()
            self.roll_dir_x = keys[pygame.K_d] - keys[pygame.K_a]
            self.roll_dir_y = keys[pygame.K_s] - keys[pygame.K_w]

            # normalize arah biar gak ngebut diagonal
            if self.roll_dir_x != 0 or self.roll_dir_y != 0:
                length = (self.roll_dir_x**2 + self.roll_dir_y**2) ** 0.5
                self.roll_dir_x /= length
                self.roll_dir_y /= length
            else:
                self.roll_dir_x = 1 if self.facing_right else -1
                self.roll_dir_y = 0

# ==================================================
# ACTIONS
# ==================================================

    # ==================================
    def attack(self):
        if not self.attacking:
            self.attacking = True
            self.state = "attack"
            self.frame_index = 0
            self.attack_timer = 0

    # ==================================
    def throw_bomb(self):
        from core.game import Game  # ← aman di sini
        if not self._held_bomb:
            return

        pickup = self._held_bomb

        # Lepas pickup dari player
        pickup.attached = False
        pickup.player = None

        # Hapus pickup dari game
        pickup.kill()

        # Spawn ThrownBomb projectile
        direction = 1 if self.facing_right else -1
        thrown = ThrownBomb(self.rect.centerx, self.rect.centery - 10, direction)
        self.game.projectiles.add(thrown)

        self._held_bomb = None
        Game.instance.current_bomb = None

        # Respawn pickup baru
        BombPickup.spawn_random(self.game)

# ==================================================
# UPDATE LOOP
# ==================================================
        
    # ==================================
    def update(self, dt):
        keys = pygame.key.get_pressed()

        # Timer attack sebelum hitbox aktif
        if self.attacking:
            self.attack_timer += dt

        # Roll timer
        if self.rolling:
            self.roll_timer -= dt
            if self.roll_timer <= 0:
                self.rolling = False
                self.state = "idle"

        # Stop saat attack
        if self.attacking:
            dx = dy = 0
        else:
            dx = keys[pygame.K_d] - keys[pygame.K_a]
            dy = keys[pygame.K_s] - keys[pygame.K_w]

            # ===========================
            # SET VELOCITY
            # ===========================
            if self.rolling:
                self.vel_x = self.roll_dir_x
                self.vel_y = self.roll_dir_y
            else:
                self.vel_x = dx
                self.vel_y = dy

        # ==== HITUNG VELOCITY ====
        speed = self.roll_speed if self.rolling else self.speed

        self.vel_x = dx * speed
        self.vel_y = dy * speed

        # ================================
        # MOVE USING HITBOX
        # ================================

        # X
        self.hitbox.x += self.vel_x * dt
        self.collide_map_x()

        # Y
        self.hitbox.y += self.vel_y * dt
        self.collide_map_y()

        # Setelah gerak, sinkronkan rect ke hitbox
        self.rect.center = self.hitbox.center


        # ====== KEEP PLAYER INSIDE MAP ======
        map_w = self.game.map.map_width
        map_h = self.game.map.map_height


        if self.hitbox.left < 0:
            self.hitbox.left = 0
        if self.hitbox.right > map_w:
            self.hitbox.right = map_w

        if self.hitbox.top < 0:
            self.hitbox.top = 0
        if self.hitbox.bottom > map_h:
            self.hitbox.bottom = map_h

        # sync rect
        self.rect.center = self.hitbox.center

        if dx > 0: self.facing_right = True
        elif dx < 0: self.facing_right = False

        # Pilih animasi
        if self.attacking:
            anim = self.atk_right if self.facing_right else self.atk_left

        elif self.rolling:
            anim = self.roll_right if self.facing_right else self.roll_left
        else:
            if dx != 0 or dy != 0:
                anim = self.run_right if self.facing_right else self.run_left
            else:
                anim = self.idle_right if self.facing_right else self.idle_left

        # Frame anim
        self.frame_index += self.animation_speed * dt

        if self.attacking:
            if self.frame_index >= len(anim):
                self.frame_index = 0
                self.attacking = False
                anim = self.idle_right if self.facing_right else self.idle_left
        elif self.rolling:
            if self.frame_index >= len(anim):
                self.rolling = False
                self.state = "idle"
                self.frame_index = 0

        else:
            if self.frame_index >= len(anim):
                self.frame_index %= len(anim)
        

        # Update gambar tanpa geser posisi
        center = self.rect.center
        self.image = anim[int(self.frame_index)]
        self.rect = self.image.get_rect(center=center)

        # === BOUNDARY MAP ===
        map_w = self.game.map.map_width
        map_h = self.game.map.map_height

        self.clamp_to_map(map_w, map_h)


    # ==================================
    def get_attack_hitbox(self):
        if self.attack_timer < self.attack_delay:
            return pygame.Rect(0, 0, 0, 0)

        w = 40
        h = 30

        if self.facing_right:
            return pygame.Rect(self.rect.centerx + 10, self.rect.centery - 10, w, h)
        else:
            return pygame.Rect(self.rect.centerx - w - 10, self.rect.centery - 10, w, h)

    # ==================================
    def draw_debug(self, screen):
        cam_x = self.game.camera_x
        cam_y = self.game.camera_y

        # Debug rect player
        pygame.draw.rect(
            screen, (0, 255, 0),
            pygame.Rect(self.rect.x - cam_x, self.rect.y - cam_y, self.rect.width, self.rect.height),
            2
        )

        # Debug hitbox player
        pygame.draw.rect(
            screen, (255, 0, 0),
            pygame.Rect(self.hitbox.x - cam_x, self.hitbox.y - cam_y, self.hitbox.width, self.hitbox.height),
            2
        )

        # Debug attack hitbox
        if self.attacking:
            atk = self.get_attack_hitbox()
            pygame.draw.rect(
                screen, (0, 0, 255),
                pygame.Rect(atk.x - cam_x, atk.y - cam_y, atk.width, atk.height),
                2
            )

    def clamp_to_map(self, map_w, map_h):
        # clamp posisi center, bukan rect.x
        if self.rect.centerx < 0:
            self.rect.centerx = 0
        if self.rect.centery < 0:
            self.rect.centery = 0

        if self.rect.centerx > map_w:
            self.rect.centerx = map_w
        if self.rect.centery > map_h:
            self.rect.centery = map_h

# ==================================================
# COLLISION MAP
# ==================================================

    def collide_map_x(self):
        for c in self.game.map.colliders:
            if self.hitbox.colliderect(c):
                if self.vel_x > 0:  # kanan
                    self.hitbox.right = c.left
                elif self.vel_x < 0:  # kiri
                    self.hitbox.left = c.right

                # update rect
                self.rect.centerx = self.hitbox.centerx

    def collide_map_y(self):
        for c in self.game.map.colliders:
            if self.hitbox.colliderect(c):
                if self.vel_y > 0:  # turun
                    self.hitbox.bottom = c.top
                elif self.vel_y < 0:  # naik
                    self.hitbox.top = c.bottom

                # update rect
                self.rect.centery = self.hitbox.centery

    # =========================
    # ENCAPSULATION - HP
    # =========================
    def get_hp(self):
        return self._hp


    def take_damage(self, amount):
        self._hp = max(0, self._hp - amount)
        print("Player HP:", self._hp)

        if self._hp == 0:
            self.die()

    def heal(self, amount):
        self._hp = min(self._max_hp, self._hp + amount)

    def reset_hp(self):
        self._hp = self._max_hp

    def die(self):
        print("Player mati")
        self.game.state = "GAMEOVER"
    
    # =========================
    # ENCAPSULATION - BOMB
    # =========================
    def has_bomb(self):
        return self._held_bomb is not None
    
    def can_pick_bomb(self):
        return not self.has_bomb()
    
    def try_pick_bomb(self, bomb):
        if not self.has_bomb():
            self.pick_bomb(bomb)
    
    def pick_bomb(self, bomb):
        from core.game import Game

        self._held_bomb = bomb
        bomb.attach_to_player(self)

        Game.instance.bomb_available = False
        Game.instance.current_bomb = bomb
