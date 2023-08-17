import pygame, sys
import os
import random
import pygame.time
pygame.font.init()
clock = pygame.time.Clock()

pygame.init()

#window size
WIDTH, HEIGHT = 1800, 920
WIN = pygame.display.set_mode((WIDTH,HEIGHT))

#player size
PLAYER_WIDTH, PLAYER_HEIGHT = 125,125
#ball size
BALL_WIDTH, BALL_HEIGHT = 30,25

#possesion delay
BALL_POSSESSION_DELAY = 30

#Frames per second
FPS = 60

#Player speed
VEL = 12
SPRINT_DURATION = 2  # or any other desired value
SPRINT_MULTIPLIER = 0 # or any other desired value
SPRINT_COOLDOWN = 5
cooldown_timer1 = 0
cooldown_timer2 = 0

goal_color = (255, 0, 0)
BLACK = (0,0,0)
goal_thickness = 2
WHITE = (255, 255, 255)

goalFont = pygame.font.SysFont('comicsans', 40)

#Load in images
SOCCER_FIELD_IMAGE =  pygame.transform.scale(
    pygame.image.load(os.path.join("Assets",'field.png')), (WIDTH,HEIGHT))
SOCCER_PLAYER1_IMAGE =  pygame.transform.flip((pygame.transform.scale(
    pygame.image.load(os.path.join("Assets",'BluePlayerRun.png')), (PLAYER_WIDTH,PLAYER_HEIGHT))),True,False)
SOCCER_PLAYER2_IMAGE =  pygame.transform.scale(
    pygame.image.load(os.path.join("Assets",'OrangePlayerRun.png')), (PLAYER_WIDTH,PLAYER_HEIGHT))
SOCCER_BALL_IMAGE = pygame.transform.scale(
    pygame.image.load(os.path.join("Assets",'ball.png')), (BALL_WIDTH,BALL_HEIGHT))
#load in sounds
BLIP_SOUND = pygame.mixer.Sound(
    os.path.join('Sounds', 'blip.mp3' ))
pygame.mixer.Sound.set_volume(BLIP_SOUND, .09)
GOAL_SOUND = pygame.mixer.Sound(
    os.path.join('Sounds', 'goal.mp3' ))
WIN_SOUND = pygame.mixer.Sound(
    os.path.join('Sounds', 'win.mp3' ))
CHEER_SOUND = pygame.mixer.Sound(
    os.path.join('Sounds', 'cheer.wav' ))
BACKGROUND_MUSIC = pygame.mixer.Sound(
    os.path.join('Sounds', 'music.mp3'))
pygame.mixer.Sound.set_volume(BACKGROUND_MUSIC, .2)
BAD_SOUND = pygame.mixer.Sound(
    os.path.join('Sounds', 'bad.mp3'))



