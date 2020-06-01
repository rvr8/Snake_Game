import pygame, random, sys
from pygame.locals import *

# game FPS
SPEED = 10

# game field size
FIELD_X = 10
FIELD_Y = 10
FIELD_CELL_SIZE = 30
WINDOW_WIDTH = FIELD_X * FIELD_CELL_SIZE
WINDOW_HEIGHT = FIELD_Y * FIELD_CELL_SIZE

# the field matrix
EMPTY_FIELD = 0
SNAKE_FIELD = 1
FOOD_FIELD = 2
SNAKE_HEAD = 3

# game colors
BACKGROUND_COLOR = (10, 10, 10)
SNAKE_COLOR = (50, 150, 50)
FOOD_COLOR = (220, 220, 50)
SNAKE_HEAD_COLOR = (100, 250, 100)
COLOR_MATRIX = {EMPTY_FIELD: BACKGROUND_COLOR, SNAKE_FIELD: SNAKE_COLOR, FOOD_FIELD: FOOD_COLOR,
                SNAKE_HEAD: SNAKE_HEAD_COLOR}
TEXT_COLOR = (250, 250, 250)


# TODO: Add obstacles


class FieldObject:
    def __init__(self, object_type):
        # self.length = 0
        self.body = [[4, 0]]
        # starting position of the snake's head   --- not needed?
        # self.position = [1, 0]
        # The type of field object
        self.object_type = object_type


class Snake(FieldObject):
    def __init__(self):
        super(Snake, self).__init__(SNAKE_FIELD)
        self.direction = [1, 0]
        self.body.append([3, 0])
        self.body.append([2, 0])
        self.body.append([1, 0])

    def change_direction(self, key):
        if key == K_w:  # up
            d = [0, -1]
        elif key == K_s:  # down
            d = [0, 1]
        elif key == K_a:  # left
            d = [-1, 0]
        elif key == K_d:  # right
            d = [1, 0]
        else:
            return
        # Check if proposed direction (d) is not the opposite of current direction
        if [x + y for x, y in zip(d, self.direction)] == [0, 0]:
            return
        self.direction = d

    def move(self):
        tail = len(self.body) - 1
        # Move the snake's body towards the head. Move the head towards snake.direction
        for i in reversed(range(len(self.body))):
            if i > 0:
                self.body[i] = self.body[i - 1]
            else:
                # Move the head of the snake
                self.body[0] = [pos_x(self.body[0][0] + self.direction[0]),
                                pos_y(self.body[0][1] + self.direction[1])]


def pos_x(x):
    # returns a proper coordinate for x, taking field borders into account
    if x < 0:
        x = x + FIELD_X
    if x > FIELD_X - 1:
        x = x - FIELD_X
    return x


def pos_y(y):
    # returns a proper coordinate for y, taking field borders into account
    if y < 0:
        y = y + FIELD_Y
    if y > FIELD_Y - 1:
        y = y - FIELD_Y
    return y


class Field:
    # A class for main game field. Contains all the field info and references on all objects, including the snake,
    # the food, obstacles etc.
    def __init__(self, surface):
        # Create an empty field
        self.surface = surface
        self.field_matrix = [[EMPTY_FIELD for _ in range(FIELD_X)] for _ in range(FIELD_Y)]
        # No objects in the field
        self.objects = []
        # Create the snake
        self.snake = Snake()
        self.add_object(self.snake)
        self.collision = False
        self.draw()

    def add_object(self, obj: FieldObject):
        # Adds an object to the field
        # TODO: Check overlapping

        self.objects.append(obj)
        # Update the field
        for cell in obj.body:
            self.field_matrix[cell[0]][cell[1]] = obj.object_type

    def draw(self):
        # Update field matrix (used for collision check)
        self.field_matrix = [[EMPTY_FIELD for _ in range(FIELD_X)] for _ in range(FIELD_Y)]
        for obj in self.objects:
            for cell in obj.body:
                self.field_matrix[cell[0]][cell[1]] = obj.object_type
        # Exception for snake's head
        self.field_matrix[self.snake.body[0][0]][self.snake.body[0][1]] = SNAKE_HEAD

        # Draw the field
        self.surface.fill(BACKGROUND_COLOR)
        for i in range(FIELD_X):
            for j in range(FIELD_Y):
                pygame.draw.rect(self.surface, COLOR_MATRIX[self.field_matrix[i][j]],
                                 (i * FIELD_CELL_SIZE, j * FIELD_CELL_SIZE, FIELD_CELL_SIZE, FIELD_CELL_SIZE))
        pygame.display.update()
        pass

    def next_step(self):
        # Move the snake
        self.snake.move()

        # Check for collisions: snake's head is in new position
        head = self.snake.body[0]
        cell = self.field_matrix[head[0]][head[1]]
        if cell != EMPTY_FIELD:
            if cell == SNAKE_FIELD:
                self.collision = True
            elif cell == FOOD_FIELD:
                pass
        # TODO: Add collision with your own body
        # TODO: Add food collision
        # TODO: Add obstacle collision
        # TODO: Update other objects


def draw_text(text, surface, x, y):
    font = pygame.font.SysFont(None, 48)
    text_obj = font.render(text, 1, TEXT_COLOR)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)
    pygame.display.update()


def exit_game():
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    # Set up pygame, the window, and the mouse cursor.
    pygame.init()
    mainClock = pygame.time.Clock()
    windowSurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Snake game')
    pygame.mouse.set_visible(False)

    # Initialize the field
    field = Field(windowSurface)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit_game()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit_game()
                # Assuming the player pressed one of 'w, a, s, d' buttons
                field.snake.change_direction(event.key)

        field.next_step()
        if not field.collision:
            field.draw()
        else:
            print('Collided with yourself!')
            draw_text('Game over!', windowSurface, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            while True:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        exit_game()
            # TODO: Add food collision
            # TODO: Add obstacle collision

        mainClock.tick(SPEED)
