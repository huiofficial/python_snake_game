import pygame
import random
import sys

# 初始化游戏
pygame.init()

# 设置游戏窗口大小
WINDOW_SIZE = 600
CELL_SIZE = 20
GRID_WIDTH = WINDOW_SIZE // CELL_SIZE
GRID_HEIGHT = WINDOW_SIZE // CELL_SIZE
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("贪吃蛇游戏")

# 颜色设置
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 字体设置
font = pygame.font.SysFont(None, 48)
button_font = pygame.font.SysFont(None, 36)

# 按钮位置和大小
button_width = 200
button_height = 50
easy_button_rect = pygame.Rect((WINDOW_SIZE // 2 - button_width // 2, WINDOW_SIZE // 2 - 60),
                               (button_width, button_height))
medium_button_rect = pygame.Rect((WINDOW_SIZE // 2 - button_width // 2, WINDOW_SIZE // 2),
                                 (button_width, button_height))
hard_button_rect = pygame.Rect((WINDOW_SIZE // 2 - button_width // 2, WINDOW_SIZE // 2 + 60),
                               (button_width, button_height))
restart_button_rect = pygame.Rect((WINDOW_SIZE // 2 - button_width // 2, WINDOW_SIZE // 2), (button_width, button_height))
quit_button_rect = pygame.Rect((WINDOW_SIZE // 2 - button_width // 2, WINDOW_SIZE // 2 + 60), (button_width, button_height))


def draw_button(screen, rect, text):
    pygame.draw.rect(screen, WHITE, rect)
    text_surface = button_font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)


def start_screen():
    screen.fill(BLACK)
    title_text = font.render('Level', True, WHITE)
    text_rect = title_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 120))
    screen.blit(title_text, text_rect)

    draw_button(screen, easy_button_rect, 'Easy')
    draw_button(screen, medium_button_rect, 'Middle')
    draw_button(screen, hard_button_rect, 'Hard')
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if easy_button_rect.collidepoint(event.pos):
                    return 3
                elif medium_button_rect.collidepoint(event.pos):
                    return 7
                elif hard_button_rect.collidepoint(event.pos):
                    return 10


def game_over_screen(score):
    screen.fill(BLACK)
    game_over_text = font.render(f'Game Over!'
                                 f'Score: {score}', True, WHITE)
    text_rect = game_over_text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE // 2 - 100))
    screen.blit(game_over_text, text_rect)

    draw_button(screen, restart_button_rect, 'Restart')
    draw_button(screen, quit_button_rect, 'Quit')
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if restart_button_rect.collidepoint(event.pos):
                    return True
                elif quit_button_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()


def main():
    speed = start_screen()

    # 初始化贪吃蛇
    snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
    snake_direction = pygame.K_RIGHT
    new_direction = snake_direction
    snake_length = 1

    # 初始化食物
    food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))

    # 游戏主循环
    clock = pygame.time.Clock()
    score = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    new_direction = event.key

        # 防止蛇逆向移动
        if (new_direction == pygame.K_UP and snake_direction != pygame.K_DOWN) or \
                (new_direction == pygame.K_DOWN and snake_direction != pygame.K_UP) or \
                (new_direction == pygame.K_LEFT and snake_direction != pygame.K_RIGHT) or \
                (new_direction == pygame.K_RIGHT and snake_direction != pygame.K_LEFT):
            snake_direction = new_direction

        # 更新蛇的位置
        head_x, head_y = snake[0]
        if snake_direction == pygame.K_UP:
            head_y -= 1
        elif snake_direction == pygame.K_DOWN:
            head_y += 1
        elif snake_direction == pygame.K_LEFT:
            head_x -= 1
        elif snake_direction == pygame.K_RIGHT:
            head_x += 1

        new_head = (head_x, head_y)
        snake.insert(0, new_head)

        # 检测是否吃到食物
        if new_head == food:
            snake_length += 1
            score += 10
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        else:
            snake.pop()

        # 检测游戏是否结束
        if head_x < 0 or head_x >= GRID_WIDTH or head_y < 0 or head_y >= GRID_HEIGHT or new_head in snake[1:]:
            if game_over_screen(score):
                main()
            else:
                pygame.quit()
                sys.exit()

        # 绘制游戏界面
        screen.fill(BLACK)
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.update()

        # 控制游戏速度
        clock.tick(speed)


if __name__ == '__main__':
    main()