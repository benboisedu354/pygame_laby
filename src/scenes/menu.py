import pygame
import math
import random
from src.scenes.options import Options
from src.scenes.level import Level


class Menu:
    def __init__(self, game, show_victory=False):
        self.game = game
        self.font = pygame.font.SysFont('Arial', 30)
        # Ajout d'une option pour choisir le nombre de niveaux
        self.options = ["Partie Rapide", "Mode Custom", "Options", "Quit"]
        self.selected_option = 0
        
        # Attributs améliorés pour l'animation
        self.animation_time = 0
        self.animation_speed = 0.03  # Vitesse plus lente
        self.pulse_amount = 1.15  # Pulsation de taille
        
        # Attributs pour l'arrière-plan
        self.stars = []
        # Récupérer les dimensions réelles de l'écran
        self.screen_width, self.screen_height = pygame.display.get_surface().get_size()
        self.generate_stars(250)  # Plus d'étoiles pour remplir l'écran
        
        # Attribut pour afficher un message de victoire
        self.show_victory = show_victory
        self.victory_message = "Félicitations! Vous avez terminé tous les niveaux!"

    def generate_stars(self, count):
        # Utiliser les dimensions réelles de l'écran
        for _ in range(count):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            size = random.randint(1, 3)
            speed = random.uniform(0.1, 0.5)
            # Ajouter une luminosité variable pour plus de réalisme
            brightness = random.randint(150, 255)
            self.stars.append([x, y, size, speed, brightness])

    def draw(self, screen):
        screen_width, screen_height = screen.get_width(), screen.get_height()
        
        # Fond avec étoiles
        screen.fill((0, 0, 25))  # Bleu très foncé (presque noir)
        
        # Dessiner les étoiles en mouvement
        for star in self.stars:
            x, y, size, speed, base_brightness = star
            # Faire clignoter légèrement les étoiles
            brightness_variation = int(30 * math.sin(self.animation_time * 2 + x))
            brightness = max(100, min(255, base_brightness + brightness_variation))
            color = (brightness, brightness, brightness)
            pygame.draw.circle(screen, color, (int(x), int(y)), size)
            
            # Déplacer les étoiles (effet de parallaxe)
            star[1] = (y + speed) % screen_height
        
        # Afficher le titre sans ondulation
        title_font = pygame.font.SysFont('Arial', 60)
        title_text = title_font.render("Labyrinthe", True, (255, 255, 0))
        title_width = title_text.get_width()
        screen.blit(title_text, ((screen_width - title_width) // 2, 30))
        
        # Afficher le message de victoire si nécessaire
        if self.show_victory:
            victory_font = pygame.font.SysFont('Arial', 40)
            victory_text = victory_font.render(self.victory_message, True, (0, 255, 0))
            victory_width = victory_text.get_width()
            screen.blit(victory_text, ((screen_width - victory_width) // 2, 90))
        
        # Afficher les options
        y_offset = 170 if self.show_victory else 130
        
        for index, option in enumerate(self.options):
            # Déterminer la couleur et la taille en fonction de si l'option est sélectionnée
            if index == self.selected_option:
                # Couleur claire pour l'option sélectionnée
                color = (255, 255, 255)
                
                # Taille pulsante (on garde cette animation)
                size = int(40 * (1 + 0.15 * math.sin(self.animation_time * 2)))
                option_font = pygame.font.SysFont('Arial', size)
            else:
                color = (150, 150, 150)
                option_font = pygame.font.SysFont('Arial', 30)
            
            text_surface = option_font.render(option, True, color)
            text_width = text_surface.get_width()
            # Supprimer l'offset d'ondulation (wave_offset)
            screen.blit(text_surface, ((screen_width - text_width) // 2, y_offset + index * 70))
        
        # Afficher les meilleurs temps
        self.draw_highscores(screen)
    
    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.select_option()

        # Mise à jour de l'animation
        self.animation_time += self.animation_speed

    def select_option(self):
        if self.selected_option == 0:
            # Partie rapide (3 niveaux par défaut)
            print("Starting quick game...")
            self.game.total_levels = 3
            self.game.current_scene = Level(self.game, level_number=1)
        elif self.selected_option == 1:
            # Mode custom - ouvrir l'écran de sélection du nombre de niveaux
            print("Opening level count selection...")
            from src.scenes.level_select import LevelSelect
            self.game.current_scene = LevelSelect(self.game)
        elif self.selected_option == 2:
            print("Opening options...")
            self.game.current_scene = Options(self.game)
        elif self.selected_option == 3:
            # Quitter le jeu
            print("Quitting game...")
            self.game.running = False  # S'assurer que la boucle s'arrête avant d'appeler quit()
        elif self.selected_option == 4:
            # Option pour revenir au menu principal
            print("Returning to main menu...")
            self.game.current_scene = Menu(self.game)
        elif self.selected_option == 5:
            # Option pour recommencer le niveau
            print("Restarting level...")
            self.game.current_scene = Level(self.game, level_number=1)

    # Ajouter cette fonction à la classe Menu

    def draw_highscores(self, screen):
        if not self.game.best_times:
            return
            
        screen_width, screen_height = screen.get_width(), screen.get_height()
        
        # Afficher le titre des meilleurs temps
        title_font = pygame.font.SysFont('Arial', 30)
        title_text = title_font.render("Meilleurs Temps", True, (255, 255, 0))
        screen.blit(title_text, (screen_width - 300, 150))
        
        # Afficher les meilleurs temps pour chaque niveau
        score_font = pygame.font.SysFont('Arial', 25)
        y_offset = 190
        
        # Calculer la somme totale des temps
        total_time = 0
        
        for level_id, time in sorted(self.game.best_times.items()):
            level_num = level_id.split('_')[1]
            score_text = score_font.render(
                f"Niveau {level_num}: {self.game.format_time(time)}", 
                True, (200, 200, 200)
            )
            screen.blit(score_text, (screen_width - 300, y_offset))
            y_offset += 30
            
            # Ajouter ce temps au total
            total_time += time
        
        # Vérifier si tous les niveaux sont complétés
        completed_levels = len(self.game.best_times)

        # Afficher le total seulement si tous les niveaux du dernier lot ont été complétés
        if completed_levels >= self.game.total_levels:
            # Dessiner une ligne de séparation
            pygame.draw.line(
                screen, 
                (200, 200, 200), 
                (screen_width - 300, y_offset), 
                (screen_width - 100, y_offset),
                1
            )
            y_offset += 15
            
            # Afficher le temps total
            total_text = pygame.font.SysFont('Arial', 28).render(
                f"Total: {self.game.format_time(total_time)}", 
                True, (255, 255, 0)
            )
            screen.blit(total_text, (screen_width - 300, y_offset))