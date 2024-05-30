import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Set up the display
display_width = 1200
display_height = 800
world_width = 2000
world_height = 2000

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Car Game')

pygame.font.init()
font = pygame.font.Font(None, 36)

# Set the game clock
clock = pygame.time.Clock()

# Load the car image
carImg = pygame.image.load('car.png')

#Load the has image
gasImg = pygame.image.load('gas.png')

car_width = 40
car_height = 79

GASUSAGE = .5

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
        self.gas = 100
        self.score = 0

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
        if keys[pygame.K_LEFT] and self.gas > 0:
            self.direction += 5
        if keys[pygame.K_RIGHT] and self.gas > 0:
            self.direction -= 5
        if keys[pygame.K_UP] and self.gas > 0:
            self.x += self.speed * math.cos(math.radians(self.direction-90))
            self.y -= self.speed * math.sin(math.radians(self.direction-90))
            self.gas -= GASUSAGE
            car.updateScore()
        if keys[pygame.K_DOWN] and self.gas > 0:
            self.x -= self.speed * math.cos(math.radians(self.direction-90))
            self.y += self.speed * math.sin(math.radians(self.direction-90))
            self.gas -= GASUSAGE
            car.updateScore()
    
    def updateScore(self):
        self.score += GASUSAGE

class GasCan:
    def __init__(self) -> None:
        self.x = random.randint(0, world_width)
        self.y = random.randint(0, world_height)
        self.width = 40
        self.height = 40

    def draw(self):
        gameDisplay.blit(gasImg, (self.x - camera.x, self.y - camera.y))

    def checkCollision(self, car):
        if (self.x - car.x)**2 + (self.y - car.y)**2 < (self.width + car.width)**2:
            car.gas = 100
            return True
        return False

car = Car()
camera = Camera()
gasCans = [GasCan() for _ in range(10)]

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

    # Draw the gas cans
    for gasCan in gasCans[:]:
        gasCan.draw()
        gasCan.checkCollision(car)

    # Draw the score
    text = font.render(f'Score: {car.score}', True, (0, 0, 0))
    gameDisplay.blit(text, (10, 10))

    # Check for collisions and remove gas cans that have been picked up
    gasCans = [gasCan for gasCan in gasCans if not gasCan.checkCollision(car)]

    # Draw the gas
    text = font.render(f'Gas: {car.gas}', True, (0, 0, 0))
    gameDisplay.blit(text, (10, 50))

    # Spawn new gas cans for each one that was picked up
    while len(gasCans) < 10:
        gasCans.append(GasCan())

     # Check if the car is out of gas
    if car.gas <= 0:
        print(f"Game Over. Your score is: {car.score}")  # print the score
        
        running = False  # end the game

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
