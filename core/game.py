import pygame
import random
from core.settings import *
from entities.player import Player
from entities.slime import Slime
from world.map_loader import MapLoader
from entities.health import HealthPickup
from entities.skeleton import Skeleton
from entities.BombPickup import BombPickup

class Game:
    instance = None 
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Top Down OOP Game")
        # === MENU BACKGROUND ===
        self.__menu_bg = pygame.image.load("assets/ui/bgMainMenu.jpg").convert()
        self.__menu_bg = pygame.transform.scale(
            self.__menu_bg, (SCREEN_W, SCREEN_H)
        )
        # === BGM ===
        self.__menu_bgm = "assets/audio/bgm.mp3"
        self.__game_bgm = "assets/audio/playgame.mp3"

        self.__current_bgm = None  # buat ngecek lagi play apa

        self.state = "MENU"

        # === CAMERA ZOOM ===
        self.ZOOM = 2  # integer zoom agar pixel tidak blur

        cam_w = int(SCREEN_W / self.ZOOM)
        cam_h = int(SCREEN_H / self.ZOOM)

        self.camera_surface = pygame.Surface((cam_w, cam_h)).convert()

        self.clock = pygame.time.Clock()

        self.heart_img = pygame.image.load("assets/ui/heart.png").convert_alpha()
        w, h = self.heart_img.get_size()
        self.heart_img = pygame.transform.scale(self.heart_img, (w * 4, h * 4))

        self.hp_food_images = [
            pygame.image.load("assets/food/watermelon.png").convert_alpha(),
            pygame.image.load("assets/food/apple.png").convert_alpha(),
            pygame.image.load("assets/food/chicken.png").convert_alpha()
        ]

        self.hp_food_images = [
            pygame.transform.scale2x(img) for img in self.hp_food_images
        ]

        self.max_hp_pickup = 2

        self.bomb_img = pygame.image.load("assets/bomb.png").convert_alpha()
        self.bomb_available = True   # bomb siap untuk spawn
        self.current_bomb = None     # referensi bomb yang lagi ada

        Game.instance = self   # ← set instance
        self.font = pygame.font.Font(None, 40)
        self.__score = 0

        self.__gameover_card = pygame.image.load("assets/ui/cardGameOver.png").convert_alpha()

        # === BUTTON IMAGES ===
        self.btn_img = pygame.image.load("assets/ui/button.png").convert_alpha()

        # scale
        self.btn_img = pygame.transform.scale_by(self.btn_img, 3)

        # rect tombol menu
        self.play_rect  = self.btn_img.get_rect(center=(SCREEN_W//2, SCREEN_H//2))
        self.quit_rect  = self.btn_img.get_rect(center=(SCREEN_W//2, SCREEN_H//2 + 120))

        # ===============================
        # MAP
        # ===============================
        self.map = MapLoader()
        self.map.load("assets/maps/mainMap.tmx")

        # Map size (biar gampang dipakai)
        self.map_width = self.map.map_width
        self.map_height = self.map.map_height

        # Collider group dari MapLoader
        self.walls = []
        for rect in self.map.colliders:
            self.walls.append(rect)

        # ===============================
        # ENTITY GROUPS
        # ===============================
        self.entities = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.pickups = pygame.sprite.Group()
        self.bomb_pickups = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        # ===============================
        # PLAYER
        # ===============================
        px = random.randint(0, self.map.map_width)
        py = random.randint(0, self.map.map_height)
        self.player = Player(px, py, self)
        self.entities.add(self.player)

        # ===============================
        # AUTO SPAWN MUSUH
        # ===============================
        self.max_enemy = 2
        self.enemy_increase_timer = 0
        self.enemy_increase_interval = 20
        self.enemy_max_limit = 20

        self.spawn_initial_enemies()

        # Health Pickup group
        self.pickups = pygame.sprite.Group()

        # Spawn pertama kali 3 kotak
        for i in range(self.max_hp_pickup):
            self.spawn_health()

    # =========================
    # ENCAPSULATION - SCORE
    # =========================
    def get_score(self):
        return self.__score

    def add_score(self, amount=1):
        self.__score += amount

    def reset_score(self):
        self.__score = 0


    def spawn_initial_enemies(self):
        """Wave awal: semua slime dulu (spawn di posisi aman)."""
        while len(self.enemies) < self.max_enemy:
            x, y = self.get_random_safe_position()
            slime = Slime(x, y, self.player, self.walls)
            self.enemies.add(slime)
            self.entities.add(slime)

    def spawn_random_enemy(self, x, y):
        enemy_type = random.choice(["slime", "skeleton"])

        if enemy_type == "slime":
            e = Slime(x, y, self.player, self.walls)
        else:
            e = Skeleton(x, y, self.player, self.walls)

        self.enemies.add(e)
        self.entities.add(e)


    # -------------------------------------------------------
    def respawn_enemy_if_needed(self):
        while len(self.enemies) < self.max_enemy:
            x, y = self.get_random_safe_position()
            self.spawn_random_enemy(x, y)


    def get_random_safe_position(self):
        """Cari posisi random yang tidak overlap collider."""
        SAFE_SIZE = 32   # ukuran bounding pickup/enemy

        while True:
            x = random.randint(0, self.map_width - SAFE_SIZE)
            y = random.randint(0, self.map_height - SAFE_SIZE)

            test = pygame.Rect(x, y, SAFE_SIZE, SAFE_SIZE)

            blocked = False
            for wall in self.walls:
                if test.colliderect(wall):
                    blocked = True
                    break

            if not blocked:
                return x, y

    # -------------------------------------------------------
    def spawn_health(self):
        x, y = self.get_random_safe_position()
        h = HealthPickup(x, y, self.hp_food_images)
        self.pickups.add(h)

    def spawn_bomb(self):
        x, y = self.get_random_safe_position()
        b = BombPickup(x, y, self.bomb_img)
        self.bomb_pickups.add(b)
        self.entities.add(b)

    # -------------------------------------------------------
    def draw_hp(self):
        for i in range(self.player.get_hp()):
            x = 10 + i * (self.heart_img.get_width() + 5)
            self.screen.blit(self.heart_img, (x, 10))

    def kill_enemy(self, enemy):
        self.add_score(1)
        if enemy in self.enemies:
            self.enemies.remove(enemy)
        if enemy in self.entities:
            self.entities.remove(enemy)
        enemy.kill()
        print("Enemy mati!")

    def play_bgm(self, path, volume=0.5, force=False):
        if self.__current_bgm == path and not force:
            return

        pygame.mixer.music.stop()
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)
        self.__current_bgm = path


    def draw_game_over(self):
            # --- CARD BACKGROUND ---
        card_rect = self.__gameover_card.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2))
        self.screen.blit(self.__gameover_card, card_rect)
        
        font_big = pygame.font.Font("assets/font/Tiny5-Regular.ttf", 60)
        font_mid = pygame.font.Font("assets/font/Tiny5-Regular.ttf", 50)
        font_small = pygame.font.Font("assets/font/Tiny5-Regular.ttf", 40)

        # Tulisan "GAME OVER"
        text = font_big.render("GAME OVER", True, (102, 61, 0))
        rect = text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 3.5))
        self.screen.blit(text, rect)

        # === SCORE ===
        score_text = font_mid.render(f"Score: {self.get_score()}", True, (255, 255, 255))
        score_rect = score_text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 3 + 20))
        self.screen.blit(score_text, score_rect)

        # Tombol Retry
        retry_text = font_small.render("Retry", True, (255, 255, 255))
        self.retry_rect = retry_text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2))
        pygame.draw.rect(self.screen, (153, 102, 51), self.retry_rect.inflate(40, 20))
        self.screen.blit(retry_text, self.retry_rect)
        

        # Tombol Quit
        home_text = font_small.render("Quit", True, (255, 255, 255))
        self.home_rect = home_text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 80))
        pygame.draw.rect(self.screen, (153, 102, 51), self.home_rect.inflate(40, 20))
        self.screen.blit(home_text, self.home_rect)

    def draw_menu(self):
            # === DRAW MENU BACKGROUND ===
        self.screen.blit(self.__menu_bg, (0, 0))

        font_big = pygame.font.Font("assets/font/Jersey15-Regular.ttf", 100)
        font_btn = pygame.font.Font("assets/font/Tiny5-Regular.ttf", 40)

        title = font_big.render("FOREST SURVIVORS", True, (245, 190, 39))
        title_rect = title.get_rect(center=(SCREEN_W // 2, SCREEN_H // 3))
        self.screen.blit(title, title_rect)

        # ========= PLAY =========
        play_text = font_btn.render("Play", True, (255, 255, 255))
        self.play_rect = play_text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2))
        pygame.draw.rect(self.screen, (153, 102, 51), self.play_rect.inflate(40, 20))
        self.screen.blit(play_text, self.play_rect)

        # ========= QUIT =========
        quit_text = font_btn.render("Quit", True, (255, 255, 255))
        self.quit_rect = quit_text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 80))
        pygame.draw.rect(self.screen, (153, 102, 51), self.quit_rect.inflate(40, 20))
        self.screen.blit(quit_text, self.quit_rect)

    def restart_game(self):
        # Reset semua variabel game
        self.reset_score()
        self.player.reset_hp()
        self.state = "PLAY"

        # Reset player posisi
        self.player.rect.x, self.player.rect.y = self.get_random_safe_position()

        # Bersihkan enemy lama
        self.entities = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.pickups = pygame.sprite.Group()
        self.bomb_pickups = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()

        # Tambah player lagi
        self.entities.add(self.player)

        # Reset musuh awal
        self.max_enemy = 2
        self.spawn_initial_enemies()

        # Spawn health lagi
        for i in range(self.max_hp_pickup):
            self.spawn_health()

        # 🔁 PAKSA RESTART BGM GAME
        self.play_bgm(self.__game_bgm, volume=0.4, force=True)

    def go_to_menu(self):
        self.state = "MENU"

    def can_spawn_bomb(self):
        return (
            len(self.bomb_pickups) == 0
            and not self.player.has_bomb()
            and len(self.projectiles) == 0
        )

    # -------------------------------------------------------
    def run(self):
        running = True
        while running:
            dt = self.clock.tick(FPS) / 1000

            # ========================
            # BGM BASED ON GAME STATE
            # ========================
            if self.state == "MENU":
                self.play_bgm(self.__menu_bgm, volume=0.4)

            elif self.state == "PLAY":
                self.play_bgm(self.__game_bgm, volume=0.4)


            # === TIMER PENAMBAHAN MUSUH OTOMATIS ===
            self.enemy_increase_timer += dt

            # setiap 20 detik max musuh bertambah 1
            if self.enemy_increase_timer >= self.enemy_increase_interval:
                if self.max_enemy < self.enemy_max_limit:
                    self.max_enemy += 1
                    print("Musuh bertambah! max sekarang =", self.max_enemy)
                self.enemy_increase_timer = 0


            # Input
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False

                # ======================================
                # HANDLE INPUT SAAT MENU
                # ======================================
                if self.state == "MENU":
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()

                        if self.play_rect.collidepoint(mx, my):
                            self.state = "PLAY"

                        if self.quit_rect.collidepoint(mx, my):
                            pygame.quit()
                            quit()

                    continue  # supaya input lain tidak aktif

                # ======================================
                # HANDLE INPUT SAAT GAME OVER
                # ======================================   
                if self.state == "GAMEOVER":
                    if e.type == pygame.MOUSEBUTTONDOWN:
                        mx, my = pygame.mouse.get_pos()
                        print("Mouse clicked at:", mx, my)

                        if self.retry_rect.collidepoint(mx, my):
                            print("Retry CLICKED")
                            self.restart_game()

                        if self.home_rect.collidepoint(mx, my):
                            pygame.quit()
                            quit()

                    continue

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        self.player.attack()
                    if e.key == pygame.K_LSHIFT or e.key == pygame.K_RSHIFT:
                        self.player.roll()
                    if e.key == pygame.K_e:
                        self.player.throw_bomb()

            # ========================
            #   UPDATE ENTITY HANYA SAAT MAIN
            # ========================
            if self.state == "PLAY":
                self.entities.update(dt)
                self.projectiles.update(dt)
            else:
                # Freeze semua musuh dan player
                for enemy in self.enemies:
                    enemy.vel_x = 0
                    enemy.vel_y = 0

            if self.can_spawn_bomb():
                self.spawn_bomb()

            # === UPDATE CAMERA ===
            # CAMERA FOLLOW + ZOOM
            self.camera_x = self.player.rect.centerx - (SCREEN_W / self.ZOOM) / 2
            self.camera_y = self.player.rect.centery - (SCREEN_H / self.ZOOM) / 2

            # Batasi supaya tidak keluar map
            self.camera_x = max(0, min(self.camera_x, self.map.map_width - (SCREEN_W / self.ZOOM)))
            self.camera_y = max(0, min(self.camera_y, self.map.map_height - (SCREEN_H / self.ZOOM)))

            map_w = self.map.surface.get_width()
            map_h = self.map.surface.get_height()

            self.player.clamp_to_map(self.map.map_width, self.map.map_height)

            # === HEALTH PICKUP ===
            for h in list(self.pickups):
                if self.player.hitbox.colliderect(h.hitbox):
                    h.apply_effect(self.player)

                    # Pastikan jumlah makanan selalu 2
                    while len(self.pickups) < self.max_hp_pickup:
                        self.spawn_health()
                        

            # PLAYER AMBIL BOMB
            for b in list(self.bomb_pickups):
                if self.player.hitbox.colliderect(b.hitbox):
                    if self.player.can_pick_bomb():
                        self.player.pick_bomb(b)
                        
                       
            # ===============================
            # PLAYER SERANG SEMUA MUSUH
            # ===============================
            if self.player.attacking:
                atk = self.player.get_attack_hitbox()

                for enemy in list(self.enemies):
                    if atk.colliderect(enemy.hitbox):
                        enemy.take_damage(1)

            # ===============================
            # UNIVERSAL ENEMY DEATH CHECK
            # (bom, projectile, poison, dll)
            # ===============================
            for enemy in list(self.enemies):
                if not enemy.is_alive():
                    self.kill_enemy(enemy)

            # ===============================
            # RESPAWN MUSUH OTOMATIS
            # ===============================
            self.respawn_enemy_if_needed()


           # ======================================
            #  DRAW KE CAMERA_SURFACE (NON-ZOOM)
            # ======================================
            self.camera_surface.fill((90, 150, 90))

            # Map
            self.map.draw(self.camera_surface, self.camera_x, self.camera_y) #, debug=True)

            # Player
            self.camera_surface.blit(
                self.player.image,
                (self.player.rect.x - self.camera_x,
                self.player.rect.y - self.camera_y)
            )

            # Enemies
            for enemy in self.enemies:
                self.camera_surface.blit(
                    enemy.image,
                    (enemy.rect.x - self.camera_x,
                    enemy.rect.y - self.camera_y)
                )

            # Pickup
            for h in self.pickups:
                self.camera_surface.blit(
                    h.image,
                    (h.rect.x - self.camera_x,
                    h.rect.y - self.camera_y)
                )
            
            # Bomb pickups
            for b in self.bomb_pickups:
                self.camera_surface.blit(
                    b.image,
                    (b.rect.x - self.camera_x,
                    b.rect.y - self.camera_y)
                )
            # Projectiles
            for p in self.projectiles:
                self.camera_surface.blit(
                    p.image,
                    (p.rect.x - self.camera_x, p.rect.y - self.camera_y)
                )

            # Debug (gambar di camera, supaya ikut zoom)
            # self.player.draw_debug(self.camera_surface)
            # for enemy in self.enemies:
            #     enemy.draw_debug(self.camera_surface)
            # for h in self.pickups:
            #     h.draw_debug(self.camera_surface, self.camera_x, self.camera_y)

            # ======================================
            #  APPLY ZOOM KE LAYAR
            # ======================================
            # scaled_frame = pygame.transform.scale(
            #     self.camera_surface,
            #     (SCREEN_W, SCREEN_H)
            # )
            scaled = pygame.transform.scale2x(self.camera_surface)
            self.screen.blit(scaled, (0, 0))

            if self.state == "PLAY":
                self.draw_hp()
                score_surf = self.font.render(f"Score: {self.get_score()}", True, (255,255,255))
                score_rect = score_surf.get_rect(topright=(self.screen.get_width() - 20, 20))
                self.screen.blit(score_surf, score_rect)

            elif self.state == "GAMEOVER":
                self.draw_game_over()

            elif self.state == "MENU":
                self.draw_menu()

            pygame.display.flip()
