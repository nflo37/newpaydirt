import pygame

class PlaysheetWindow:
    """A separate window to display the playsheet"""
    
    def __init__(self, width=400, height=600):
        self.width = width
        self.height = height
        self.screen = None
        
        # Define colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (200, 200, 200)
        self.LIGHT_GREEN = (144, 238, 144)  # Positive yardage plays
        self.LIGHT_RED = (255, 160, 160)    # Negative yardage plays
        self.DARK_GRAY = (50, 50, 50)       # Header background
        
        # Font
        pygame.font.init()  # Make sure fonts are initialized
        self.title_font = pygame.font.SysFont(None, 32)
        self.header_font = pygame.font.SysFont(None, 24)
        self.play_font = pygame.font.SysFont(None, 20)
        
        # Window state
        self.initialized = False
    
    def initialize(self):
        """Initialize the window when needed"""
        if not self.initialized:
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.NOFRAME)
            pygame.display.set_caption("Playsheet")
            self.initialized = True
    
    def close(self):
        """Close the playsheet window"""
        if self.initialized:
            pygame.display.quit()
            self.initialized = False
    
    def update(self, game_state):
        """Update the playsheet window with current game state"""
        if not self.initialized:
            self.initialize()
        
        # Clear the screen
        self.screen.fill(self.GRAY)
        
        # Determine if user is on offense or defense
        user_on_offense = game_state.play_state == "offense" and game_state.possession == game_state.user_team
        
        # Draw the title
        title_text = "OFFENSE PLAYS" if user_on_offense else "DEFENSE PLAYS"
        title_surface = self.title_font.render(title_text, True, self.WHITE)
        title_rect = pygame.Rect(0, 0, self.width, 40)
        pygame.draw.rect(self.screen, self.DARK_GRAY, title_rect)
        self.screen.blit(title_surface, (self.width // 2 - title_surface.get_width() // 2, 10))
        
        # Get the appropriate play list
        if user_on_offense:
            plays = self.get_offense_plays(game_state)
        else:
            plays = self.get_defense_plays(game_state)
        
        # Header for play columns
        headers = ["Play Name", "Expected Yards"]
        header_y = 50
        col1_x = 20
        col2_x = self.width - 120
        
        # Draw headers
        for i, header in enumerate([headers[0], headers[1]]):
            x_pos = col1_x if i == 0 else col2_x
            header_surface = self.header_font.render(header, True, self.BLACK)
            self.screen.blit(header_surface, (x_pos, header_y))
        
        # Draw horizontal line below headers
        pygame.draw.line(self.screen, self.BLACK, (10, header_y + 25), (self.width - 10, header_y + 25), 2)
        
        # Draw each play with appropriate color based on expected yardage
        y_offset = header_y + 40
        row_height = 30
        
        for i, play in enumerate(plays):
            play_name = play.get('name', f"Play {i+1}")
            expected_yards = play.get('expected_yards', 0)
            
            # Choose color based on yardage
            if expected_yards > 0:
                color = self.LIGHT_GREEN
            elif expected_yards < 0:
                color = self.LIGHT_RED
            else:
                color = self.WHITE
            
            # Draw row background
            row_rect = pygame.Rect(10, y_offset, self.width - 20, row_height)
            pygame.draw.rect(self.screen, color, row_rect)
            pygame.draw.rect(self.screen, self.BLACK, row_rect, 1)  # Border
            
            # Draw play name
            name_surface = self.play_font.render(play_name, True, self.BLACK)
            self.screen.blit(name_surface, (col1_x, y_offset + 6))
            
            # Draw expected yards
            yards_text = f"{expected_yards:+d}" if expected_yards != 0 else "0"
            yards_surface = self.play_font.render(yards_text, True, self.BLACK)
            self.screen.blit(yards_surface, (col2_x, y_offset + 6))
            
            y_offset += row_height + 2
            
            # Check if we need to add a scroll mechanism (for future implementation)
            if y_offset > self.height - 40:
                more_text = self.play_font.render("...", True, self.BLACK)
                self.screen.blit(more_text, (self.width // 2, y_offset))
                break
        
        # Add a close button
        close_rect = pygame.Rect(self.width - 60, 5, 50, 30)
        pygame.draw.rect(self.screen, self.LIGHT_RED, close_rect)
        pygame.draw.rect(self.screen, self.BLACK, close_rect, 1)
        close_text = self.play_font.render("Close", True, self.BLACK)
        self.screen.blit(close_text, (self.width - 45, 12))
        
        # Update the display
        pygame.display.flip()
        
        # Handle events for this window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if close button was clicked
                if close_rect.collidepoint(event.pos):
                    self.close()
    
    def get_offense_plays(self, game_state):
        """Get the list of offensive plays with expected yardage"""
        # Check if game state has offense_plays, otherwise return samples
        if hasattr(game_state, 'offense_plays'):
            return game_state.offense_plays
        
        # Create samples based on actual play names from the game
        return [
            {'name': 'Line Plunge', 'expected_yards': 3},
            {'name': 'Off Tackle', 'expected_yards': 4},
            {'name': 'End Run', 'expected_yards': 5},
            {'name': 'Draw', 'expected_yards': 6},
            {'name': 'Screen', 'expected_yards': 7},
            {'name': 'Short Pass', 'expected_yards': 10},
            {'name': 'Medium Pass', 'expected_yards': 15},
            {'name': 'Long', 'expected_yards': 20},
            {'name': 'Sideline', 'expected_yards': 8},
            {'name': 'Field Goal', 'expected_yards': 3},
            {'name': 'Punt', 'expected_yards': 0},
        ]
    
    def get_defense_plays(self, game_state):
        """Get the list of defensive plays with expected yardage"""
        # Check if game state has defense_plays, otherwise return samples
        if hasattr(game_state, 'defense_plays'):
            return game_state.defense_plays
        
        # Create samples based on actual play names from the game
        return [
            {'name': 'Standard', 'expected_yards': 0},
            {'name': 'Nickel', 'expected_yards': -1},
            {'name': 'Dime', 'expected_yards': -2},
            {'name': 'Prevent', 'expected_yards': 2},
            {'name': 'Blitz', 'expected_yards': -3},
        ]

class FootballField:
    
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height
        
        # Define colors
        self.GREEN = (34, 139, 34)   # Field green
        self.WHITE = (255, 255, 255) # Yard lines, hash marks
        self.RED = (200, 0, 0)       # Left end zone
        self.BLUE = (0, 0, 200)      # Right end zone
        self.YELLOW = (255, 255, 0)  # First down marker
        self.BLACK = (0, 0, 0)       # Background/text
        self.GRAY = (128, 128, 128)  # Scoreboard background
        self.LIGHT_GREEN = (144, 238, 144)  # Positive yardage plays
        self.LIGHT_RED = (255, 160, 160)    # Negative yardage plays
        
        # Load and scale the football image
        try:
            self.ball_img = pygame.image.load("assets/football.png").convert_alpha()
            # Scale the image to be approximately 20x12 pixels
            self.ball_img = pygame.transform.scale(self.ball_img, (50, 40))
        except pygame.error:
            print("Warning: Could not load football image. Using circle instead.")
            self.ball_img = None
        
        # Field dimensions
        self.SCOREBOARD_HEIGHT = 100
        self.FIELD_HEIGHT = self.height - self.SCOREBOARD_HEIGHT
        self.ENDZONE_WIDTH = 50
        self.YARD_WIDTH = (self.width - 2 * self.ENDZONE_WIDTH) / 100  # Each yard is 7 pixels
        
        # Create font
        self.font = pygame.font.SysFont(None, 24)

        # Add animation variables
        self.current_ball_x = self.ENDZONE_WIDTH + 50 * self.YARD_WIDTH  # Start at midfield
        self.target_ball_x = self.current_ball_x
        self.animation_speed = 0.1  # Adjust this to control animation speed (0.1 = 10% of distance per frame)

    def draw(self, game_state):
        """Draw the complete field with current game state"""
        # Update target position
        target_x = self.ENDZONE_WIDTH + ((game_state.ball_position + 50) * self.YARD_WIDTH)
        self.target_ball_x = target_x
        
        # If ball needs to move, animate it
        if abs(self.current_ball_x - self.target_ball_x) > 1:
            self.animate_ball_movement(game_state)
        else:
            # Otherwise just render once
            self._render_frame(game_state)

    def _render_frame(self, game_state):
        """Helper method to draw a single frame"""
        self.screen.fill(self.BLACK)
        self.draw_field()
        self.draw_first_down_marker(game_state)
        self.draw_ball(game_state.ball_position, game_state)
        self.draw_scoreboard(game_state)
        self.draw_playsheet(game_state)
        pygame.display.flip()

    def draw_field(self):
        """Draw the basic field with yard lines"""
        # Draw main field (green background)
        field_rect = pygame.Rect(0, self.SCOREBOARD_HEIGHT, self.width, self.FIELD_HEIGHT)
        pygame.draw.rect(self.screen, self.GREEN, field_rect)
        
        # Draw end zones
        left_endzone = pygame.Rect(0, self.SCOREBOARD_HEIGHT, self.ENDZONE_WIDTH, self.FIELD_HEIGHT)
        right_endzone = pygame.Rect(self.width - self.ENDZONE_WIDTH, self.SCOREBOARD_HEIGHT, 
                                  self.ENDZONE_WIDTH, self.FIELD_HEIGHT)
        pygame.draw.rect(self.screen, self.RED, left_endzone)
        pygame.draw.rect(self.screen, self.BLUE, right_endzone)
        
        # Draw yard lines
        for yard in range(10, 100, 10):
            x_pos = self.ENDZONE_WIDTH + (yard * self.YARD_WIDTH)
            pygame.draw.line(self.screen, self.WHITE, 
                           (x_pos, self.SCOREBOARD_HEIGHT),
                           (x_pos, self.height),
                           2)
            
            # Draw yard numbers
            yard_num = str(yard if yard <= 50 else 100 - yard)
            text = self.font.render(yard_num, True, self.WHITE)
            self.screen.blit(text, (x_pos - 10, self.SCOREBOARD_HEIGHT + 10))

    def draw_ball(self, ball_position, game_state):
        """Draw the ball at its current position"""
        y_pos = self.height - self.FIELD_HEIGHT/2
        
        if self.ball_img:
            ball_rect = self.ball_img.get_rect()
            
            # Align the ball based on direction
            if game_state.direction == "right":
                ball_rect.midright = (int(self.current_ball_x), int(y_pos))
            else:
                ball_rect.midleft = (int(self.current_ball_x), int(y_pos))
            
            self.screen.blit(self.ball_img, ball_rect)
        else:
            pygame.draw.circle(self.screen, (255, 255, 0), (int(self.current_ball_x), int(y_pos)), 5)

    def draw_scoreboard(self, game_state):
        """Draw the scoreboard section"""
        # Draw scoreboard background
        score_rect = pygame.Rect(0, 0, self.width, self.SCOREBOARD_HEIGHT)
        pygame.draw.rect(self.screen, self.GRAY, score_rect)
        
        # Draw scores
        score_text = f"{game_state.user_team.name}: {game_state.user_team.score}  vs  {game_state.comp_team.name}: {game_state.comp_team.score}"
        time_text = f"Time: {game_state.seconds // 60}:{game_state.seconds % 60:02d}"
        down_text = f"{game_state.down} and {game_state.distance} on {game_state.convert_yardage()}"
        
        score = self.font.render(score_text, True, self.BLACK)
        time = self.font.render(time_text, True, self.BLACK)
        down = self.font.render(down_text, True, self.BLACK)
        
        self.screen.blit(score, (20, 20))
        self.screen.blit(time, (20, 45))
        self.screen.blit(down, (20, 70))

    def draw_first_down_marker(self, game_state):
        """Draw the first down marker line"""
        # Calculate the first down position based on ball position and distance
        if abs(game_state.ball_position) > 40 or abs(game_state.ball_position) < -40:
            self.first_down_pos = False
        else:
            if game_state.direction == "left" and game_state.down == 1:
                self.first_down_pos = game_state.ball_position - 10
            elif game_state.direction == "right" and game_state.down == 1:
                self.first_down_pos = game_state.ball_position + 10
        
            # Convert first down position to screen coordinates1
            x_pos = self.ENDZONE_WIDTH + ((self.first_down_pos + 50) * self.YARD_WIDTH)
            
            # Draw a semi-transparent yellow line across the field
            line_surface = pygame.Surface((3, self.FIELD_HEIGHT))
            line_surface.fill(self.YELLOW)
            line_surface.set_alpha(128)  # Make it semi-transparent
            
            self.screen.blit(line_surface, (x_pos - 1, self.SCOREBOARD_HEIGHT))

    def animate_ball_movement(self, game_state):
        """Animate the ball moving to its new position"""
        # Keep animating until we're very close to the target
        while abs(self.current_ball_x - self.target_ball_x) > 1:
            # Update ball position
            dx = self.target_ball_x - self.current_ball_x
            self.current_ball_x += dx * self.animation_speed
            
            # Draw the current frame
            self._render_frame(game_state)
            
            # Control animation speed
            pygame.time.wait(33)  # About 30 FPS
            
            # Process events to keep the window responsive
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

    def draw_playsheet(self, game_state):
        """Draw the playsheet panel based on offense/defense state"""
        # Determine if user is on offense or defense
        user_on_offense = game_state.user_on_offense
        
        # Create a semi-transparent panel on the right side
        panel_width = 200
        panel_height = self.FIELD_HEIGHT
        panel_x = self.width - panel_width
        panel_y = self.SCOREBOARD_HEIGHT
        
        # Draw the panel background
        panel_surface = pygame.Surface((panel_width, panel_height))
        panel_surface.fill(self.GRAY)
        panel_surface.set_alpha(200)  # Semi-transparent
        self.screen.blit(panel_surface, (panel_x, panel_y))
        
        # Draw the title
        title_text = "OFFENSE PLAYS" if user_on_offense else "DEFENSE PLAYS"
        title = pygame.font.SysFont(None, 28).render(title_text, True, self.BLACK)
        self.screen.blit(title, (panel_x + 10, panel_y + 10))
        
        # Get the appropriate play list
        if user_on_offense:
            plays = game_state.offense_plays if hasattr(game_state, 'offense_plays') else self.get_sample_offense_plays()
        else:
            plays = game_state.defense_plays if hasattr(game_state, 'defense_plays') else self.get_sample_defense_plays()
        
        # Draw each play with appropriate color based on expected yardage
        y_offset = 50
        for i, play in enumerate(plays):
            play_name = play.get('name', f"Play {i+1}")
            expected_yards = play.get('expected_yards', 0)
            
            # Choose color based on yardage
            if expected_yards > 0:
                color = self.LIGHT_GREEN
            elif expected_yards < 0:
                color = self.LIGHT_RED
            else:
                color = self.WHITE
            
            # Draw the play button
            button_rect = pygame.Rect(panel_x + 10, panel_y + y_offset, panel_width - 20, 30)
            pygame.draw.rect(self.screen, color, button_rect)
            pygame.draw.rect(self.screen, self.BLACK, button_rect, 1)  # Border
            
            # Draw play text
            play_text = f"{play_name} ({expected_yards:+d} yds)"
            text = self.font.render(play_text, True, self.BLACK)
            self.screen.blit(text, (panel_x + 15, panel_y + y_offset + 8))
            
            y_offset += 35
            
            # Stop if we run out of space
            if y_offset > panel_height - 40:
                more_text = self.font.render("...", True, self.BLACK)
                self.screen.blit(more_text, (panel_x + panel_width//2, panel_y + y_offset))
                break
    
    def get_sample_offense_plays(self):
        """Return sample offense plays if game_state doesn't provide them"""
        return [
            {'name': 'QB Sneak', 'expected_yards': 2},
            {'name': 'Inside Run', 'expected_yards': 4},
            {'name': 'Power Run', 'expected_yards': 3},
            {'name': 'Outside Run', 'expected_yards': 6},
            {'name': 'Short Pass', 'expected_yards': 5},
            {'name': 'Medium Pass', 'expected_yards': 10},
            {'name': 'Deep Pass', 'expected_yards': 20},
            {'name': 'Screen Pass', 'expected_yards': 5},
            {'name': 'Play Action', 'expected_yards': 15},
            {'name': 'Draw Play', 'expected_yards': 4},
            {'name': 'Option Run', 'expected_yards': 7},
            {'name': 'Hail Mary', 'expected_yards': 30},
        ]
    
    def get_sample_defense_plays(self):
        """Return sample defense plays if game_state doesn't provide them"""
        return [
            {'name': 'Goal Line Defense', 'expected_yards': -1},
            {'name': 'Run Blitz', 'expected_yards': 0},
            {'name': 'Pass Blitz', 'expected_yards': -2},
            {'name': 'Zone Coverage', 'expected_yards': 2},
            {'name': 'Man Coverage', 'expected_yards': 0},
            {'name': 'Cover 2', 'expected_yards': 1},
            {'name': 'Cover 3', 'expected_yards': 2},
            {'name': 'Prevent Defense', 'expected_yards': 5},
            {'name': 'Nickel Package', 'expected_yards': 3},
            {'name': 'Dime Package', 'expected_yards': 4},
        ]

