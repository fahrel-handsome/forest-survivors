import pygame

class BaseEntity(pygame.sprite.Sprite):

    """
    BaseEntity
    ----------
    Kelas dasar (parent) untuk semua entity di game
    seperti Player, Enemy, Projectile, dll.

    Menerapkan konsep:
    - Inheritance (turunan dari pygame.sprite.Sprite)
    - Encapsulation (status hidup disimpan sebagai atribut private)
    """

    def __init__(self, x, y, image_path=None, speed=4):
        super().__init__()

        # =========================
        # STATUS HIDUP (ENCAPSULATION)
        # =========================
        self._alive = True

        # =========================
        # LOAD IMAGE
        # =========================
        if image_path:
            self.image = pygame.image.load(image_path).convert_alpha()

        else:
            # fallback kotak kalau tidak ada gambar
            self.image = pygame.Surface((32, 32))
            self.image.fill((255, 0, 0))

        # Rect utama (untuk render)
        self.rect = self.image.get_rect(topleft=(x, y))
        # Hitbox terpisah untuk collision
        self.hitbox = self.rect.copy()
        # Kecepatan dasar entity
        self.speed = speed

    def move(self, dx, dy, dt, map_width=None, map_height=None):
        """
        Menggerakkan entity berdasarkan arah dan delta time.
        Digunakan oleh entity sederhana (bukan player).
        """
        # Normal movement
        step = self.speed * dt
        self.rect.x += dx * step
        self.rect.y += dy * step

        # Update hitbox
        self.hitbox.center = self.rect.center
        self.hitbox.y -= 10

        # =========================
        # BATAS MAP (BOUNDARY)
        # =========================
        if map_width and map_height:
            if self.rect.left < 0:
                self.rect.left = 0
            if self.rect.top < 0:
                self.rect.top = 0
            if self.rect.right > map_width:
                self.rect.right = map_width
            if self.rect.bottom > map_height:
                self.rect.bottom = map_height

            # update hitbox lagi habis dipaksa
            self.hitbox.center = self.rect.center
            self.hitbox.y -= 10

    def is_alive(self):
        """Mengembalikan status hidup entity"""
        return self._alive

    def die(self):
        """
        Mematikan entity:
        - Set status hidup false
        - Nonaktifkan hitbox agar tidak collide lagi
        """
        self._alive = False
        if hasattr(self, "hitbox"):
            self.hitbox.size = (0, 0)
    
    def draw_debug(self, surface):
        """
        Method kosong untuk polymorphism.
        Entity turunan boleh override method ini
        untuk menampilkan debug (hitbox, dll).
        """
        pass 