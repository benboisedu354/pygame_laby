import pygame

class Options:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont('Arial', 30)
        self.options = ["Volume: 50%", "Difficulté: Normal", "Retour"]
        self.selected_option = 0

    def draw(self, screen):
        screen.fill((0, 0, 50))  # Fond bleu foncé
        
        # Titre
        title_font = pygame.font.SysFont('Arial', 50)
        title_surface = title_font.render("Options", True, (255, 255, 0))
        screen.blit(title_surface, (100, 30))
        
        # Afficher les options
        for index, option in enumerate(self.options):
            color = (255, 255, 255) if index == self.selected_option else (100, 100, 100)
            text_surface = self.font.render(option, True, color)
            screen.blit(text_surface, (100, 100 + index * 40))



    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_option = (self.selected_option - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.selected_option = (self.selected_option + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    self.select_option()
                # Ajout de contrôles gauche/droite pour modifier les options
                elif event.key == pygame.K_LEFT:
                    self.adjust_option(-1)
                elif event.key == pygame.K_RIGHT:
                    self.adjust_option(1)

    def select_option(self):
        if self.selected_option == 2:  # Option "Retour"
            from src.scenes.menu import Menu
            self.game.current_scene = Menu(self.game)

    def adjust_option(self, direction):
        if self.selected_option == 0:  # Volume
            current_volume = int(self.options[0].split(": ")[1].replace("%", ""))
            new_volume = max(0, min(100, current_volume + direction * 10))
            self.options[0] = f"Volume: {new_volume}%"
        elif self.selected_option == 1:  # Difficulté
            difficulties = ["Facile", "Normal", "Difficile"]
            current_diff = self.options[1].split(": ")[1]
            current_index = difficulties.index(current_diff)
            new_index = (current_index + direction) % len(difficulties)
            self.options[1] = f"Difficulté: {difficulties[new_index]}"