#draw game window
def draw_window(player1, player2, ball, ball_possessor, goal1, goal2, P1_GOALS,P2_GOALS,field):
    WIN.blit(SOCCER_FIELD_IMAGE, (0, 0))
    player1_goals_text = goalFont.render("Goals: " + str(P1_GOALS), 1, WHITE)
    WIN.blit(player1_goals_text, (200, 10))  # Draws player1's goals on the top left corner of the screen
    player2_goals_text = goalFont.render("Goals: " + str(P2_GOALS), 1, WHITE)
    WIN.blit(player2_goals_text, (1450, 10))  # Draws player1's goals on the top left corner of the screen
    player1_cooldown_text = goalFont.render("Cooldown: " + str(cooldown_timer1),1,WHITE)
    WIN.blit(player1_cooldown_text, (200, 850))
    player2_cooldown_text = goalFont.render("Cooldown: " + str(cooldown_timer2),1,WHITE)
    WIN.blit(player2_cooldown_text, (1450, 850))
    WIN.blit(SOCCER_PLAYER1_IMAGE, player1)
    WIN.blit(SOCCER_PLAYER2_IMAGE, player2)
    #pygame.draw.rect(WIN,goal_color,field,goal_thickness)
    #pygame.draw.rect(WIN, goal_color, goal1, goal_thickness)
    #pygame.draw.rect(WIN, goal_color, goal2, goal_thickness)
    if ball_possessor is not None:
        if ball_possessor == 1:
            ball_pos = (player1.x + PLAYER_WIDTH // 2 - 22,
                        player1.y + PLAYER_HEIGHT // 4 + 18)
        elif ball_possessor == 2:
            ball_pos = (player2.x + PLAYER_WIDTH // 2 ,
                        player2.y + PLAYER_HEIGHT // 4 + 18)
        WIN.blit(SOCCER_BALL_IMAGE, ball_pos)
    else:
        WIN.blit(SOCCER_BALL_IMAGE, ball)
    pygame.display.update()


#handle player movement
def player1_move(keys_pressed, player1):
    if keys_pressed[pygame.K_a] and player1.x > 0:
        player1.x -= VEL
    if keys_pressed[pygame.K_d] and player1.x < WIDTH - PLAYER_WIDTH:
         player1.x += VEL
    if keys_pressed[pygame.K_w] and player1.y > 0:
        player1.y -= VEL
    if keys_pressed[pygame.K_s] and player1.y < HEIGHT - PLAYER_HEIGHT:
        player1.y += VEL
def player2_move(keys_pressed, player2,):
    if keys_pressed[pygame.K_LEFT] and player2.x > 0:
        player2.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and player2.x < WIDTH - PLAYER_WIDTH:
         player2.x += VEL
    if keys_pressed[pygame.K_UP] and player2.y > 0:
        player2.y -= VEL
    if keys_pressed[pygame.K_DOWN] and player2.y < HEIGHT - PLAYER_HEIGHT:
        player2.y += VEL

def player1_dash(keys_pressed, player1):
    global cooldown_timer1
    if cooldown_timer1 > 0:
        cooldown_timer1 -= 1
    else: 
        if keys_pressed[pygame.K_LCTRL]:
            if keys_pressed[pygame.K_d] and player1.x + 250 < WIDTH - PLAYER_WIDTH:
                player1.x = player1.x + 250
                cooldown_timer1 = 90
                BLIP_SOUND.play()
            if keys_pressed[pygame.K_a] and player1.x - 250 > 0:
                player1.x = player1.x - 250
                cooldown_timer1 = 90
                BLIP_SOUND.play()
            if keys_pressed[pygame.K_w] and player1.y - 100 > 0:
                player1.y = player1.y - 100
                cooldown_timer1 = 90
                BLIP_SOUND.play()
            if keys_pressed[pygame.K_s] and player1.y + 100 < HEIGHT - PLAYER_HEIGHT:
                player1.y = player1.y + 100
                cooldown_timer1 = 90
                BLIP_SOUND.play()


        
def player2_dash(keys_pressed, player2): 
    global cooldown_timer2
    if cooldown_timer2 > 0:
        cooldown_timer2 -= 1
    else: 
        if keys_pressed[pygame.K_RCTRL]:
            if keys_pressed[pygame.K_RIGHT] and player2.x + 250 < WIDTH - PLAYER_WIDTH:
                player2.x = player2.x + 250
                cooldown_timer2 = 90
                BLIP_SOUND.play()
            if keys_pressed[pygame.K_LEFT] and player2.x - 250> 0:
                player2.x = player2.x - 250
                cooldown_timer2 = 90
                BLIP_SOUND.play()
            if keys_pressed[pygame.K_UP] and player2.y - 100 > 0:
                player2.y = player2.y - 100
                cooldown_timer2 = 90
                BLIP_SOUND.play()
            if keys_pressed[pygame.K_DOWN] and player2.y + 100 < HEIGHT - PLAYER_HEIGHT:
                player2.y = player2.y + 100
                cooldown_timer2 = 90
                BLIP_SOUND.play()

def player2_sprint(keys_pressed, player2): 
    if keys_pressed[pygame.K_RSHIFT]:
        sprint_vel = VEL * SPRINT_MULTIPLIER
        if keys_pressed[pygame.K_RIGHT] and player2.x < WIDTH - PLAYER_WIDTH:
            player2.x += sprint_vel
        if keys_pressed[pygame.K_LEFT] and player2.x > 0:
            player2.x -= sprint_vel
        if keys_pressed[pygame.K_UP] and player2.y > 0:
            player2.y -= sprint_vel
        if keys_pressed[pygame.K_DOWN] and player2.y < HEIGHT - PLAYER_HEIGHT:
            player2.y += sprint_vel
def player1_sprint(keys_pressed, player1): 
    if keys_pressed[pygame.K_LSHIFT]:
        sprint_vel = VEL * SPRINT_MULTIPLIER
        if keys_pressed[pygame.K_d] and player1.x < WIDTH - PLAYER_WIDTH:
            player1.x += sprint_vel
        if keys_pressed[pygame.K_a] and player1.x > 0:
            player1.x -= sprint_vel
        if keys_pressed[pygame.K_w] and player1.y > 0:
            player1.y -= sprint_vel
        if keys_pressed[pygame.K_s] and player1.y < HEIGHT - PLAYER_HEIGHT:
            player1.y += sprint_vel



def ball_posses(player1, player2, ball, ball_possessor, possession_delay):
    if possession_delay > 0:  # Possession delay period
        possession_delay -= 1
    else:
        if ball_possessor == None:
            if player1.colliderect(ball):
                ball_possessor = 1
            elif player2.colliderect(ball):
                ball_possessor = 2
        else:
            if player1.colliderect(player2) and ball_possessor in [1, 2]:  # Collision between players
                if ball_possessor == 1:
                    ball_possessor = 2
                else:
                    ball_possessor = 1   
                possession_delay = BALL_POSSESSION_DELAY  # Start possession delay period
            elif ball_possessor == 1:
                ball.x = player1.x - PLAYER_WIDTH // 2 - BALL_WIDTH // 2
                ball.y = player1.y + PLAYER_HEIGHT // 2 - BALL_HEIGHT // 2 
            elif ball_possessor == 2:
                ball.x = player2.x + PLAYER_WIDTH // 2 - BALL_WIDTH // 2
                ball.y = player2.y + PLAYER_HEIGHT // 2 - BALL_HEIGHT // 2
    return ball_possessor, possession_delay

def draw_winner(text):
    draw_text = goalFont.render(text,1,BLACK)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)



def main():
    player1 = pygame.Rect(400,400,PLAYER_WIDTH,PLAYER_HEIGHT)
    player2 = pygame.Rect(1300,400,PLAYER_WIDTH,PLAYER_HEIGHT)
    goal1 = pygame.Rect(105,98,160,725)
    goal2 = pygame.Rect(1535,98,160,725)
    field = pygame.Rect(100,90,1605,740)
    ball = pygame.Rect(WIDTH//2 - BALL_WIDTH//2, HEIGHT//2 - BALL_HEIGHT//2, BALL_WIDTH,BALL_HEIGHT)
    ball_possessor = None
    possession_delay = BALL_POSSESSION_DELAY
    P1_GOALS = 0
    P2_GOALS = 0
    win_text = ""

    def main_menu(screen, clock):
        # Displays a main menu with options to play, view controls, or quit
        BACKGROUND_MUSIC.play(-1)
    
        TITLE_IMAGE = pygame.transform.scale(
            pygame.image.load(os.path.join("Assets",'title.png')), (1000,1000))
        PLAY_IMAGE = pygame.transform.scale(
            pygame.image.load(os.path.join("Assets",'play.png')), (500,500))
        CONTROLS_IMAGE = pygame.transform.scale(
            pygame.image.load(os.path.join("Assets",'controls.png')), (500,500))
        QUIT_IMAGE = pygame.transform.scale(
            pygame.image.load(os.path.join("Assets",'quit.png')), (500,500))
    
        menu_items = [TITLE_IMAGE, PLAY_IMAGE, CONTROLS_IMAGE,QUIT_IMAGE]
        item_rects = []

        # Determine position of menu items on the screen
        for i, item in enumerate(menu_items):
            item_rect = item.get_rect(center=(screen.get_width()/2, (i+2)*screen.get_height()/6 - 75))
            item_rect.centerx = screen.get_rect().centerx
            item_rects.append(item_rect)

        go = True
        while go:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, item in enumerate(menu_items):
                        if item_rects[i].collidepoint(event.pos):
                            if i == 1:  
                                go = False
                            elif i == 2:  # Controls
                                print("hey")
                            elif i == 3:  # Quit
                                pygame.quit()
                                quit()

        # Draw menu items onto the screen
            screen.blit(SOCCER_FIELD_IMAGE, (0, 0))
            for i, item in enumerate(menu_items):
                screen.blit(item, item_rects[i])
            pygame.display.flip()
            clock.tick(60)


    clock = pygame.time.Clock()
    main_menu(WIN, clock)

    run = True
    while run: 
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit() 
        #Player Movement
        keys_pressed = pygame.key.get_pressed()
        player1_move(keys_pressed, player1)
        player2_move(keys_pressed, player2)
        player1_dash(keys_pressed,player1)
        player2_dash(keys_pressed, player2)
        player1_sprint(keys_pressed,player1)
        player2_sprint(keys_pressed, player2)
            

        if player1.colliderect(goal1) and ball_possessor == 1:
            P2_GOALS += 1
            BAD_SOUND.play()
            player1.x = 400
            player1.y = 400
            player2.x = 1300
            player2.y = 400
            ball_possessor = None
            ball.x = WIDTH//2 - BALL_WIDTH//2
            ball.y = HEIGHT//2 - BALL_HEIGHT//2
        if player2.colliderect(goal2) and ball_possessor == 2:
            P1_GOALS += 1
            BAD_SOUND.play()
            player1.x = 400
            player1.y = 400
            player2.x = 1300
            player2.y = 400
            ball_possessor = None
            ball.x = WIDTH//2 - BALL_WIDTH//2
            ball.y = HEIGHT//2 - BALL_HEIGHT//2
        if player1.colliderect(goal2) and ball_possessor == 1:
            P1_GOALS += 1
            GOAL_SOUND.play()
            player1.x = 400
            player1.y = 400
            player2.x = 1300
            player2.y = 400
            ball_possessor = None
            ball.x = WIDTH//2 - BALL_WIDTH//2
            ball.y = HEIGHT//2 - BALL_HEIGHT//2

        if player2.colliderect(goal1) and ball_possessor == 2:
            GOAL_SOUND.play()
            P2_GOALS += 1
            player1.x = 400
            player1.y = 400
            player2.x = 1300
            player2.y = 400
            ball_possessor = None
            ball.x = WIDTH//2 - BALL_WIDTH//2
            ball.y = HEIGHT//2 - BALL_HEIGHT//2
        if player1.y > field.height and ball_possessor == 1:
            player1.x = 400
            player1.y = 400
            player2.x = 1300
            player2.y = 400
            ball_possessor = None
            ball.x = player2.x
            ball.y = player2.y
        if player1.y < 5 and ball_possessor == 1:
            player1.x = 400
            player1.y = 400
            player2.x = 1300
            player2.y = 400
            ball_possessor = None
            ball.x = player2.x
            ball.y = player2.y
        if player2.y > field.height and ball_possessor == 2:
            player1.x = 400
            player1.y = 400
            player2.x = 1300
            player2.y = 400
            ball_possessor = None
            ball.x = player1.x
            ball.y = player1.y
        if player2.y < 5 and ball_possessor == 2:
            player1.x = 400
            player1.y = 400
            player2.x = 1300
            player2.y = 400
            ball_possessor = None
            ball.x = player1.x
            ball.y = player1.y
        
            
            

        
        if P1_GOALS == 5:
            win_text = "PLAYER 1 WINS!!"
            BACKGROUND_MUSIC.stop()
            WIN_SOUND.play()
            CHEER_SOUND.play()
        if P2_GOALS == 5:
            win_text = "PLAYER 2 WINS!!"
            BACKGROUND_MUSIC.stop()
            WIN_SOUND.play()
            CHEER_SOUND.play()
        if win_text != "":
            draw_winner(win_text)
            break

        #Ball logic
        ball_possessor, possession_delay = ball_posses(player1, player2, ball, ball_possessor, possession_delay)
        #draw window
        draw_window(player1, player2, ball, ball_possessor,goal1,goal2,P1_GOALS,P2_GOALS,field)
    main()
    

if __name__ == "__main__":
    main()