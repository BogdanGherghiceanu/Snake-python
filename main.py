import copy
import pygame
import random
import json

pygame.font.init()
SCORE_FONT=pygame.font.SysFont('calibri',30)
max_score = 1
actual_score = 0
#WINDOW MAIN MENU

WIDTH_START = 400
HEIGHT_START =600
WIN = pygame.display.set_mode((WIDTH_START,HEIGHT_START))

#colors
BACKGROUND_COLOR1=(0, 181, 82)
BACKGROUND_COLOR2=(2, 212, 97)
BLACK = (0, 0, 0)
GREEN= (34,139,34)
BLACK = (0, 0, 0)
BACKGROUND_COLOR=BLACK
WHITE= (255,255,255)
GREEN= (34,139,34)
RED = (255,99,71)
SNAKE_COLOR = GREEN
FOOD_COLOR= (0, 22, 189)


def draw_background(cell_size, height, width):
    color1_line=True
    for h in range(0, height, cell_size):
        color1=color1_line
        for w in range(0, width, cell_size):
            border = pygame.Rect(w, h, cell_size, cell_size)
            if color1:
                pygame.draw.rect(WIN, BACKGROUND_COLOR1, border)
                color1 = False
            else:
                pygame.draw.rect(WIN, BACKGROUND_COLOR2, border)
                color1 = True
        if color1_line:
            color1_line=False
        else:
            color1_line=True


