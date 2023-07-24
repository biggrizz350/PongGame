import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pong Game")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up fonts
font = pygame.font.Font(None, 74)


def get_computer_move(paddle1_y, paddle2_y, ball_x, ball_y):
    # Calculate the difference between the paddle's position and the ball's position
    diff = paddle2_y - ball_y

    # Set the paddle movement based on the difference
    if diff > 0:
        return 'up'
    elif diff < 0:
        return 'down'
    else:
        return 'none'  # Don't move the paddle

# Function to draw the paddles and ball
def draw_objects(paddle1_y, paddle2_y, ball_x, ball_y):
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, (30, paddle1_y, 20, 100))
    pygame.draw.rect(screen, WHITE, (screen_width - 50, paddle2_y, 20, 100))
    pygame.draw.circle(screen, WHITE, (ball_x, ball_y), 15)

# Function to move the paddles
def move_paddle(paddle_y, move):
    if move == 'up' and paddle_y > 0:
        paddle_y -= 10
    elif move == 'down' and paddle_y < screen_height - 100:
        paddle_y += 10
    return paddle_y

# Function to update the ball's position
def move_ball(ball_x, ball_y, ball_dir_x, ball_dir_y):
    ball_x += ball_dir_x * 5
    ball_y += ball_dir_y * 5
    return ball_x, ball_y

# Set Initial ball speed
ball_speed = 0.5

# Function to check for collisions with the paddles and walls
def check_collisions(ball_x, ball_y, ball_dir_x, ball_dir_y, paddle1_y, paddle2_y):
    global ball_speed 

    if ball_y <= 15 or ball_y >= screen_height - 15:
        ball_dir_y *= -1

    if ball_x <= 60 and paddle1_y <= ball_y <= paddle1_y + 100:
        ball_speed += 0.1
        ball_dir_x *= -1

    if ball_x >= screen_width - 60 and paddle2_y <= ball_y <= paddle2_y + 100:
        ball_speed += 0.1
        ball_dir_x *= -1

 # Move the ball after updating the speed
    ball_x += ball_dir_x * ball_speed
    ball_y += ball_dir_y * ball_speed

    return ball_x, ball_y, ball_dir_x, ball_dir_y

# Function to display the score
def display_score(score1, score2):
    score_display = font.render(f"{score1} - {score2}", True, WHITE)
    screen.blit(score_display, (screen_width // 2 - score_display.get_width() // 2, 20))

# Function to display the main menu and select game mode
def main_menu():
    selected_mode = None

    while selected_mode is None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected_mode = "computer"
                elif event.key == pygame.K_2:
                    selected_mode = "player"

        # Clear the screen and display the main menu
        screen.fill(BLACK)
        menu_text = font.render("Pong Game", True, WHITE)
        mode_text = font.render("Select Game Mode:", True, WHITE)
        computer_text = font.render("1 - Player vs. Computer", True, WHITE)
        player_text = font.render("2 - Player vs. Player", True, WHITE)

        screen.blit(menu_text, (screen_width // 2 - menu_text.get_width() // 2, 200))
        screen.blit(mode_text, (screen_width // 2 - mode_text.get_width() // 2, 300))
        screen.blit(computer_text, (screen_width // 2 - computer_text.get_width() // 2, 400))
        screen.blit(player_text, (screen_width // 2 - player_text.get_width() // 2, 500))

        pygame.display.flip()

    return selected_mode

# Main function to run the game
def play_pong():
    mode = main_menu()

    paddle1_y = screen_height // 2 - 50
    paddle2_y = screen_height // 2 - 50
    ball_x = screen_width // 2
    ball_y = screen_height // 2
    ball_dir_x = random.choice([-1, 1])
    ball_dir_y = random.choice([-1, 1])
    score1 = 0
    score2 = 0

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddle1_y = move_paddle(paddle1_y, 'up')
        if keys[pygame.K_s]:
            paddle1_y = move_paddle(paddle1_y, 'down')
        if mode == "player" and keys[pygame.K_UP]:
            paddle2_y = move_paddle(paddle2_y, 'up')
        if mode == "player" and keys[pygame.K_DOWN]:
            paddle2_y = move_paddle(paddle2_y, 'down')


        if mode == "computer":
            computer_move = get_computer_move(paddle1_y, paddle2_y, ball_x, ball_y)
            if computer_move == 'up':
                paddle2_y = move_paddle(paddle2_y, 'up')
            elif computer_move == 'down':
                paddle2_y = move_paddle(paddle2_y, 'down')
        

        ball_x, ball_y, ball_dir_x, ball_dir_y = check_collisions(ball_x, ball_y, ball_dir_x, ball_dir_y, paddle1_y, paddle2_y)
        ball_x, ball_y = move_ball(ball_x, ball_y, ball_dir_x, ball_dir_y)

        draw_objects(paddle1_y, paddle2_y, ball_x, ball_y)
        display_score(score1, score2)

        if ball_x < 0:
            score2 += 1
            ball_speed = 0.5
            if score2 >= 7:  # Check if player 2 wins
                print("Player 2 wins!")
                pygame.quit()
                sys.exit()
            ball_x = screen_width // 2
            ball_y = screen_height // 2
            ball_dir_x = random.choice([-1, 1])
            ball_dir_y = random.choice([-1, 1])
        elif ball_x > screen_width:
            score1 += 1
            ball_speed = 0.5
            if score1 >= 7:  # Check if player 1 wins
                print("Player 1 wins!")
                pygame.quit()
                sys.exit()
            ball_x = screen_width // 2
            ball_y = screen_height // 2
            ball_dir_x = random.choice([-1, 1])
            ball_dir_y = random.choice([-1, 1])

        pygame.display.flip()
        clock.tick(60)

# Run the game
play_pong()
