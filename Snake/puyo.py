import pygame
import random

colors = [
    (0, 255, 0),  # Green
    (255, 0, 0),  # Red
    (0, 0, 255),  # Blue
    (255, 255, 0)  # Yellow
]


class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5], [0, 1]],
    ]

    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = color if color else random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate_right(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])

    def rotate_left(self):
        self.rotation = (self.rotation - 1) % len(self.figures[self.type])

from collections import deque

class Tetris:
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = 0
        self.width = 0
        self.x = 100
        self.y = 60
        self.zoom = 40
        self.figure = None
        self.draw_field()
        self.next_figures = deque([Figure(3, 0, random.randint(1, len(colors) - 1)) for _ in range(2)], maxlen=2)

        self.figure = self.next_figures[0]
        self.next_figures.popleft()
        self.next_figures.append(Figure(3, 0, random.randint(1, len(colors) - 1)))

        self.height = height
        self.width = width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        next_color = self.next_figures[0].color
        self.figure = Figure(3, 0, next_color)
        self.next_figures.popleft()  # Remove the used figure from the deque
        self.next_figures.append(Figure(3, 0, random.randint(1, len(colors) - 1)))  # Add a new figure to the deque
    def draw_field(self):
        for i in range(self.height):
            for j in range(self.width):
                pygame.draw.rect(screen, GRAY, [self.x + self.zoom * j, self.y + self.zoom * i, self.zoom, self.zoom],
                                 1)
                if self.field[i][j] > 0:
                    pygame.draw.rect(screen, colors[self.field[i][j]],
                                     [self.x + self.zoom * j + 1, self.y + self.zoom * i + 1, self.zoom - 2,
                                      self.zoom - 1])

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                # Animate the disappearance of the blocks in the cleared row
                for k in range(5):
                    for j in range(self.width):
                        self.field[i][j] = k % 2 + 1
                    self.draw_field()
                    pygame.time.wait(50)
                    pygame.display.flip()
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self, direction):
        old_rotation = self.figure.rotation
        if direction == 'right':
            self.figure.rotate_right()
        elif direction == 'left':
            self.figure.rotate_left()
        if self.intersects():
            self.figure.rotation = old_rotation


# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

size = (500, 600)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# Loop until the user clicks the close button.
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(12, 6)
counter = 0

pressing_down = False

while not done:
    if game.figure is None:
        game.new_figure()
    counter += 1
    if counter > 100000:
        counter = 0

    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start":
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_z:
                game.rotate('left')
            if event.key == pygame.K_DOWN:
                pressing_down = True
            if event.key == pygame.K_LEFT:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT:
                game.go_side(1)
            if event.key == pygame.K_SPACE:
                game.go_space()
            if event.key == pygame.K_x:
                game.rotate('left')
            if event.key == pygame.K_ESCAPE:
                game.__init__(12, 6)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    screen.fill(WHITE)

    preview_x, preview_y = size[0] - game.zoom * 5 + 50, game.zoom  # Set the top-right corner of your screen as starting point
    for index, next_figure in enumerate(game.next_figures):
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in next_figure.image():
                    pygame.draw.rect(screen, colors[next_figure.color],
                                     [preview_x + game.zoom * j,
                                      preview_y + game.zoom * (i + index * 5),  # Multiply index by 5 to separate figures
                                      game.zoom - 2, game.zoom - 2])

    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

    if game.figure is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.figure.image():
                    pygame.draw.rect(screen, colors[game.figure.color],
                                     [game.x + game.zoom * (j + game.figure.x) + 1,
                                      game.y + game.zoom * (i + game.figure.y) + 1,
                                      game.zoom - 2, game.zoom - 2])

    font = pygame.font.SysFont('Calibri', 25, True, False)
    font1 = pygame.font.SysFont('Calibri', 65, True, False)
    text = font.render("Score: " + str(game.score), True, BLACK)
    text_game_over = font1.render("Game Over", True, (255, 125, 0))
    text_game_over1 = font1.render("Press ESC", True, (255, 215, 0))

    screen.blit(text, [0, 0])
    if game.state == "gameover":
        screen.blit(text_game_over, [20, 200])
        screen.blit(text_game_over1, [25, 265])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()

#CURRENT STATE