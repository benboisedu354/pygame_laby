import pygame
from src.scenes.menu import Menu
import json
import os

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        pygame.display.set_caption("Pygame Game")
        self.clock = pygame.time.Clock()
        self.running = True
        self.current_scene = None
        
        # Variables pour le timer
        self.timer_running = False
        self.start_time = 0
        self.current_time = 0
        self.best_times = {}
        
        # Variable pour stocker le nombre total de niveaux à jouer
        self.total_levels = 3  # Valeur par défaut
        
        # Charger les scores sauvegardés
        self.load_scores()
        
        # Initialiser le menu et la scène courante
        self.menu = Menu(self)
        self.current_scene = self.menu  # Par défaut, on commence par le menu

    def run(self):
        while self.running:
            try:
                events = pygame.event.get()
                self.handle_events(events)
                
                # Mise à jour du timer si actif
                if self.timer_running:
                    self.current_time = pygame.time.get_ticks() - self.start_time
                
                # Mise à jour et affichage de la scène courante
                if self.current_scene and pygame.get_init():  # Vérifier que pygame est initialisé
                    self.current_scene.update(events)
                    self.current_scene.draw(self.screen)
                
                pygame.display.flip()
                self.clock.tick(60)
            except pygame.error:
                # En cas d'erreur liée à pygame (comme surface fermée), sortir de la boucle
                self.running = False
                break

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False

    def quit(self):
        """Quitte le jeu en sauvegardant les scores"""
        self.save_scores()  # Sauvegarde avant de fermer
        self.running = False  # S'assurer que la boucle principale s'arrête
        pygame.quit()  # Fermer pygame
        
    def start_timer(self):
        """Démarre le timer pour un nouveau niveau"""
        self.timer_running = True
        self.start_time = pygame.time.get_ticks()
        self.current_time = 0
    
    def stop_timer(self, level_id=None):
        """Arrête le timer et enregistre le temps si c'est un record"""
        if not self.timer_running:
            return
            
        self.timer_running = False
        final_time = self.current_time
        
        # Enregistrer le meilleur temps pour ce niveau
        if level_id and (level_id not in self.best_times or final_time < self.best_times[level_id]):
            self.best_times[level_id] = final_time
            # Sauvegarder immédiatement les scores
            self.save_scores()
            return True  # Indique un nouveau record
        return False

    def format_time(self, milliseconds):
        """Convertit les millisecondes en format lisible MM:SS:MS"""
        seconds = milliseconds // 1000
        ms = milliseconds % 1000
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02}:{seconds:02}:{ms//10:02}"
    
    def save_scores(self):
        """Sauvegarde les meilleurs temps dans un fichier JSON"""
        try:
            # Convertir les clés en chaînes pour le JSON
            scores_data = {str(key): value for key, value in self.best_times.items()}
            
            # Créer le dossier de sauvegarde s'il n'existe pas
            save_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "save")
            os.makedirs(save_dir, exist_ok=True)
            
            # Chemin du fichier de sauvegarde
            save_path = os.path.join(save_dir, "high_scores.json")
            
            # Écrire les données dans le fichier
            with open(save_path, 'w') as f:
                json.dump(scores_data, f)
                
            print(f"Scores sauvegardés dans {save_path}")
            return True
        except Exception as e:
            print(f"Erreur lors de la sauvegarde des scores: {e}")
            return False

    def load_scores(self):
        """Charge les meilleurs temps depuis un fichier JSON"""
        try:
            save_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "save", "high_scores.json")
            
            if not os.path.exists(save_path):
                print("Aucun fichier de scores trouvé")
                return False
                
            with open(save_path, 'r') as f:
                scores_data = json.load(f)
                
            # Convertir les clés en format approprié (ajoutez des conversions si nécessaire)
            self.best_times = {key: value for key, value in scores_data.items()}
            
            print(f"Scores chargés depuis {save_path}")
            return True
        except Exception as e:
            print(f"Erreur lors du chargement des scores: {e}")
            return False

if __name__ == "__main__":
    game = Game()
    game.run()
    game.quit()