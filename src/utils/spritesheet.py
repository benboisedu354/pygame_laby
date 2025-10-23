import pygame

class SpriteSheet:
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert_alpha()

    def get_image(self, x, y, width, height):
        image = pygame.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pygame.transform.scale(image, (width, height))
        return image

    def get_images(self, rects):
        images = []
        for rect in rects:
            images.append(self.get_image(rect[0], rect[1], rect[2], rect[3]))
        return images