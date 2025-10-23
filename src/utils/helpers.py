def load_image(filepath):
    """Load an image from the specified file path."""
    try:
        image = pygame.image.load(filepath)
        return image
    except pygame.error as e:
        print(f"Unable to load image at {filepath}: {e}")
        return None

def check_collision(rect1, rect2):
    """Check if two rectangles collide."""
    return rect1.colliderect(rect2)

def load_sound(filepath):
    """Load a sound from the specified file path."""
    try:
        sound = pygame.mixer.Sound(filepath)
        return sound
    except pygame.error as e:
        print(f"Unable to load sound at {filepath}: {e}")
        return None

def get_centered_position(rect, screen_width, screen_height):
    """Get the centered position for a rectangle on the screen."""
    x = (screen_width - rect.width) // 2
    y = (screen_height - rect.height) // 2
    return x, y