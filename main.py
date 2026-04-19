import pygame
import json
import sys
import multiprocessing
import Stats  # To access graphing functions
from database.db_manager import db_function as db #need db access
from Game import SudokuGame # The actual game logic.    
import logging

logging.basicConfig(
    level=logging.INFO,
    filename='pydoku.log',
    filemode='a',
    format='%(asctime)s | %(name)-15s | %(levelname)-8s | %(message)s',
    datefmt='%H:%M:%S',
)

class Button:
    def __init__(self, x, y, w, h, text, color, text_color):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.font = pygame.font.SysFont("Arial", 28, bold=True)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        txt_surf = self.font.render(self.text, True, self.text_color)
        txt_rect = txt_surf.get_rect(center=self.rect.center)
        screen.blit(txt_surf, txt_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False

class Slider:
    def __init__(self, x, y, w, min_val, max_val, label, initial_val, color):
        self.rect = pygame.Rect(x, y, w, 10)
        self.handle_rect = pygame.Rect(x, y - 10, 20, 30)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.color = color
        self.font = pygame.font.SysFont("Arial", 20, bold=True)
        
        # Set initial position
        pos = x + (initial_val - min_val) / (max_val - min_val) * w
        self.handle_rect.centerx = pos

    def draw(self, screen):
        pygame.draw.rect(screen, (200, 200, 200), self.rect) # Track
        pygame.draw.rect(screen, self.color, self.handle_rect) # Handle
        txt = self.font.render(f"{self.label}: {int(self.value)}", True, (255, 255, 255))
        screen.blit(txt, (self.rect.x, self.rect.y - 35))

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN or (event.type == pygame.MOUSEMOTION and event.buttons[0]):
            if self.rect.collidepoint(event.pos) or self.handle_rect.collidepoint(event.pos):
                self.handle_rect.centerx = max(self.rect.left, min(event.pos[0], self.rect.right))
                pos_ratio = (self.handle_rect.centerx - self.rect.left) / self.rect.width
                self.value = self.min_val + pos_ratio * (self.max_val - self.min_val)
                return True
        return False

class Pydoku:
    def __init__(self) -> None:
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        pygame.init()
        self.logger.info("Initiated Pygame")
        self.load_settings()
        self.logger.info("Successfuly Loaded Settings")
        
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("PyDoku")
        self.clock = pygame.time.Clock()
        
        self.state = "HOME"
        self.running = True
        self.game = None 
        self.selected_cell = None 

        # UI Constants
        self.cell_size = 50
        self.grid_offset_x = (self.width - (self.cell_size * 9)) // 2
        self.grid_offset_y = 150
        
        btn_w, btn_h = 240, 60
        center_x = (self.width // 2) - (btn_w // 2)
        self.scroll_y = 0
        
        self.title_font = pygame.font.SysFont("Arial", 64, bold=True)
        self.num_font = pygame.font.SysFont("Arial", 32)
        
        # In game buttons
        self.back_btn = Button(20, 20, 100, 40, "Back", self.colors['primary'], (255, 255, 255))
        self.save_btn = Button(center_x, 500, btn_w, btn_h, "Save Settings", self.colors['primary'], (255,255,255))
        side_btn_x = self.grid_offset_x + (9 * self.cell_size) + 30
        self.check_btn = Button(side_btn_x, 250, 140, 50, "Check", self.colors['secondary'], (255, 255, 255))
        self.save_game_btn = Button(side_btn_x, 320, 140, 50, "Save", self.colors['primary'], (255, 255, 255))
        
        self.show_errors = False
        
        # Updated Navigation Buttons
        self.play_btn = Button(center_x, 260, btn_w, btn_h, "New Game", self.colors['primary'], (255,255,255))
        self.prev_btn = Button(center_x, 340, btn_w, btn_h, "Previous Game", self.colors['secondary'], (255,255,255))
        self.stats_btn = Button(center_x, 420, btn_w, btn_h, "Statistics", self.colors['secondary'], (255,255,255))
        self.opts_btn = Button(center_x, 500, btn_w, btn_h, "Options", self.colors['tertiary'], (0,0,0))

        # Stats Screen Specific Buttons
        self.stat_time_btn = Button(center_x, 300, btn_w, btn_h, "Play Time", self.colors['secondary'], (255,255,255))
        self.stat_error_btn = Button(center_x, 380, btn_w, btn_h, "Error Rates", self.colors['tertiary'], (0,0,0))
        self.stat_diff_btn = Button(center_x, 460, btn_w, btn_h, "Difficulty", self.colors['fourth'], (0,0,0))

        # Timer UI
        self.TIMER_EVENT = pygame.USEREVENT + 1
        # Increment every second
        pygame.time.set_timer(self.TIMER_EVENT, 1000) 
        
        slider_w = 300
        start_x = (self.width - slider_w) // 2
        self.vol_slider = Slider(start_x, 300, slider_w, 0, 100, "Volume", self.volume * 100, self.colors['secondary'])
        self.diff_slider = Slider(start_x, 400, slider_w, 10, 70, "Difficulty", self.difficulty, self.colors['tertiary'])
        # Elijah can change to what he desires  
        self.timer_font = pygame.font.SysFont("Arial", 32)

        # Create our music object
        pygame.mixer.init()
        pygame.mixer.music.load("music.mp3") 
        pygame.mixer.music.set_volume(self.volume)
        # Loop forever
        pygame.mixer.music.play(-1)  
        
        #win button
        self.win_btn = Button(center_x, 400, btn_w, btn_h, "Back to Menu", self.colors['primary'], (255,255,255))

    def load_settings(self) -> None:
        # We are making default json settings so we may populate a potential non existing file.
        default_settings = {
            "colors": {
                "primary": [174, 224, 255],
                "background": [82, 72, 168],
                "secondary": [105, 118, 250],
                "tertiary": [221, 180, 255],
                "fourth": [96, 213, 255]
            },
            "window": {
                "width": 800,
                "height": 800,
                "fps": 60
            },
            "gameplay": {
                "volume": 0.19,
                "difficulty": 10
            },
        }
        try:
            with open('settings.json', 'r') as f:
                data = json.load(f)
                self.logger.info("Loading Settings...")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # If the file does not exist use the default_settings to mak the new file.
            self.logger.warning("settings.json could not be found making default settings.")
            data = default_settings
            with open('settings.json', 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            self.logger.error(f"Unexpected Error: {e}")
        
        # Get the settings present within waht can be oaded.
        self.colors = data['colors']
        self.width = data['window']['width']
        self.height = data['window']['height']
        self.fps = data['window']['fps']
        # new update for options
        gameplay = data.get('gameplay', {})
        self.volume = gameplay.get('volume', 0.5)
        self.difficulty = gameplay.get('difficulty', 40)
        
    def save_settings(self):
            data = {
                "colors": self.colors,
                "window": {"width": self.width, "height": self.height, "fps": self.fps},
                "gameplay": {
                    "volume": round(self.volume, 2),
                    "difficulty": self.difficulty
                }
            }
            try:
                with open('settings.json', 'w') as f:
                    json.dump(data, f, indent=4)
            except PermissionError as e:
                self.logger.error(f"Permission error: {e}")
            except OSError as e:
                self.logger.error(f"Operating System error: {e}")
            except Exception as e:
                self.logger.error(f"Unexpected Error: {e}")
        
    def spawn_stats_process(self, target_func):
        """Spawns a new OS process for Matplotlib to ensure thread-safe GUI rendering"""
        p = multiprocessing.Process(target=target_func)
        p.daemon = True
        p.start()

    def draw_home(self) -> None:
        self.screen.fill(self.colors['background'])
        title_surf = self.title_font.render("PyDoku", True, self.colors['primary'])
        self.screen.blit(title_surf, title_surf.get_rect(center=(self.width // 2, 150)))
        self.play_btn.draw(self.screen)
        self.prev_btn.draw(self.screen) 
        self.stats_btn.draw(self.screen)
        self.opts_btn.draw(self.screen)

    def draw_stats(self) -> None:
        self.screen.fill(self.colors['background'])
        title_surf = self.title_font.render("Statistics", True, self.colors['primary'])
        self.screen.blit(title_surf, title_surf.get_rect(center=(self.width // 2, 150)))
        self.stat_time_btn.draw(self.screen)
        self.stat_error_btn.draw(self.screen)
        self.stat_diff_btn.draw(self.screen)
        self.back_btn.draw(self.screen)

    def draw_game(self) -> None:
        self.screen.fill(self.colors['background'])
        self.back_btn.draw(self.screen)
        
        self.check_btn.draw(self.screen)
        self.save_game_btn.draw(self.screen)
        
        for i in range(10):
            thick = 4 if i % 3 == 0 else 1
            pygame.draw.line(self.screen, self.colors['primary'], 
                             (self.grid_offset_x + i * self.cell_size, self.grid_offset_y), 
                             (self.grid_offset_x + i * self.cell_size, self.grid_offset_y + 9 * self.cell_size), thick)
            pygame.draw.line(self.screen, self.colors['primary'], 
                             (self.grid_offset_x, self.grid_offset_y + i * self.cell_size), 
                             (self.grid_offset_x + 9 * self.cell_size, self.grid_offset_y + i * self.cell_size), thick)

        if self.selected_cell:
            r, c = self.selected_cell
            sel_rect = pygame.Rect(self.grid_offset_x + c * self.cell_size, self.grid_offset_y + r * self.cell_size, self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, self.colors['fourth'], sel_rect, 3)

        for r in range(9):
            for c in range(9):
                val = self.game.curr[r][c]
                if val != 0:
                    if self.game.initial[r][c] != 0:
                        # Original tile = black
                        color = (0, 0, 0)  
                    elif self.show_errors and val != self.game.solution[r][c]:
                        # Wrong = red
                        color = (255, 0, 0)  
                    else:
                        # User placed = normal color
                        color = self.colors['secondary']  
                    num_surf = self.num_font.render(str(val), True, color)
                    num_rect = num_surf.get_rect(center=(self.grid_offset_x + c * self.cell_size + self.cell_size//2, 
                                                        self.grid_offset_y + r * self.cell_size + self.cell_size//2))
                    self.screen.blit(num_surf, num_rect)

        # Get the current time and seperate it into minute/seconds     
        elapsed_time = self.game.time
        mins, secs = divmod(int(elapsed_time), 60)
        # Create the actual shape and render to the screen 
        time_str = f"{mins:02d}:{secs:02d}"
        time_surf = self.timer_font.render(time_str, True, self.colors['primary'])
        time_rect = time_surf.get_rect(center=(self.width // 2, self.grid_offset_y - 40))
        self.screen.blit(time_surf, time_rect)
        
    def draw_options(self) -> None:
        self.screen.fill(self.colors['background'])
        self.back_btn.draw(self.screen)
        self.vol_slider.draw(self.screen)
        self.diff_slider.draw(self.screen)
        self.save_btn.draw(self.screen)

    def draw_win(self) -> None:
        #put the win button on the screen when someone wins 
        self.screen.fill(self.colors['background'])
        title_surf = self.title_font.render("You Win!", True, self.colors['primary'])
        self.screen.blit(title_surf, title_surf.get_rect(center=(self.width // 2, 200)))
        self.win_btn.draw(self.screen)

    def draw_selection_screen(self):
        self.screen.fill(self.colors['background'])
        self.back_btn.draw(self.screen) # Add the back button because we dnt want to get trapped
        
        # Add Title
        title = self.title_font.render("Choose Game!", True, self.colors['primary'])
        self.screen.blit(title, title.get_rect(center=(self.width // 2, 80)))
        
        # SHow previous games
        for i, selection, in enumerate(self.session_list): # Go through all game from database
            y_pos = 150 + (i * 50) + self.scroll_y
            
            selection_font = pygame.font.SysFont("Arial", 20, bold=True)
            
            # Optimize to only generate what is on screen
            if y_pos > 100 and y_pos < self.height + 50:
                
                btn_rect = pygame.Rect(0,0,500,40)
                btn_rect.center = (self.width // 2, y_pos)
                pygame.draw.rect(self.screen, self.colors['secondary'], btn_rect, border_radius=3)
                
                # Format Session data
                if selection.completion_status == False:
                    color = (255, 255, 255)
                    status_indicator = "Not Compelete"
                else:
                    color = self.colors['tertiary']
                    status_indicator = "Complete"
                    
                    
                session_info = f"ID: {selection.session_id} | DIFFICULTY: {selection.difficulty} | STATUS: {status_indicator}"
                btn_txt = selection_font.render(session_info, True, color)
                rect = btn_txt.get_rect(center=(self.width // 2, y_pos))
                self.screen.blit(btn_txt, rect)

        pygame.draw.rect(self.screen, self.colors['background'], (0, 0, self.width, 130))
        title = self.title_font.render("Choose Game!", True, self.colors['primary'])
        self.screen.blit(title, title.get_rect(center=(self.width // 2, 80)))
        self.back_btn.draw(self.screen)
        
    def run(self) -> None:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if self.state == "HOME":
                    self.handle_home_events(event)
                elif self.state == "GAME":
                    self.handle_game_events(event)
                elif self.state == "STATS":
                    self.handle_stats_events(event)
                elif self.state == "OPTIONS":
                    self.handle_options_events(event)
                #helper call to print to screen
                elif self.state == "WIN":
                    self.handle_win_events(event)
                elif self.state == "SELECT_GAME":
                    self.handle_selection_event(event)

            if self.state == "HOME":
                self.draw_home()
            elif self.state == "GAME":
                self.draw_game()
            elif self.state == "STATS":
                self.draw_stats()
            elif self.state == "OPTIONS":
                self.draw_options()
            #draws the button    
            elif self.state == "WIN":
                self.draw_win()
            elif self.state == "SELECT_GAME":
                self.draw_selection_screen()

            pygame.display.flip()
            self.clock.tick(self.fps)
        pygame.quit()
        sys.exit()

    def handle_home_events(self, event) -> None:
        if self.play_btn.is_clicked(event):
            self.game = SudokuGame(difficulty=self.difficulty)
            self.state = "GAME"
        elif self.prev_btn.is_clicked(event):
            self.session_list = db.get_all_sessions_for_select()
            self.state = "SELECT_GAME"
        elif self.stats_btn.is_clicked(event):
            self.state = "STATS"
        elif self.opts_btn.is_clicked(event):
            self.state = "OPTIONS"

    def handle_stats_events(self, event) -> None:
        if self.back_btn.is_clicked(event):
            self.state = "HOME"
        if self.stat_time_btn.is_clicked(event):
            self.spawn_stats_process(Stats.GamesByTime)
        elif self.stat_error_btn.is_clicked(event):
            self.spawn_stats_process(Stats.ErrorRate)
        elif self.stat_diff_btn.is_clicked(event):
            self.spawn_stats_process(Stats.Difficulty)

    def handle_game_events(self, event) -> None:        
        if self.back_btn.is_clicked(event):
            self.state = "HOME"
            self.selected_cell = None
            return 
        
        #saves game based on button click   
        if self.save_game_btn.is_clicked(event):
            if self.game:
             self.game.SaveGame()

        #prints out what errors you made
        if self.check_btn.is_clicked(event):
            if self.game:
                self.show_errors = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            col = (x - self.grid_offset_x) // self.cell_size
            row = (y - self.grid_offset_y) // self.cell_size
            self.selected_cell = (row, col) if 0 <= row < 9 and 0 <= col < 9 else None
        
        if event.type == pygame.KEYDOWN and self.selected_cell:
            r, c = self.selected_cell
            if pygame.K_1 <= event.key <= pygame.K_9:
                #reset our errors for new board 
                self.show_errors = False 
                self.game.PlaceTile(r, c, event.key - pygame.K_0)
                #check if they won
                if self.game.IsSolved():       
                    self.state = "WIN"
            elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_0:
                self.game.curr[r][c] = 0 

        # Increment our game time 
        if event.type == self.TIMER_EVENT and self.game:
            self.game.time += 1 
            
    def handle_options_events(self, event) -> None:
        if self.back_btn.is_clicked(event):
            self.state = "HOME"
            return
        if self.vol_slider.update(event):
                    self.volume = self.vol_slider.value / 100
                    pygame.mixer.music.set_volume(self.volume)
        
        # difficulty
        if self.diff_slider.update(event):
            self.difficulty = int(round(self.diff_slider.value / 5) * 5)
            
        if self.save_btn.is_clicked(event):
            self.save_settings()
        
        # Vol
        if self.vol_slider.update(event):
            self.volume = self.vol_slider.value / 100
            pygame.mixer.music.set_volume(self.volume)

        if self.save_btn.is_clicked(event):
            self.save_settings()
 
    def handle_win_events(self, event) -> None:
        #handler function to help us set game state and current board 
        if self.win_btn.is_clicked(event):
            self.state = "HOME"
            self.game = None
    
    def handle_selection_event(self, event) -> None:
        """ Handle events in the selection screen """
        
        # Handle Back Button
        if self.back_btn.is_clicked(event):
            self.state = "HOME"
        
        # Allow to scroll down
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_y += event.y * 25
            self.scroll_y = min(0, self.scroll_y)
            height = len(self.session_list) * 50
            if (height > (self.height - 150)):
                self.scroll_y = max(self.scroll_y, -(height - (self.height - 200)))
                
        # Press Events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, selection in enumerate(self.session_list):
                    y_pos = 150 + (i * 50) + self.scroll_y
                    
                    # Create the same rect used in draw_selection_screen
                    click_rect = pygame.Rect(0, 0, 500, 40)
                    click_rect.center = (self.width // 2, y_pos)
                    
                    # Check if click is inside this rect AND below the header
                    if y_pos > 130 and click_rect.collidepoint(event.pos):
                        saved = db.load_selected_game(selection.session_id)
                        if saved:
                            self.game = SudokuGame(
                                initial=saved["initial"],
                                curr=saved["curr"],
                                solution=saved["solution"],
                                notes=saved["notes"],
                                time=saved["time"],
                                difficulty=saved["difficulty"],
                                ID=saved["session_id"]
                            )
                            self.state = "GAME"
                        break
        
        
if __name__ == "__main__":
    app = Pydoku()
    app.run()