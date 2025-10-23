class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.health = 100

    def move(self):
        self.x -= self.speed

    def attack(self, player):
        if self.collides_with(player):
            player.health -= 10

    def collides_with(self, player):
        # Simple collision detection
        return (self.x < player.x + player.width and
                self.x + self.width > player.x and
                self.y < player.y + player.height and
                self.y + self.height > player.y)

    def draw(self, screen):
        # Placeholder for drawing the enemy
        pass

    def update(self):
        self.move()