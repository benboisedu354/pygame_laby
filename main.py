import pygame
from src.game import Game

def main():
    pygame.init()
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        # S'assurer que pygame est bien fermé
        if pygame.get_init():
            pygame.quit()

if __name__ == "__main__":
    main()