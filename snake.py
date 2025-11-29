import time
import pygame
import asyncio
import random

pygame.init()
global width
(width, height) = (600,600)
screen = pygame.display.set_mode((width, height))
background_colour = (0,160,0)
screen.fill(background_colour)
pygame.display.set_caption('Snake Game')

class Apple:
    def __init__(self, x=random.randint(1,(width//10)-1)*10, y=random.randint(1,(width//10)-1)*10):
        self.x = x
        self.y = y
        self.colour = (255, 0, 0)
    def display(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), 5)
    def move(self,occupied):
        self.x=random.randint(1,(width//10)-1)*10
        self.y=random.randint(1,(width//10)-1)*10
        coords=(self.x,self.y)
        while coords in occupied:
            self.x=random.randint(1,(width//10)-1)*10
            self.y=random.randint(1,(width//10)-1)*10
            coords=(self.x,self.y)

class Snake:
    def __init__(self, x=width//2, y=width//2, direction=(0,0), body=None):
        self.direction=direction
        self.x=x
        self.y=y
        self.length=1
        self.color=(0,0,0)
        self.body=body
    def show(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 5, 0)
        if self.body==None:
            return None
        return self.body.show()
    def grow(self):
        if self.body==None:
            self.body=Snake(self.x-self.direction[0],self.y-self.direction[1],self.direction)
            return None
        return self.body.grow()
    def move(self):
        self.x+=self.direction[0]
        self.y+=self.direction[1]
    def movement(self, key=None): #Got to make it so when a new key is clicked, it takes priority
        if key=="down" and self.direction!=(0,-10):
            self.direction=(0,10)
        elif key=="up" and self.direction!=(0,10):
            self.direction=(0,-10)
        elif key=="right" and self.direction!=(-10,0):
            self.direction=(10,0)
        elif key=="left" and self.direction!=(10,0):
            self.direction=(-10,0)
        else:
            pass
        if self.body==None:
            self.move()
            return None
        self.body.follow(self.x,self.y,self.direction)
        self.move()
    def follow(self,x,y,direction):
        nextx=self.x
        nexty=self.y
        self.x=x
        self.y=y
        self.direction=direction
        if self.body==None:
            return None
        return self.body.follow(nextx,nexty,direction)
    def occupy(self):
        coord=(self.x,self.y)
        if self.body==None:
            return [coord]
        return [coord]+self.body.occupy()
    def death(self):
        for coord in self.body.occupy():
            if coord==(self.x,self.y):
                return True
        if self.x>width-10 or self.x<10 or self.y>width-10 or self.y<10:
            return True
        return False



#Doesn't let flip() funtion end. If the program reaches the end,  so does the screen
#I don't know why but a simple forever loop makes the program freeze
async def main():
    running=True
    event=pygame.event.wait(1)
    apple=Apple()
    apple.display()
    snake=Snake()
    snake.show()
    pygame.display.flip()
    while event.type!=pygame.KEYDOWN:
        event=pygame.event.wait(1)
    if event.type==pygame.KEYDOWN and event.scancode==82:#Up Arrow
        snake.movement("up")
    elif event.type==pygame.KEYDOWN and event.scancode==81:#Down Arrow
        snake.movement("down")
    elif event.type==pygame.KEYDOWN and event.scancode==80:#Left Arrow
        snake.movement("left")
    elif event.type==pygame.KEYDOWN and event.scancode==79:#Right Arrow
        snake.movement("right")
    for _ in range(2):
        snake.movement()
        snake.grow()
        snake.show()
        time.sleep(0.04)
        pygame.display.flip()
    while running:
        pygame.display.flip() #Updates the screen
        screen.fill(background_colour)
        #Start timer to make each turn equal
        start_time=time.time()
        event=pygame.event.wait(50)
        end_time=time.time()
        if end_time-start_time<0.05:
            await asyncio.sleep(0.05-(end_time-start_time))#Add appropriate time
        #end timer
        if event.type==pygame.KEYDOWN and event.scancode==82:#Up Arrow
            snake.movement("up")
        elif event.type==pygame.KEYDOWN and event.scancode==81:#Down Arrow
            snake.movement("down")
        elif event.type==pygame.KEYDOWN and event.scancode==80:#Left Arrow
            snake.movement("left")
        elif event.type==pygame.KEYDOWN and event.scancode==79:#Right Arrow
            snake.movement("right")
        else:
            snake.movement()
        if (apple.x,apple.y)==(snake.x,snake.y):
            apple.move(snake.occupy())
            snake.grow()
        if snake.death():
            running=None
        if event.type == pygame.QUIT:
            running = False
        snake.show()
        apple.display()
        await asyncio.sleep(0)
    if running==None:#Lose Screen
        screen.fill((100,0,0))
        pygame.font.init() # you have to call this at the start, if you want to use script.
        lose = pygame.font.SysFont('Comic Sans MS', 30).render('You Lose', False, (0, 0, 0))
        if snake.body.body.body!=None:
            score = pygame.font.SysFont('Comic Sans MS', 15).render(f'Score: {len(snake.body.body.body.occupy())}', False, (0, 0, 0))
            screen.blit(score, (width//2-30,width//2))
        screen.blit(lose, (width//2-60,width//2-60))
        pygame.display.flip()
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())