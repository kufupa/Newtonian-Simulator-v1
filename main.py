import pygame
import pymunk
import os

pygame.init() # initialise all pygame modules
# name of window
pygame.display.set_caption("Newtonian Simulator v1")

# pygame display constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 144

#pymunk constants
SPACE = pymunk.Space()
SPACE.gravity = (0, 500) # no x gravity, 500 y gravity

# colour constants
WHITE = (255, 255, 255)
BLACK = (0,0,0)
STATIC_CIRCLE_RGB = (255, 98, 119)
BG_RGB = WHITE # (217, 217, 217)

# load images
apple_image = pygame.transform.scale(
    pygame.image.load(os.path.join("assets", "red_apple.png")), (80, 80)
)
apple_group = []
static_circle_group = []

class player_Apple:

    def __init__(self, SPACE, apple_group, pos): 
        self.body = pymunk.Body(1, 100, body_type = pymunk.Body.DYNAMIC)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, 40)
        SPACE.add(self.body, self.shape)
        apple_group.append(self)


def draw_apples(apple_group):
    for i in apple_group:
        x = int(i.body.position.x)
        y = int(i.body.position.y)
        a_rect = apple_image.get_rect(center = (x, y))
        
        # remove apple if out of frame
        if x < 0 or x > SCREEN_WIDTH or y > SCREEN_HEIGHT:
            apple_group.remove(i) # remove from apple group
            SPACE.remove(i.body, i.shape) # remove from pymunk space - remove line above to test if it actually removes it

        SCREEN.blit(apple_image, a_rect)
        # pygame.draw.circle(SCREEN, BLACK, (x, y), 80) # for massive black blob

class static_Circle:

    def __init__(self, SPACE, static_circle_group, pos):
        self.body = pymunk.Body(body_type = pymunk.Body.STATIC)
        self.body.position = pos
        self.shape = pymunk.Circle(self.body, 50)
        SPACE.add(self.body, self.shape)
        static_circle_group.append(self)

def draw_static_Circle(static_circle_group):
    for i in static_circle_group:
        x = int(i.body.position.x)
        y = int(i.body.position.y)
        pygame.draw.circle(SCREEN, STATIC_CIRCLE_RGB, (x, y), 50)


def draw_background():
    SCREEN.fill(BG_RGB)



def simulate():
    
    clock = pygame.time.Clock()

    static_Circle(SPACE, static_circle_group, (500, 350))
    static_Circle(SPACE, static_circle_group, (250, 550))

    run = True
    while run: 
        clock.tick(FPS) # FPS cap

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False  
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN: # if mouse clicked
                if pygame.mouse.get_pressed()[0] == 1: # if left button pressed
                    player_Apple(SPACE, apple_group, event.pos) # create apple at mouse location

        # NO LONGER IN EVENT FOR LOOP

        # draw everything
        draw_background()
        draw_static_Circle(static_circle_group)
        draw_apples(apple_group)

        SPACE.step(1/50)



        pygame.display.update()

    pygame.quit()




if __name__ == "__main__":
    simulate()