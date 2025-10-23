class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 60
        self.speed = 5
        self.image = None  # Placeholder for player image
        self.health = 100

    def load_image(self, image_path):
        self.image = pygame.image.load(image_path)

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_alive(self):
        return self.health > 0