import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width = 800
screen_height = 600

# Set up the display
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')
icon = pygame.image.load('snake.png')
pygame.display.set_icon(icon)

# Updated color definitions
background_color = (20, 20, 20)  # Dark gray for the background
food_color = (255, 165, 0)  # Orange for the food
snake_color = (128, 0, 128)  # Purple for the snake
text_color = (255, 255, 255)  # White for the text
border_color = (50, 50, 50)  # Dark gray for the borders
button_color = food_color  # Orange for the play again button
button_hover_color = (245, 150, 0)  # Darker orange for the play again button hover effect

# Snake settings
snake_pos = [[100, 50], [90, 50], [80, 50]]  # Initial snake position
snake_speed = 15  # Adjust speed as necessary
direction = 'RIGHT'
change_to = direction

# Food settings
food_pos = [random.randrange(1, (screen_width // 10) - 1) * 10 + 10, random.randrange(1, (screen_height // 10) - 1) * 10 + 10]
food_spawn = True

# Score
score = 0

# Font settings
font = pygame.font.SysFont('arial', 35)

def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (screen_width / 10, 15)
    else:
        score_rect.midtop = (screen_width / 2, screen_height / 1.25)
    screen.blit(score_surface, score_rect)

def draw_play_again_button():
    mouse = pygame.mouse.get_pos()
    play_again_text = font.render('Play Again', True, text_color)
    button_rect = play_again_text.get_rect()
    button_rect.center = (screen_width // 2, screen_height // 2 + 50)
    
    button_color_to_use = button_hover_color if button_rect.collidepoint(mouse) else button_color
    
    # Draw the rounded rectangle button
    pygame.draw.rect(screen, button_color_to_use, button_rect.inflate(20, 20), border_radius=10)
    screen.blit(play_again_text, play_again_text.get_rect(center=button_rect.center))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button_rect.collidepoint(mouse):
                main()
                return True
    return False

def show_game_over():
    screen.fill(background_color)
    game_over_text = font.render('GAME OVER', True, food_color)
    game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
    screen.blit(game_over_text, game_over_rect)
    pygame.display.flip()
    waiting_for_input = True
    while waiting_for_input:
        if draw_play_again_button():
            waiting_for_input = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

def main():
    global snake_pos, food_pos, food_spawn, direction, change_to, score
    score = 0
    snake_pos = [[100, 50], [90, 50], [80, 50]]
    direction = 'RIGHT'
    change_to = direction
    food_pos = [random.randrange(1, (screen_width // 10) - 1) * 10 + 10, random.randrange(1, (screen_height // 10) - 1) * 10 + 10]
    food_spawn = True
    clock = pygame.time.Clock()
    
    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    change_to = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    change_to = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    change_to = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    change_to = 'RIGHT'

        direction = change_to
        
        # Update snake position
        if direction == 'UP':
            snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1] - 10])
        elif direction == 'DOWN':
            snake_pos.insert(0, [snake_pos[0][0], snake_pos[0][1] + 10])
        elif direction == 'LEFT':
            snake_pos.insert(0, [snake_pos[0][0] - 10, snake_pos[0][1]])
        elif direction == 'RIGHT':
            snake_pos.insert(0, [snake_pos[0][0] + 10, snake_pos[0][1]])

        # Snake eating food
        if snake_pos[0] == food_pos:
            score += 10
            food_spawn = False
        else:
            snake_pos.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (screen_width // 10) - 1) * 10 + 10, random.randrange(1, (screen_height // 10) - 1) * 10 + 10]
            while food_pos in snake_pos:  # Ensure food does not spawn on the snake
                food_pos = [random.randrange(1, (screen_width // 10) - 1) * 10 + 10, random.randrange(1, (screen_height // 10) - 1) * 10 + 10]
        food_spawn = True

        # Fill the background color
        screen.fill(background_color)

        # Draw borders
        border_thickness = 5
        pygame.draw.rect(screen, border_color, pygame.Rect(0, 0, screen_width, border_thickness))  # Top border
        pygame.draw.rect(screen, border_color, pygame.Rect(0, screen_height - border_thickness, screen_width, border_thickness))  # Bottom border
        pygame.draw.rect(screen, border_color, pygame.Rect(0, 0, border_thickness, screen_height))  # Left border
        pygame.draw.rect(screen, border_color, pygame.Rect(screen_width - border_thickness, 0, border_thickness, screen_height))  # Right border

        # Draw snake
        for pos in snake_pos:
            pygame.draw.rect(screen, snake_color, pygame.Rect(pos[0], pos[1], 10, 10))

        # Draw food
        pygame.draw.rect(screen, food_color, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        # Check for game over
        if (snake_pos[0][0] >= screen_width - border_thickness or snake_pos[0][0] < border_thickness or
            snake_pos[0][1] >= screen_height - border_thickness or snake_pos[0][1] < border_thickness or
            snake_pos[0] in snake_pos[1:]):
            show_game_over()
            break

        show_score(1, text_color, 'arial', 35)
        pygame.display.flip()
        clock.tick(snake_speed)

if __name__ == '__main__':
    main()
