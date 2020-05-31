import pygame, random, sys
from pygame.locals import *

# game field size
FIELD_X = 10
FIELD_Y = 10
FIELD_CELL_SIZE = 50
WINDOWWIDTH = FIELD_X * FIELD_CELL_SIZE
WINDOWHEIGHT = FIELD_Y * FIELD_CELL_SIZE

# the field matrix
EMPTY_FIELD = 0
SNAKE_FIELD = 1
FOOD_FIELD = 2

# game colors
BACKGROUND_COLOR = (10, 10, 10)
SNAKE_COLOR = (50, 200, 50)
FOOD_COLOR = (220, 220, 50)
COLOR_MATRIX = {EMPTY_FIELD: BACKGROUND_COLOR, SNAKE_FIELD: SNAKE_COLOR, FOOD_FIELD: FOOD_COLOR}
# TODO: Add obstacles


class FieldObject:
    def __init__(self, object_type):
        # self.length = 0
        self.body = [[0, 0]]
        # starting position of the snake's head
        self.position = [0, 0]
        # The type of field object
        self.object_type = object_type


class Snake(FieldObject):
    def __init__(self):
        super(Snake, self).__init__(SNAKE_FIELD)
        self.direction = [1, 0]
        pass

    def change_direction(self, key):
        if key == K_w:      # up
            self.direction = [0, -1]
        elif key == K_s:    # down
            self.direction = [0, 1]
        elif key == K_a:    # left
            self.direction = [-1, 0]
        elif key == K_d:    # right
            self.direction = [1, 0]


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
        self.draw()

    def add_object(self, obj: FieldObject):
        # Adds an object to the field
        # TODO: Check overlapping

        self.objects.append(obj)
        # Update the field
        for cell in obj.body:
            self.field_matrix[cell[0]][cell[1]] = obj.object_type

    def draw(self):
        self.surface.fill(BACKGROUND_COLOR)
        for i in range(FIELD_X):
            for j in range(FIELD_Y):
                pygame.draw.rect(self.surface, COLOR_MATRIX[self.field_matrix[i][j]],
                                 (i*FIELD_CELL_SIZE, j*FIELD_CELL_SIZE, FIELD_CELL_SIZE, FIELD_CELL_SIZE))
        pygame.display.update()
        pass

    def next_step(self):
        # TODO: Add food collision
        # TODO: Add obstacle collision

        # If everything is all right, move the snake
        # 1. Clear the snake's tail in the field_matrix
        tail = len(self.snake.body)-1
        self.field_matrix[self.snake.body[tail][0]][self.snake.body[tail][1]] = EMPTY_FIELD
        # 2. Move the snake body towards the head. Move the head towards snake.direction
        for i in reversed(range(len(self.snake.body))):
            if i > 0:
                self.snake.body[i] = self.snake.body[i-1]
            else:
                # Move the head of the snake
                head = self.snake.body[0]
                # Move the x axis:
                head[0] += self.snake.direction[0]
                if head[0] < 0:
                    head[0] = FIELD_X - 1
                if head[0] > FIELD_X - 1:
                    head[0] = 0
                # Move the y axis:
                head[1] += self.snake.direction[1]
                if head[1] < 0:
                    head[1] = FIELD_Y - 1
                if head[1] > FIELD_Y - 1:
                    head[1] = 0
                self.snake.body[0] = head
                # Update the field_matrix with the new head
                self.field_matrix[head[0]][head[1]] = SNAKE_FIELD

        # TODO: Update other objects

        self.draw()


if __name__ == '__main__':
    # Set up pygame, the window, and the mouse cursor.
    pygame.init()
    mainClock = pygame.time.Clock()
    windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Snake game')
    pygame.mouse.set_visible(False)

    # Initialize the field
    field = Field(windowSurface)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # Assuming the player pressd one of 'w, a, s, d' buttons
                field.snake.change_direction(event.key)
                field.next_step()
                field.draw()
                # TODO: Add food collision
                # TODO: Add obstacle collision






