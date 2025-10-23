import pygame
import math

class LevelSelect:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont('Arial', 30)
        self.title_font = pygame.font.SysFont('Arial', 50)
        
        # Configurer les options de nombre de niveaux
        self.level_counts = [1, 3, 5, 10]
        self.selected_index = 1  # Par défaut, sélectionner l'option 3 niveaux
        
        # Animation
        self.animation_time = 0
        self.animation_speed = 0.03
        
        # Récupérer les dimensions de l'écran
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        
    def draw(self, screen):
        # Fond bleu foncé
        screen.fill((0, 0, 35))
        
        # Titre
        title_text = self.title_font.render("Sélection du Nombre de Labyrinthes", True, (255, 255, 0))
        screen.blit(title_text, (self.screen_width//2 - title_text.get_width()//2, 50))
        
        # Instructions
        instruction_text = self.font.render("Combien de labyrinthes voulez-vous résoudre?", True, (255, 255, 255))
        screen.blit(instruction_text, (self.screen_width//2 - instruction_text.get_width()//2, 130))
        
        # Afficher les options
        y_offset = 200
        for i, count in enumerate(self.level_counts):
            # Déterminer la taille et la couleur en fonction de la sélection
            if i == self.selected_index:
                color = (255, 255, 255)
                # Animation de pulsation pour l'option sélectionnée
                size = int(40 * (1 + 0.15 * math.sin(self.animation_time * 2)))
                option_font = pygame.font.SysFont('Arial', size)
            else:
                color = (150, 150, 150)
                option_font = pygame.font.SysFont('Arial', 30)
            
            option_text = option_font.render(f"{count} labyrinthe{'s' if count > 1 else ''}", True, color)
            screen.blit(option_text, (self.screen_width//2 - option_text.get_width()//2, y_offset))
            y_offset += 70
        
        # Instructions supplémentaires
        help_text = self.font.render("Utilisez les flèches ↑↓ pour choisir, Entrée pour confirmer", True, (200, 200, 200))
        screen.blit(help_text, (self.screen_width//2 - help_text.get_width()//2, self.screen_height - 100))
        
        # Option de retour
        back_text = self.font.render("ESC pour revenir au menu", True, (200, 200, 200))
        screen.blit(back_text, (self.screen_width//2 - back_text.get_width()//2, self.screen_height - 60))
    
    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.level_counts)
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.level_counts)
                elif event.key == pygame.K_RETURN:
                    self.confirm_selection()
                elif event.key == pygame.K_ESCAPE:
                    # Retour au menu principal
                    from src.scenes.menu import Menu
                    self.game.current_scene = Menu(self.game)
        
        # Mettre à jour l'animation
        self.animation_time += self.animation_speed
    
    def confirm_selection(self):
        # Récupérer le nombre de niveaux sélectionné
        level_count = self.level_counts[self.selected_index]
        # Stocker cette valeur dans l'objet Game
        self.game.total_levels = level_count
        # Commencer le jeu avec le niveau 1
        from src.scenes.level import Level
        self.game.current_scene = Level(self.game, level_number=1)