def draw_menu(button1_text, button1rect, button2_text, button2rect):
    draw_background(20,HEIGHT_START,WIDTH_START)
    #button1
    pygame.draw.rect(WIN, BLACK, button1rect)
    WIN.blit(button1_text,( WIDTH_START/2 - (button1_text.get_width()//2), HEIGHT_START/2-(button1_text.get_height()//2) ))
    #button2
    pygame.draw.rect(WIN, BLACK, button2rect)
    WIN.blit(button2_text,
             (WIDTH_START / 2 - (button2_text.get_width() // 2) + 5,
                              HEIGHT_START / 2 + (button1_text.get_height() // 2) + 15))
    pygame.display.update()

def menu():
    # button Start new game
    button1_text = SCORE_FONT.render("Start new game", 1, BACKGROUND_COLOR1)
    button1rectPos=(WIDTH_START / 2 - (button1_text.get_width() // 2) - 5,
                              HEIGHT_START / 2 - (button1_text.get_height() // 2) - 5,
                              button1_text.get_width() + 10,
                              button1_text.get_height() + 10)
    button1rect = pygame.Rect(button1rectPos[0],button1rectPos[1],button1rectPos[2],button1rectPos[3])
    # button settings
    button2_text = SCORE_FONT.render("Custom map", 1, BACKGROUND_COLOR2)
    button2rectPos=(WIDTH_START / 2 - (button2_text.get_width() // 2) - 5,
                              HEIGHT_START / 2 + (button1_text.get_height() // 2) + 10,
                              button2_text.get_width() + 20,
                              button2_text.get_height() + 10)
    button2rect = pygame.Rect(button2rectPos[0],button2rectPos[1],button2rectPos[2],button2rectPos[3])
    run_menu=True
    while run_menu:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_menu = False
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button1rectPos[0]<=mouse[0]<=button1rectPos[0]+button1rectPos[2] and button1rectPos[1]<=mouse[1]<=button1rectPos[1]+button1rectPos[3]:
                    return 1
                if button2rectPos[0]<=mouse[0]<=button2rectPos[0]+button2rectPos[2] and button2rectPos[1]<=mouse[1]<=button2rectPos[1]+button2rectPos[3]:
                    return 2

        draw_menu(button1_text, button1rect, button2_text, button2rect)

def draw_game(cell_size, cells_x, cells_y, FOOD, SNAKE, bridges,max_score):
    WIN.fill(BACKGROUND_COLOR)

    height=cells_y*cell_size
    width=cells_x*cell_size
    draw_background(cell_size,height,width)

    for bridge in bridges:
        pygame.draw.rect(WIN, BLACK, bridge)

    for snake_part in SNAKE:
        pygame.draw.rect(WIN, SNAKE_COLOR, snake_part)
    pygame.draw.rect(WIN, WHITE, SNAKE[-1])

    pygame.draw.rect(WIN, FOOD_COLOR, FOOD)
    score = len(SNAKE)
    score_text = SCORE_FONT.render("Score " + str(score), 1, GREEN)

    score_max_text = SCORE_FONT.render("Max score " + str(max_score), 1, GREEN)
    WIN.blit(score_text, (2, height + 2))
    WIN.blit(score_max_text,(width-score_max_text.get_width()-2,height+2))
    pygame.display.update()

def move_snake(lastKey,food,SNAKE,CELL_SIZE, WIDTH, HEIGHT, bridges):
    next = copy.copy(SNAKE[-1])


    if lastKey == pygame.K_LEFT:
        next.x -= CELL_SIZE

    if lastKey == pygame.K_RIGHT:
        next.x += CELL_SIZE

    if lastKey == pygame.K_UP:

        next.y -= CELL_SIZE
    if lastKey == pygame.K_DOWN:

        next.y += CELL_SIZE
    #check if out of border
    if next.x <0 or next.x > WIDTH - CELL_SIZE or next.y<0 or next.y >HEIGHT-CELL_SIZE:
        return False, food



    snakeNext = pygame.Rect(next.x, next.y, CELL_SIZE, CELL_SIZE)
    if snakeNext in SNAKE or snakeNext in bridges:
        return False, food
    SNAKE.append(snakeNext)
    if food in SNAKE:
        food = manager_food(SNAKE,CELL_SIZE,WIDTH, HEIGHT,bridges)

    else:
        SNAKE.pop(0)


    return True, food
def manager_food(SNAKE,CELL_SIZE,WIDTH, HEIGHT ,bridges):
    run=True
    while run:
        foodx=random.randint(0,WIDTH//CELL_SIZE-1)*CELL_SIZE
        foody=random.randint(0,HEIGHT//CELL_SIZE-1)*CELL_SIZE
        food=pygame.Rect(foodx,foody,CELL_SIZE,CELL_SIZE)
        if food not in SNAKE or food not in bridges:
            run=False
    return food

def draw_lose(width, height):
    text1 = SCORE_FONT.render("Ai pierdut", 1, WHITE)
    text2 = SCORE_FONT.render("Click pentru un joc nou", 1, WHITE)
    lose_rect=pygame.Rect(width//2-(text2.get_width()//2),height//2-(text1.get_height()+text2.get_height())//2,text2.get_width(),text1.get_height()+text2.get_height())
    pygame.draw.rect(WIN, BLACK, lose_rect)

    WIN.blit(text1, (width//2-(text1.get_width()//2),height//2-(text1.get_height()+text2.get_height())//2))
    WIN.blit(text2,
             (width // 2 - (text2.get_width() // 2), height // 2 +  2))
    run_lose=True
    pygame.display.update()
    while run_lose:
        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_lose = False
                return -1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if (width//2-(text2.get_width()//2)) <= mouse[0] <= (width//2-(text2.get_width()//2)+text2.get_width()) and (( height//2-(text1.get_height()+text2.get_height())//2) <=mouse[1] <= (height//2-(text1.get_height()+text2.get_height())//2)+text1.get_height()+text2.get_height()):
                        run_lose=False
    return 1







def game_pause(width, height):
    text1 = SCORE_FONT.render("Click arrows to resume", 1, WHITE)
    pause_rect = pygame.Rect(width // 2 - (text1.get_width() // 2),
                            height // 2 - (text1.get_height() ) // 2, text1.get_width(),
                            text1.get_height())
    pygame.draw.rect(WIN, BLACK, pause_rect)
    WIN.blit(text1,
             (pause_rect.x,pause_rect.y))
    pygame.display.update()

def load_json(nameOfFile):
    path="costumize/"+nameOfFile+".json"
    read=open(path)
    jsonText=read.read()

    jsonFile=json.loads(jsonText)


    cell_size = jsonFile['cell_size']
    cellsx = jsonFile['cellsx']
    cellsy = jsonFile['cellsy']
    speed = jsonFile['speed']
    bridgesRect= []
    for bridges in jsonFile['bridges']:
        bridgesx=bridges['x']
        bridgesy=bridges['y']
        bridge_rect = pygame.Rect(((bridgesx-1)*cell_size),
                                  ((bridgesy-1)*cell_size),
                                  cell_size,
                                  cell_size)
        bridgesRect.append(bridge_rect)


    read.close()
    return cell_size,cellsx,cellsy,speed,bridgesRect


def writeScoreJson(score):
    dictionary = {
        "score": score
    }
    jsonFile = json.dumps(dictionary)
    with open("costumize/score.json", "w") as outfile:
        outfile.write(jsonFile)

def readScoreJson():
    path = "costumize/score.json"
    read = open(path)
    jsonText = read.read()

    jsonFile = json.loads(jsonText)

    score = jsonFile['score']
    print(score)
    return score

def game(nameOfFile):

    try:
        cell_size,cells_x,cells_y,fps,bridges=load_json(nameOfFile)
    except:
        cell_size = 20
        cells_x = 40
        cells_y = 25
        fps = 5
        bridges= []
    try:
        max_score=readScoreJson()
        print(max_score)
    except:
        max_score=0
    clock = pygame.time.Clock()
    run_game = True
    pause_game = True
    WIDTH=cells_x*cell_size
    HEIGHT=cells_y*cell_size
    WIN = pygame.display.set_mode((WIDTH, HEIGHT+40))
    lastKey = pygame.K_UP
    snakeFirstPosition = pygame.Rect(WIDTH // 2 - (WIDTH / 2) % cell_size, HEIGHT // 2 - (HEIGHT / 2) % cell_size,
                                     cell_size, cell_size)
    SNAKE=[]
    SNAKE.append(snakeFirstPosition)
    food = manager_food(SNAKE,cell_size,WIDTH,HEIGHT,bridges)

    while run_game:
        clock.tick(fps)
        SNAKE_COLOR = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                    if not ( ( lastKey==pygame.K_LEFT and event.key == pygame.K_RIGHT ) or
                    ( lastKey == pygame.K_RIGHT and event.key == pygame.K_LEFT ) or
                    ( lastKey == pygame.K_DOWN and event.key == pygame.K_UP ) or
                    ( lastKey == pygame.K_UP and event.key == pygame.K_DOWN )
                    ):
                        lastKey=event.key
                        pause_game=True
                if event.key == pygame.K_ESCAPE:
                    pause_game = False
        if pause_game:
            check_move, food =move_snake(lastKey,food,SNAKE, cell_size, WIDTH, HEIGHT,bridges)
            if check_move==False :
                a=draw_lose(WIDTH,HEIGHT)

                if len(SNAKE)>max_score:
                    writeScoreJson(len(SNAKE))
                if a==-1:
                    return -1
                if nameOfFile == "default":
                    return 1
                else:
                    return 2
            draw_game(cell_size,cells_x,cells_y,food, SNAKE,bridges,max_score)
        else:
            game_pause(WIDTH,HEIGHT)



def main():

    #initialize menu
    run_app=True
    page=0
    while run_app:

        if page==-1:
            run_app = False
        if page==0:
            page = menu()
        if page==1: #start new game
            page = game("default")
        if page == 2:
            page = game("costumize")



    pygame.display.set_caption("Snake Menu")



if __name__ == '__main__':
    main()