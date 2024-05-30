import pygame
import math

# Initialize Pygame
pygame.init()

# Set up the display
display_width = 1200
display_height = 800
world_width = 2000
world_height = 2000

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Car Game')

# Set the game clock
clock = pygame.time.Clock()

# Load the car image
carImg = pygame.image.load('car.png')

car_width = 40
car_height = 79

# Load the background
texture = pygame.image.load('background.png')

# Define the camera class
class Camera:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0

    def apply(self, entity):
        return entity.x - self.x, entity.y - self.y

    def update(self, target):
        x = -target.x + display_width / 2
        y = -target.y + display_height / 2

        # Limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(display_width - world_width, x)  # right
        y = max(display_height - world_height, y)  # bottom

        self.x = -x
        self.y = -y

# Define the car class
class Car:
    def __init__(self) -> None:
        self.x = display_width * 0.5
        self.y = display_height * 0.5
        self.width = car_width
        self.height = car_height
        self.speed = 5
        self.direction = 0

    def draw(self):
        directionAdjustedCarImg = pygame.transform.rotate(carImg, self.direction)
        rotatedCarImgRect = directionAdjustedCarImg.get_rect(center=(self.x - camera.x, self.y - camera.y))
        gameDisplay.blit(directionAdjustedCarImg, rotatedCarImgRect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            if self.speed < 20:
                self.speed += .5
        if keys[pygame.K_LCTRL]:
            if self.speed > 0:
                self.speed -= .5
        if keys[pygame.K_LEFT]:
            self.direction += 5
        if keys[pygame.K_RIGHT]:
            self.direction -= 5
        if keys[pygame.K_UP]:
            self.x += self.speed * math.cos(math.radians(self.direction-90))
            self.y -= self.speed * math.sin(math.radians(self.direction-90))
        if keys[pygame.K_DOWN]:
            self.x -= self.speed * math.cos(math.radians(self.direction-90))
            self.y += self.speed * math.sin(math.radians(self.direction-90))

car = Car()
camera = Camera()

# Tile the texture across the game display
for y in range(0, world_height, texture.get_height()):
    for x in range(0, world_width, texture.get_width()):
        gameDisplay.blit(texture, (x - camera.x, y - camera.y))

# Main game loop
running = True
while running:
    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the display with white
    gameDisplay.fill((255, 255, 255))

     # Draw the background
    for y in range(0, world_height, texture.get_height()):
        for x in range(0, world_width, texture.get_width()):
            gameDisplay.blit(texture, (x - camera.x, y - camera.y))

    # Draw the car
    car.draw()

    # Move the car
    car.move()

    # Update the display
    pygame.display.update()

    # Update the camera
    camera.update(car)

    # Set the frame rate
    clock.tick(60)
