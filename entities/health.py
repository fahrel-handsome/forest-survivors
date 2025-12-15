import pygame, random
from entities.base_entity import BaseEntity

class HealthPickup(BaseEntity):
    """
    HealthPickup
    ------------
    Pickup item yang menambah HP player saat diambil.

    Konsep OOP:
    - Inheritance  : turunan dari BaseEntity
    - Polymorphism : method apply_effect() dipanggil dengan cara
                     yang sama seperti pickup lain (bomb, dll)
    """

    def __init__(self, x, y, food_images):
        super().__init__(x, y)

        # =========================
        # PILIH GAMBAR SECARA RANDOM
        # =========================
        # Memberi variasi visual tanpa logika tambahan
        self.image = random.choice(food_images)

        # posisi & hitbox
        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = self.rect.copy()
        

    def update(self, dt):
        """
        HealthPickup tidak memiliki animasi atau pergerakan,
        sehingga method update dikosongkan.
        (Tetap ada untuk konsistensi dengan entity lain)
        """
        pass

    def draw_debug(self, screen, cam_x, cam_y):
        """Menampilkan hitbox untuk keperluan debug"""
        pygame.draw.rect(
            screen, (0, 255, 0),
            pygame.Rect(
                self.rect.x - cam_x,
                self.rect.y - cam_y,
                self.rect.width,
                self.rect.height
            ),
            2
        )

    def apply_effect(self, player):
        """
        Efek pickup:
        - Menambah HP player
        - Menghapus object pickup dari game
        """
        player.heal(1)
        self.kill()