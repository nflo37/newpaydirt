

class FootballField:
    
    def __init__(self, screen, width, height):
        self.screen = screen
        self.width = width
        self.height = height


        # Define colors
        GREEN = (34, 139, 34)   # Field green
        WHITE = (255, 255, 255) # Yard lines, hash marks
        RED = (200, 0, 0)       # Left end zone
        BLUE = (0, 0, 200)      # Right end zone
        YELLOW = (255, 255, 0)  # Ball
        BLACK = (0, 0, 0)       # Background text
        GRAY = (128, 128, 128)  # Scoreboard background
        
        # Define scoreboard height (top part of the window)
        SCOREBOARD_HEIGHT = 50
        
        # Define field dimensions (the field occupies the rest of the window)
        FIELD_HEIGHT = HEIGHT - SCOREBOARD_HEIGHT
        
        # End zone width (on the left and right of the field)
        ENDZONE_WIDTH = 50
        
        # Define main field rectangle (the playable area between end zones)
        MAIN_FIELD_RECT = pygame.Rect(ENDZONE_WIDTH, SCOREBOARD_HEIGHT, WIDTH - 2 * ENDZONE_WIDTH, FIELD_HEIGHT)
        
        # Create a font for drawing text (yard numbers, scoreboard)
        font = pygame.font.SysFont(None, 24)

