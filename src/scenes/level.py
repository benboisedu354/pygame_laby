import pygame
import random

class Level:
    def __init__(self, game, level_number=1):
        self.game = game
        self.level_number = level_number
        self.font = pygame.font.SysFont('Arial', 30)
        self.background_color = (0, 0, 0)  # Fond noir
        
        # Dimensions du labyrinthe
        self.grid_width = 15
        self.grid_height = 10
        self.cell_size = 60
        
        # Position du joueur
        self.player_x = 1
        self.player_y = 1
        
        # Position de sortie
        self.exit_x = self.grid_width - 2
        self.exit_y = self.grid_height - 2
        
        # Génération du labyrinthe
        self.maze = self.generate_maze()
        
        # Démarrer le timer pour ce niveau
        self.game.start_timer()
        
        # Variables pour afficher le message de complétion
        self.completed = False
        self.completion_time = 0
        self.is_new_record = False
        self.show_completion_message = False
        
        print(f"Niveau {level_number} créé - Labyrinthe généré")
    
    def generate_maze(self):
        # Initialisation du labyrinthe (1 = mur, 0 = chemin)
        maze = [[1 for _ in range(self.grid_width)] for _ in range(self.grid_height)]
        
        # Algorithme de génération de labyrinthe simplifié
        def carve_path(x, y):
            # Marquer cette cellule comme chemin
            maze[y][x] = 0
            
            # Directions possibles: haut, droite, bas, gauche
            directions = [(0, -2), (2, 0), (0, 2), (-2, 0)]
            random.shuffle(directions)
            
            # Essayer chaque direction
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                
                # Vérifier si on est dans les limites et si la cellule n'a pas été visitée
                if (0 <= new_x < self.grid_width and 0 <= new_y < self.grid_height and 
                    maze[new_y][new_x] == 1):
                    # Abattre le mur entre les deux cellules
                    maze[y + dy//2][x + dx//2] = 0
                    carve_path(new_x, new_y)
        
        # Commencer au point (1,1)
        carve_path(1, 1)
        
        # S'assurer que l'entrée et la sortie sont des chemins
        maze[1][1] = 0  # Entrée
        maze[self.exit_y][self.exit_x] = 0  # Sortie
        
        return maze
    
    def draw(self, screen):
        # Effacer l'écran avec la couleur de fond
        screen.fill(self.background_color)
        
        # Calculer le décalage pour centrer le labyrinthe
        offset_x = (screen.get_width() - self.grid_width * self.cell_size) // 2
        offset_y = (screen.get_height() - self.grid_height * self.cell_size) // 2
        
        # Dessiner le labyrinthe
        for y in range(self.grid_height):
            for x in range(self.grid_width):
                rect = pygame.Rect(
                    offset_x + x * self.cell_size, 
                    offset_y + y * self.cell_size, 
                    self.cell_size, 
                    self.cell_size
                )
                
                if self.maze[y][x] == 1:
                    # Mur
                    pygame.draw.rect(screen, (50, 50, 100), rect)
                else:
                    # Chemin
                    pygame.draw.rect(screen, (20, 20, 30), rect)
                    
                # Dessiner une bordure fine
                pygame.draw.rect(screen, (40, 40, 70), rect, 1)
        
        # Dessiner la sortie
        exit_rect = pygame.Rect(
            offset_x + self.exit_x * self.cell_size,
            offset_y + self.exit_y * self.cell_size,
            self.cell_size,
            self.cell_size
        )
        pygame.draw.rect(screen, (0, 200, 0), exit_rect)
        
        # Dessiner le joueur
        player_rect = pygame.Rect(
            offset_x + self.player_x * self.cell_size + self.cell_size // 4,
            offset_y + self.player_y * self.cell_size + self.cell_size // 4,
            self.cell_size // 2,
            self.cell_size // 2
        )
        pygame.draw.rect(screen, (255, 0, 0), player_rect)
        
        # Afficher le chronomètre
        timer_text = self.font.render(f"Temps: {self.game.format_time(self.game.current_time)}", True, (255, 255, 255))
        screen.blit(timer_text, (20, 20))
        
        # Afficher le meilleur temps si disponible
        level_id = f"level_{self.level_number}"
        if level_id in self.game.best_times:
            best_time = self.game.format_time(self.game.best_times[level_id])
            best_time_text = self.font.render(f"Record: {best_time}", True, (255, 255, 0))
            screen.blit(best_time_text, (20, 60))
        
        # Afficher les instructions
        instructions = self.font.render("Utilisez les flèches pour vous déplacer", True, (255, 255, 255))
        screen.blit(instructions, (screen.get_width() - instructions.get_width() - 20, 20))
        
        # Afficher le message pour revenir au menu
        esc_text = self.font.render("Appuyez sur ESC pour revenir au menu", True, (200, 200, 200))
        screen.blit(esc_text, (20, screen.get_height() - 50))
        
        # Afficher message de complétion si niveau terminé
        if self.show_completion_message:
            # Créer un fond semi-transparent
            overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Noir semi-transparent
            screen.blit(overlay, (0, 0))
            
            # Afficher les messages
            completion_text = self.font.render(
                f"Niveau {self.level_number} terminé! Temps: {self.game.format_time(self.completion_time)}", 
                True, (255, 255, 255)
            )
            
            record_color = (0, 255, 0) if self.is_new_record else (255, 255, 0)
            record_message = "NOUVEAU RECORD!" if self.is_new_record else "Appuyez sur Entrée pour continuer"
            record_text = self.font.render(record_message, True, record_color)
            
            screen.blit(completion_text, (screen.get_width()//2 - completion_text.get_width()//2, screen.get_height()//2 - 50))
            screen.blit(record_text, (screen.get_width()//2 - record_text.get_width()//2, screen.get_height()//2))

    def update(self, events):
        if self.show_completion_message:
            for event in events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.proceed_after_completion()
            return
            
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Arrêter le timer et retourner au menu
                    self.game.stop_timer()
                    from src.scenes.menu import Menu
                    self.game.current_scene = Menu(self.game)
                
                # Déplacement du joueur
                new_x, new_y = self.player_x, self.player_y
                
                if event.key == pygame.K_UP:
                    new_y -= 1
                elif event.key == pygame.K_RIGHT:
                    new_x += 1
                elif event.key == pygame.K_DOWN:
                    new_y += 1
                elif event.key == pygame.K_LEFT:
                    new_x -= 1
                
                # Vérifier si le mouvement est valide
                if (0 <= new_x < self.grid_width and 
                    0 <= new_y < self.grid_height and 
                    self.maze[new_y][new_x] == 0):
                    self.player_x, self.player_y = new_x, new_y
                
                # Vérifier si le joueur a atteint la sortie
                if self.player_x == self.exit_x and self.player_y == self.exit_y:
                    self.level_completed()
    
    def level_completed(self):
        # Enregistrer le temps et vérifier si c'est un record
        self.completion_time = self.game.current_time
        level_id = f"level_{self.level_number}"
        self.is_new_record = self.game.stop_timer(level_id)
        self.completed = True
        self.show_completion_message = True
    
    def proceed_after_completion(self):
        # Passer au niveau suivant ou afficher un message de victoire
        next_level = self.level_number + 1
        
        if next_level <= self.game.total_levels:  # Utiliser la variable dynamique
            self.game.current_scene = Level(self.game, level_number=next_level)
        else:
            # Retour au menu avec un message de félicitations
            from src.scenes.menu import Menu
            self.game.current_scene = Menu(self.game, show_victory=True)