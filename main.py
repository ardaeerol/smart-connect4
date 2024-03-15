import sys
import pygame
import subprocess

# Initialize Pygame
pygame.init()

# Set up the screen
WIDTH, HEIGHT = 400, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4 Game Modes")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Fonts
font = pygame.font.Font(None, 36)


def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)


def main_menu():
    while True:
        screen.fill(WHITE)
        draw_text("Connect 4 Game Modes", BLACK, WIDTH // 2, 50)
        draw_text("Select a mode:", BLACK, WIDTH // 2, 100)

        ai_button = pygame.Rect(WIDTH // 4, 150, WIDTH // 2, 50)
        pygame.draw.rect(screen, BLUE, ai_button)
        draw_text("AI Mode", WHITE, WIDTH // 2, 175)

        two_player_button = pygame.Rect(WIDTH // 4, 225, WIDTH // 2, 50)
        pygame.draw.rect(screen, RED, two_player_button)
        draw_text("2-Player Mode", WHITE, WIDTH // 2, 250)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if ai_button.collidepoint(mouse_pos):
                    # Start AI mode
                    pygame.quit()  # Shutdown the main menu
                    subprocess.run(["python", "smart4.py"])
                    sys.exit()
                elif two_player_button.collidepoint(mouse_pos):
                    # Start 2-player mode
                    pygame.quit()  # Shutdown the main menu
                    subprocess.run(["python", "connect4.py"])
                    sys.exit()


def ai_mode():
    print("Starting AI mode...")


def two_player_mode():
    print("Starting 2-player mode...")


if __name__ == "__main__":
    main_menu()
