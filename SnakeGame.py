import pygame, random, sys
from pygame.locals import *

# game parameters
SPEED = 6
MAX_FOOD = 10

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
    def __init__(self, object_type, position):
        # Default location
        self.body = [position]
        # The type of field object
        self.object_type = object_type


class Snake(FieldObject):
    def __init__(self, position, length, direction):
        super(Snake, self).__init__(SNAKE_FIELD, position)
        self.direction = direction
        # TODO: Check that length doesn't exceed field parameters
        for i in range(length-1):
            self.body.append([pos_x(position[0]-direction[0]), pos_y(position[1]-direction[1])])

        self.tail = self.body[length-1]

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
        # Save the tail in case of future eating
        self.tail = self.body[len(self.body) - 1]
        # Move the snake's body towards the head. Move the head towards snake.direction
        for i in reversed(range(len(self.body))):
            if i > 0:
                self.body[i] = self.body[i - 1]
            else:
                # Move the head of the snake
                self.body[0] = [pos_x(self.body[0][0] + self.direction[0]),
                                pos_y(self.body[0][1] + self.direction[1])]

    def eat(self):
        # Eating means adding one cell that was a tail before moving
        self.body.append(self.tail)


class Food(FieldObject):
    def __init__(self, position):
        super(Food, self).__init__(FOOD_FIELD, position)


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
    def __init__(self, surface, s_position, s_length, s_direction, f_position):
        # Create an empty field
        self.surface = surface
        self.field_matrix = [[EMPTY_FIELD for _ in range(FIELD_X)] for _ in range(FIELD_Y)]
        # Cell reference matrix (a reference from each cell to an object occupying it)
        self.reference_matrix = [[None for _ in range(FIELD_X)] for _ in range(FIELD_Y)]
        # No objects in the field
        self.objects = []
        # Create the snake
        self.snake = Snake(s_position, s_length, s_direction)
        self.add_object(self.snake)
        # Create game controlling variables
        self.collision = False
        self.max_food_reached = False
        self.food_eaten = 0
        # Create the food
        food = Food(f_position)
        self.add_object(food)

        self.draw()

    def add_object(self, obj: FieldObject):
        # Adds an object to the field
        # TODO: Check overlapping

        self.objects.append(obj)
        # Update the field - is it necessary?
        for cell in obj.body:
            self.field_matrix[cell[0]][cell[1]] = obj.object_type
            self.reference_matrix[cell[0]][cell[1]] = obj

    def create_new_food(self):
        while True:
            x, y = random.randint(0, FIELD_X-1), random.randint(0, FIELD_Y-1)
            if self.field_matrix[x][y] == EMPTY_FIELD:
                food = Food([x, y])
                self.add_object(food)
                return

    def draw(self):
        # Update field matrix (used for collision check)
        self.field_matrix = [[EMPTY_FIELD for _ in range(FIELD_X)] for _ in range(FIELD_Y)]
        # Update cell reference matrix (used for obtaining objects from cells they are occupying)
        self.reference_matrix = [[None for _ in range(FIELD_X)] for _ in range(FIELD_Y)]
        for obj in self.objects:
            for cell in obj.body:
                self.field_matrix[cell[0]][cell[1]] = obj.object_type
                self.reference_matrix[cell[0]][cell[1]] = obj
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
                print('Collided with yourself!')
            elif cell == FOOD_FIELD:
                self.snake.eat()
                print('Ate food!')
                # Remove this food object from the field
                food_obj = self.reference_matrix[head[0]][head[1]]
                self.objects.remove(food_obj)
                del food_obj
                self. create_new_food()
                self.food_eaten += 1
                if self.food_eaten == MAX_FOOD:
                    self.max_food_reached = True

        # TODO: Add obstacle collision


def draw_text(text, surface, x, y):
    font = pygame.font.SysFont(None, 48)
    text_obj = font.render(text, 1, TEXT_COLOR)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)
    pygame.display.update()


def check_exit_command():
    for event in pygame.event.get():
        if event.type == QUIT:
            exit_game()
        if event.type == KEYDOWN and not moved:
            if event.key == K_ESCAPE:
                exit_game()


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
    random.seed(1)

    # Snake starting parameters
    s_position = [4, 0]
    s_length = 4
    s_direction = [1, 0]
    # Food starting parameters
    f_position = [9, 0]
    # Initialize the field
    field = Field(windowSurface, s_position, s_length, s_direction, f_position)

    while True:
        moved = False
        for event in pygame.event.get():
            if event.type == QUIT:
                exit_game()
            if event.type == KEYDOWN and not moved:
                if event.key == K_ESCAPE:
                    exit_game()
                # Assuming the player pressed one of 'w, a, s, d' buttons
                field.snake.change_direction(event.key)
                moved = True

        field.next_step()
        if field.collision:
            draw_text('Game over!', windowSurface, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            while True:
                check_exit_command()
        elif field.max_food_reached:
            draw_text('You won!', windowSurface, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            while True:
                check_exit_command()
        else:
            field.draw()

            # TODO: Add obstacle collision

        mainClock.tick(SPEED)
