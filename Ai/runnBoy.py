import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)
GROUND_COLOR = (101, 67, 33)
BOY_COLOR = (255, 200, 100)
OBSTACLE_COLOR = (34, 139, 34)

# Game variables
gravity = 0.8
game_speed = 6

class Player:
    def __init__(self):
        self.width = 40
        self.height = 60
        self.x = 100
        self.y = SCREEN_HEIGHT - 100 - self.height
        self.vel_y = 0
        self.jumping = False
        self.ground_y = SCREEN_HEIGHT - 100 - self.height
        
    def jump(self):
        if not self.jumping:
            self.vel_y = -15
            self.jumping = True
    
    def update(self):
        # Apply gravity
        self.vel_y += gravity
        self.y += self.vel_y
        
        # Check ground collision
        if self.y >= self.ground_y:
            self.y = self.ground_y
            self.vel_y = 0
            self.jumping = False
    
    def draw(self, screen):
        # Draw simple boy character
        # Body
        pygame.draw.rect(screen, BOY_COLOR, (self.x, self.y, self.width, self.height))
        # Head
        pygame.draw.circle(screen, BOY_COLOR, (self.x + self.width // 2, self.y - 15), 15)
        # Eyes
        pygame.draw.circle(screen, BLACK, (self.x + self.width // 2 - 5, self.y - 18), 3)
        pygame.draw.circle(screen, BLACK, (self.x + self.width // 2 + 5, self.y - 18), 3)
        # Legs
        pygame.draw.rect(screen, BLACK, (self.x + 8, self.y + self.height, 8, 10))
        pygame.draw.rect(screen, BLACK, (self.x + 24, self.y + self.height, 8, 10))

class Obstacle:
    def __init__(self):
        self.width = 30
        self.height = random.randint(40, 70)
        self.x = SCREEN_WIDTH
        self.y = SCREEN_HEIGHT - 100 - self.height
        
    def update(self, speed):
        self.x -= speed
    
    def draw(self, screen):
        # Draw cactus-like obstacle
        pygame.draw.rect(screen, OBSTACLE_COLOR, (self.x, self.y, self.width, self.height))
        # Add some spikes
        for i in range(0, self.height, 15):
            pygame.draw.polygon(screen, OBSTACLE_COLOR, 
                              [(self.x - 5, self.y + i + 7),
                               (self.x, self.y + i),
                               (self.x, self.y + i + 14)])
    
    def off_screen(self):
        return self.x < -self.width
    
    def collide(self, player):
        if (player.x + player.width > self.x and 
            player.x < self.x + self.width and
            player.y + player.height > self.y):
            return True
        return False

def draw_ground(screen):
    pygame.draw.rect(screen, GROUND_COLOR, (0, SCREEN_HEIGHT - 100, SCREEN_WIDTH, 100))
    # Draw ground line
    pygame.draw.line(screen, BLACK, (0, SCREEN_HEIGHT - 100), (SCREEN_WIDTH, SCREEN_HEIGHT - 100), 3)

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Running Boy Game")
    clock = pygame.time.Clock()
    
    player = Player()
    obstacles = []
    score = 0
    obstacle_timer = 0
    game_over = False
    current_game_speed = game_speed
    
    font = pygame.font.Font(None, 36)
    
    running = True
    while running:
        clock.tick(FPS)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    player.jump()
                if event.key == pygame.K_SPACE and game_over:
                    # Restart game
                    player = Player()
                    obstacles = []
                    score = 0
                    obstacle_timer = 0
                    game_over = False
                    current_game_speed = game_speed
        
        if not game_over:
            # Update player
            player.update()
            
            # Spawn obstacles
            obstacle_timer += 1
            if obstacle_timer > random.randint(60, 120):
                obstacles.append(Obstacle())
                obstacle_timer = 0
            
            # Update obstacles
            for obstacle in obstacles[:]:
                obstacle.update(current_game_speed)
                
                # Check collision
                if obstacle.collide(player):
                    game_over = True
                
                # Remove off-screen obstacles
                if obstacle.off_screen():
                    obstacles.remove(obstacle)
                    score += 1
            
            # Increase difficulty
            current_game_speed += 0.001
        
        # Draw everything
        screen.fill(SKY_BLUE)
        draw_ground(screen)
        
        player.draw(screen)
        
        for obstacle in obstacles:
            obstacle.draw(screen)
        
        # Draw score
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        # Draw game over
        if game_over:
            game_over_text = font.render("GAME OVER!", True, BLACK)
            restart_text = font.render("Press SPACE to restart", True, BLACK)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()