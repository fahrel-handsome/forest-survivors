import pygame
from pytmx.util_pygame import load_pygame

class MapLoader:

    """
    MapLoader
    ---------
    Bertanggung jawab untuk:
    - Memuat file map (.tmx)
    - Merender tile map ke dalam satu surface
    - Menyediakan data collision untuk entity

    Prinsip OOP:
    - Single Responsibility Principle (SRP):
      Kelas ini hanya menangani map, tidak logika player / enemy.
    - Tidak menggunakan inheritance / polymorphism
      karena map bersifat data statis, bukan entity aktif.
    """

    def __init__(self):
        # data TMX
        self.tmx = None
        # surface hasil render seluruh map
        self.surface = None
        # ukuran map dalam pixel
        self.map_width = 0
        self.map_height = 0
        # daftar collider (pygame.Rect)
        self.colliders = []

    def load(self, path):
        """
        Memuat file TMX dan:
        - Menghitung ukuran map
        - Merender tile ke satu surface
        - Mengambil collision dari layer khusus
        """
        self.tmx = load_pygame(path)

        # ============================
        # HITUNG UKURAN MAP (PIXEL)
        # ============================
        self.map_width  = self.tmx.width  * self.tmx.tilewidth
        self.map_height = self.tmx.height * self.tmx.tileheight

        # ============================
        # BUAT SURFACE MAP
        # ============================
        self.surface = pygame.Surface((self.map_width, self.map_height), pygame.SRCALPHA)

        # ============================
        # RENDER TILE MAP
        # ============================
        for layer in self.tmx.visible_layers:
            if hasattr(layer, "tiles"):

                # opacity layer (default = 1.0)
                opacity = int((layer.opacity if layer.opacity is not None else 1) * 255)

                for x, y, tile in layer.tiles():
                    if tile:
                        # salin tile agar alpha tidak mengubah source
                        temp = tile.copy()
                        temp.set_alpha(opacity)

                        # gambar tile ke surface map
                        self.surface.blit(
                            temp,
                            (x * self.tmx.tilewidth, y * self.tmx.tileheight)
                        )

        # ======================================
        #  COLLISION OBJECTS (layer name = "collision")
        # ======================================
        self.colliders = []   # reset

        for layer in self.tmx.layers:  
            if layer.name == "collision":      # cek nama layer
                for obj in layer:              # ambil objek di layer itu
                    rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                    self.colliders.append(rect)

        print(f"[Map] Loaded {len(self.colliders)} colliders")

    # ==========================================================
    def draw(self, screen, camera_x, camera_y, debug=False):
        """Gambar map sesuai kamera"""
        if self.surface:
            screen.blit(self.surface, (-camera_x, -camera_y))

        # ======================================
        # DEBUG COLLIDERS
        # ======================================
        if debug:
            for c in self.colliders:
                pygame.draw.rect(
                    screen,
                    (0, 255, 0),
                    pygame.Rect(
                        c.x - camera_x,
                        c.y - camera_y,
                        c.width,
                        c.height
                    ),
                    2
                )
