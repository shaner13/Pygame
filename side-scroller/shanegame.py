'''

shane game to do things

''' 

import pygame, random, sys, time
from threading import Timer

# classes

class Player(pygame.sprite.Sprite):
        
    def __init__(self, colour, w, h):
        super().__init__()
        
        #jumping attributes
        self.isJump = False
        self.jumpCount = 8
        
        self.image = bunny_sprite
        self.rect  = self.image.get_rect()
        
        
        
    def update(self):
        
            
        #initially player is static
        self.speedx = 0 
        self.speedy = 0 
        
        #key handling
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speedx -= 5
        if keys[pygame.K_RIGHT]:
            self.speedx += 5
        if not (self.isJump):   
            if keys[pygame.K_DOWN]:
                self.speedy += 5
            if keys[pygame.K_UP]:
                self.isJump = True
        else:
            if self.jumpCount >= -9:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.speedy -= (self.jumpCount ** 2) * 0.5 * neg
                self.jumpCount -= 1    
            else:
                self.isJump = False
                self.jumpCount = 8
            
        # update movement
        self.rect.x += self.speedx
        self.rect.y += self.speedy
    
        # boundary checking
        if self.rect.x > WINDOWWIDTH - self.rect.width:
            self.rect.x = WINDOWWIDTH - self.rect.width    
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y < 0:
            self.rect.y = 0
        if self.rect.y > 448:
            self.rect.y = 448   
            
class Collectable(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        
        self.image = carrot_sprite
        self.rect  = self.image.get_rect()
        
        self.rect.x = 400
        self.rect.y = 448
        
    def update(self):
        self.speedx = 0 
        self.speedy = 0 
        

        self.speedx -= 2
        self.rect.x += self.speedx
        
        if self.rect.x < 0:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        
        self.image = cat_sprite
        self.rect  = self.image.get_rect()
        
        self.rect.x = 400
        self.rect.y = 448
        
    def update(self):
        self.speedx = 0 
        self.speedy = 0 
        

        self.speedx -= 2
        self.rect.x += self.speedx
        
        if self.rect.x < 0:
            self.kill()
       
            
            
#functions     

def spawner():
    
    spawn_choice = random.randrange(1, 3)
    
    if spawn_choice == 1:
    	new_collectable = Collectable()
    	all_sprites_list.add(new_collectable)        
    	collectable_list.add(new_collectable)

    if spawn_choice == 2:
    	new_enemy = Enemy()
    	all_sprites_list.add(new_enemy)        
    	enemy_list.add(new_enemy)

              
    Timer(random.uniform(0.5,  2.5), spawner).start()    

def collision(stats, collectable_list, enemy_list, player1):
    
    collision_list_1 = pygame.sprite.spritecollide(player1,collectable_list,True)
    for block in collision_list_1:
        stats[0] += 1

    collision_list_2 = pygame.sprite.spritecollide(player1,enemy_list,True)
    for block in collision_list_2:
        stats[1] -= 1

    return stats 

    
def scrolling(x):
    
    relative_x = x % background_image.get_rect().width
    screen.blit(background_image, (relative_x - background_image.get_rect().width, 0))
    if relative_x < WINDOWWIDTH:
        screen.blit(background_image, (relative_x, 0))
    x -= 1  
        
    return x

def text_display(surf, text, size, x, y):

    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, BLACK, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    screen.blit(text_surface, text_rect) 
    
  

#starting game
   
pygame.init()

#Defining Constants
 
GREEN = (20, 255, 140)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLUE = (0, 0, 255)
BLACK = ( 0, 0, 0)

WINDOWWIDTH=400
WINDOWHEIGHT=500

x = 0

ALPHA = (255,255,255)

#stats[0]==score stats[1]==health
stats = [0,5]

font_name = pygame.font.match_font('arial')

size = (WINDOWWIDTH, WINDOWHEIGHT)

#Outputting Display
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Shane Game")

#Importing Images and converting to correct sizes
bunny_sprite = pygame.image.load("bunny.jpg").convert() 
bunny_sprite = pygame.transform.scale(bunny_sprite, (20, 30))
bunny_sprite.convert_alpha() 
bunny_sprite.set_colorkey(WHITE)
carrot_sprite = pygame.image.load("carrot.png").convert() 
carrot_sprite = pygame.transform.scale(carrot_sprite, (20, 30))
carrot_sprite.convert_alpha() 
carrot_sprite.set_colorkey(BLACK)
cat_sprite = pygame.image.load("cat.jpg").convert() 
cat_sprite = pygame.transform.scale(cat_sprite, (30, 30))
cat_sprite.convert_alpha() 
cat_sprite.set_colorkey(BLACK)
background_image = pygame.image.load("beach.jpg").convert() 
background_image = pygame.transform.scale(background_image, (WINDOWWIDTH, WINDOWHEIGHT))




#Making sprite group for all sprites
all_sprites_list = pygame.sprite.Group()

#add player 
player1 = Player(GREY, 20, 30)
player1.rect.x = 50
player1.rect.y = 448

#make groups for sprites 
all_sprites_list.add(player1)
collectable_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()

#spawning things periodically
spawner()



 
#Main game loop
carryOn = True
clock=pygame.time.Clock()


while carryOn:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                carryOn=False
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_x: #Pressing the x Key will quit the game
                     carryOn=False
                    
            
            
        #Game Logic
        all_sprites_list.update()
 
        #Drawing on Screen
        screen.fill(BLACK)
        x = scrolling(x)
        stats = collision(stats, collectable_list, enemy_list, player1)
        score_display = 'Score:' + str(stats[0])
        text_display(screen, score_display, 18, WINDOWWIDTH / 2, 10)
        health_display = 'Health:' + str(stats[1])
        text_display(screen, health_display, 18, WINDOWWIDTH / 2, 35)
        if stats[1] < 1:
        	text_display(screen, 'GAME OVER', 50, WINDOWWIDTH / 2, 200)
        	carryOn=False
        	
        all_sprites_list.draw(screen)
 	   
        #Refresh Screen
        pygame.display.flip()
        clock.tick(60)
 
pygame.quit()