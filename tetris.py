#!/usr/bin/env python3
# 
# (For english check below :) )
#
# Tetris
#
# Przyciski sterujące: 
# Strzałka w lewo/prawo - przesuń element w lewo/prawo
#       Strzałka w górę - obróć element zgodnie z ruchem wskazówek zegara
#        Strzałka w dół - przyspiesz spadanie elementu
#      Klawisz 'Spacja' - natychmiast opuść element na dół
#           Klawisz 'P' - przerwij grę 
#         Klawisz 'Esc' - zakończ grę
#
#
# Tetris
# 
# Control keys:
# Left/Right - Move stone left/right
#         Up - Rotate stone clockwise
#       Down - Drop stone faster
#      Space - Instant drop
#          P - Pause game
#     Escape - Quit game


import pygame, random, time, os
from pygame.locals import *
from sys import exit

# The configuration of game's window
cell_size=20
cols=10
rows=20
window_width=360
window_height=rows*cell_size
right_margin=cols*cell_size+cell_size
top_margin=0
maxfps=25

# The configuration of possible stone's shapes

O_shapes = [[[0, 0, 0, 0 ,0],
             [0, 0, 0, 0, 0],
             [0, 1, 1, 0, 0],
             [0, 1, 1, 0, 0],
             [0, 0, 0, 0, 0]]]

I_shapes = [[[0, 0, 2, 0 ,0],
             [0, 0, 2, 0, 0],
             [0, 0, 2, 0, 0],
             [0, 0, 2, 0, 0],
             [0, 0, 0, 0, 0]],
            
            [[0, 0, 0, 0 ,0],
             [0, 0, 0, 0, 0],
             [2, 2, 2, 2, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]]]

S_shapes = [[[0, 0, 0, 0 ,0],
             [0, 0, 0, 0, 0],
             [0, 0, 3, 3, 0],
             [0, 3, 3, 0, 0],
             [0, 0, 0, 0, 0]],
            
            [[0, 0, 0, 0 ,0],
             [0, 0, 3, 0, 0],
             [0, 0, 3, 3, 0],
             [0, 0, 0, 3, 0],
             [0, 0, 0, 0, 0]]]

Z_shapes = [[[0, 0, 0, 0 ,0],
             [0, 0, 0, 0, 0],
             [0, 4, 4, 0, 0],
             [0, 0, 4, 4, 0],
             [0, 0, 0, 0, 0]],
            
            [[0, 0, 0, 0 ,0],
             [0, 0, 4, 0, 0],
             [0, 4, 4, 0, 0],
             [0, 4, 0, 0, 0],
             [0, 0, 0, 0, 0]]]

L_shapes = [[[0, 0, 0, 0 ,0],
             [0, 0, 5, 0, 0],
             [0, 0, 5, 0, 0],
             [0, 0, 5, 5, 0],
             [0, 0, 0, 0, 0]],
            
            [[0, 0, 0, 0 ,0],
             [0, 0, 0, 0, 0],
             [0, 5, 5, 5, 0],
             [0, 5, 0, 0, 0],
             [0, 0, 0, 0, 0]],
           
            [[0, 0, 0, 0 ,0],
             [0, 5, 5, 0, 0],
             [0, 0, 5, 0, 0],
             [0, 0, 5, 0, 0],
             [0, 0, 0, 0, 0]],
           
            [[0, 0, 0, 0 ,0],
             [0, 0, 0, 5, 0],
             [0, 5, 5, 5, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]]]

J_shapes = [[[0, 0, 0, 0 ,0],
             [0, 0, 6, 0, 0],
             [0, 0, 6, 0, 0],
             [0, 6, 6, 0, 0],
             [0, 0, 0, 0, 0]],
            
            [[0, 0, 0, 0 ,0],
             [0, 6, 0, 0, 0],
             [0, 6, 6, 6, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]],
           
            [[0, 0, 0, 0 ,0],
             [0, 0, 6, 6, 0],
             [0, 0, 6, 0, 0],
             [0, 0, 6, 0, 0],
             [0, 0, 0, 0, 0]],
           
            [[0, 0, 0, 0 ,0],
             [0, 0, 0, 0, 0],
             [0, 6, 6, 6, 0],
             [0, 0, 0, 6, 0],
             [0, 0, 0, 0, 0]]]

T_shapes = [[[0, 0, 0, 0 ,0],
             [0, 0, 0, 0, 0],
             [0, 7, 7, 7, 0],
             [0, 0, 7, 0, 0],
             [0, 0, 0, 0, 0]],
            
            [[0, 0, 0, 0 ,0],
             [0, 0, 7, 0, 0],
             [0, 7, 7, 0, 0],
             [0, 0, 7, 0, 0],
             [0, 0, 0, 0, 0]],
           
            [[0, 0, 0, 0 ,0],
             [0, 0, 7, 0, 0],
             [0, 7, 7, 7, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]],
           
            [[0, 0, 0, 0 ,0],
             [0, 0, 7, 0, 0],
             [0, 0, 7, 7, 0],
             [0, 0, 7, 0, 0],
             [0, 0, 0, 0, 0]]]

shapes=[O_shapes, I_shapes, S_shapes, Z_shapes, L_shapes, J_shapes, T_shapes]
stone_width=5
stone_height=5

# The configuration of stone's moving - timing

move_sideway_freq=0.15
move_down_freq=0.1

# The configuration of colors

white=(255,255,255)
gray=(185,185,185)
black=(0,0,0)

red=(155,0,0)
lightred=(175,20,20)
green=(0,155,0)
lightgreen=(20,175,20)
blue=(0,0,155)
lightblue=(20,20,175)
yellow=(155,155,0)
lightyellow=(175,175,20)
orange=(244,70,17)
lightorange=(255,164,32)
purple=(222,76,138)
lightpurple=(146,78,125)
brown=(76,47,39)
lightbrown=(142,64,42)

colors=(red,green,blue,yellow,orange,purple,brown)
lightcolors=(lightred,lightgreen,lightblue,lightyellow,lightorange,lightpurple,lightbrown)

class Tetris:
    def __init__(self):
        """
        Initializing parameters and PyGame modules.
        """
        pygame.init()
        
        self.clock=pygame.time.Clock()
        
        pygame.display.set_caption('Tetris')
        self.window = pygame.display.set_mode((window_width, window_height), DOUBLEBUF)
        self.font =  pygame.font.Font(pygame.font.get_default_font(), 18)
        pygame.event.set_blocked(MOUSEMOTION)
        
        self.stone=None
        self.next_shape=random.choice(range(0,len(shapes)))
        self.next_rotation=random.choice(range(0,len(shapes[self.next_shape])))
        self.next_stone = shapes[self.next_shape][self.next_rotation]
        
            
    def showText(self,text,color=white):
        """
        This function displays text in the center of the window until a key is pressed.
        """
        surf=self.font.render(text, True, color)
        rect=surf.get_rect()
        rect.center=(int(window_width/2)-3, int(window_height/2)-3)
        self.window.blit(surf, rect)
        
        pressSurf=self.font.render('Press a key to play.',True, color)
        pressRect=pressSurf.get_rect()
        pressRect.center=(int(window_width/2), int(window_height/2)+20)
        self.window.blit(pressSurf, pressRect)
        
        while self.checkPress()==None:
            pygame.display.update()
            self.clock.tick()
            
    def checkQuit(self):
        """
        Check if any QUIT event or ESCAPE is pressed.
        """
        for event in pygame.event.get(QUIT):
            self.gameExit()
        for event in pygame.event.get(KEYUP):
            if event.key==K_ESCAPE:
                self.gameExit()
            pygame.event.post(event)
            
    def checkPress(self):
        """
        Check if any key is pressed.
        """
        self.checkQuit()
       
        for event in pygame.event.get([KEYDOWN, KEYUP]):
            if event.type==KEYDOWN and event.key!=K_ESCAPE:
                continue
            return event.key
        return None

    def newStone(self):
        """
        Return the new random stone.
        """
        self.stone=self.next_stone
        self.shape=self.next_shape
        self.rotation=self.next_rotation
        self.next_shape=random.choice(range(0,len(shapes)))
        self.next_rotation=random.choice(range(0,len(shapes[self.next_shape])))
        self.next_stone = shapes[self.next_shape][self.next_rotation]
        self.stoneX=int(cols/2)-int(stone_width/2)
        self.stoneY=-2
    
    def levelAndFreq(self):
        """
        Calculate level and fall frequency (how many seconds pass until a falling stone falls one space).
        """
        self.level=int(self.score/10)+1
        self.fall_freq=0.27-(self.level*0.02)
    
    
    def createBoard(self):
        """
        Create and return a new board of game.
        """
        self.board=[]
        for i in range(cols):
            self.board.append([0]*rows)
    
    def addToBoard(self, board, stone):
        """
        Fill stone in the board (the stone is added to the board after it's landed).
        """
        for x in range(stone_width):
            for y in range(stone_height):
                if stone[y][x]!=0:
                    board[x+self.stoneX][y+self.stoneY]=stone[y][x]
    
    def ifOnBoard(self,x,y):
        """
        Return true if x and y are on board.
        """
        return x>=0 and x<cols and y>=0 and y<rows
    
    def ifValid(self, board, stone, adjX=0, adjY=0):
        """
        Return true if the stone is within the board and not colliding.
        """
        for x in range(stone_width):
            for y in range(stone_height):
                is_above_board=y+self.stoneY+adjY<0
                if is_above_board or stone[y][x]==0:
                    continue
                if not self.ifOnBoard(x+self.stoneX+adjX, y+self.stoneY+adjY):
                    return False
                if board[x+self.stoneX+adjX][y+self.stoneY+adjY]!=0:
                    return False
        return True
    
    def ifCompleteLine(self, board, y):
        """
        Return True if the line is filled with boxes and has no gaps.
        """
        for x in range(cols):
            if board[x][y]==0:
                return False
        return True
    
    def deleteLine(self, board):
        """
        Remove all completed lines on the board, move everything above them down 
        and return the number of deleted lines.
        """
        lines=0
        y=rows-1
        while y>=0:
            if self.ifCompleteLine(board,y):
                path=os.path.dirname(os.path.realpath(__file__))
                complete_line_music=pygame.mixer.Sound(os.path.join(path, 'coins.wav'))
                pygame.mixer.Sound.play(complete_line_music)
                for p in range(y,0,-1):
                    for x in range(cols):
                        board[x][p]=board[x][p-1]
                for x in range(cols):
                    board[x][0]=0
                lines+=1
            else:
                y-=1            
        return lines
    
    def drawBox(self, box_x, box_y, color, pixel_x=None, pixel_y=None):
        """
        Draw a single box (one pixel) on the board. Box_x and box_y - 
        parameters for board coordinates where the box should be drawn.
        The pixel_x alb pixel_y - parameters used to draw the boxes of the 
        "Next:" stone, which is not on the board.
        """
        if color==0:
            return
        if pixel_x==None and pixel_y==None:
            pixel_x, pixel_y = box_x*cell_size, box_y*cell_size
        pygame.draw.rect(self.window, colors[color-1], (pixel_x+1, pixel_y+1, cell_size-1, cell_size-1))
        pygame.draw.rect(self.window, lightcolors[color-1], (pixel_x+1, pixel_y+1, cell_size-4, cell_size-4))
                         
    def drawBoard(self, board):
        """
        Draw the border around the board.
        """
        pygame.draw.rect(self.window,gray, (0, top_margin, cell_size*cols, cell_size*rows))
        for x in range(cols):
            for y in range(rows):
                self.drawBox(x,y,board[x][y])
                
    def drawStone(self, stone, pixel_x=None, pixel_y=None):
        """
        Drawing the boxes of the stone. This function will be used to draw falling stones or the "next" stone.
        """
        if pixel_x==None and pixel_y==None:
            pixel_x, pixel_y=self.stoneX*cell_size, self.stoneY*cell_size
        
        for x in range(stone_width):
            for y in range(stone_height):
                if stone[y][x]!=0:
                    self.drawBox(None,None,stone[y][x],pixel_x+x*(cell_size), pixel_y+(y*cell_size))
        
        
    def drawScore(self,score,level):
        """
        Drawing the score and the level text.
        """
        score_surf=self.font.render('Score: %s' % score, True, white)
        score_rect=score_surf.get_rect()
        score_rect.topleft=(right_margin,20)
        self.window.blit(score_surf, score_rect)
        
        level_surf=self.font.render('Level: %s' % level, True, white)
        level_rect=level_surf.get_rect()
        level_rect.topleft=(right_margin,60)
        self.window.blit(level_surf, level_rect)
        
    def drawNext(self, stone):
        """
        Drawing the "next" stone.
        """
        next_surf=self.font.render('Next:', True, white)
        next_rect=next_surf.get_rect()
        next_rect.topleft=(right_margin,100)
        self.window.blit(next_surf, next_rect)
        self.drawStone(stone, pixel_x=right_margin, pixel_y=120)
                          
    def gameExit(self):
        """
        Closing game. 
        """
        pygame.quit()
        exit()    
        
    def execute(self):
        """
        Executing the new game.
        """
        self.showText('Tetris')
        while True:
            path=os.path.dirname(os.path.realpath(__file__))
            music_file=os.path.join(path, 'arcade-music-loop.wav')
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1,0.0)
            
            #the main loop of the game
            self.runGame()
            
            pygame.mixer.music.stop()
            self.showText('Game Over')
        
    def runGame(self):
        """
        Setup variables for the start of the game and the main loop.
        """
        self.createBoard()
        last_move_down_time=time.time()
        last_move_sideways_time=time.time()
        last_fall_time=time.time()
        moving_down=False
        moving_left=False
        moving_right=False
        self.score=0
        self.levelAndFreq() #create self.level, self.fall_freq
        
        #the main loop of the game 
        while True:
            if self.stone==None:
                self.newStone()
                last_fall_time=time.time()

            if not self.ifValid(self.board, self.stone):
                return
            
            self.checkQuit()
            for event in pygame.event.get():
                if event.type==KEYUP:
                    if event.key==K_p:
                        self.window.fill(black)
                        pygame.mixer.music.pause()
                        self.showText('Paused')
                        pygame.mixer.music.unpause()
                        last_fall_time=time.time()
                        last_move_down_time=time.time()
                        last_move_sideways_time=time.time()
                    elif event.key==K_LEFT:
                        moving_left=False
                    elif event.key==K_RIGHT:
                        moving_right=False
                    elif event.key==K_DOWN:
                        moving_down=False
                        
                elif event.type==KEYDOWN:
                    if event.key==K_LEFT and self.ifValid(self.board,self.stone,adjX=-1):
                        self.stoneX-=1
                        moving_left=True
                        moving_right=False
                        last_move_sideways_time=time.time()

                    elif event.key==K_RIGHT and self.ifValid(self.board,self.stone,adjX=1):
                        self.stoneX+=1
                        moving_left=False
                        moving_right=True
                        last_move_sideways_time=time.time()

                    elif event.key==K_UP and self.ifValid(self.board,self.stone,adjX=-1):
                        self.rotation=(self.rotation+1)%len(shapes[self.shape])
                        self.stone=shapes[self.shape][self.rotation]
                        if not self.ifValid(self.board,self.stone):
                            self.rotation=(self.rotation-1)%len(shapes[self.shape])
                            self.stone=shapes[self.shape][self.rotation]
                    
                    elif event.key==K_DOWN:
                        moving_down=True

                        if self.ifValid(self.board, self.stone, adjY=1):
                            self.stoneY+=1
                        last_move_down=time.time()
                        
                    elif event.key==K_SPACE:
                        moving_down=False
                        moving_left=False
                        moving_right=False
                        for i in range(1, rows):
                            if not self.ifValid(self.board, self.stone, adjY=i):
                                break
                        self.stoneY += i-1
                        
            if (moving_left or moving_right) and time.time() - last_move_sideways_time>move_sideway_freq:
                if moving_left and self.ifValid(self.board, self.stone, adjX=-1):
                    self.stoneX-=1
                elif moving_right and self.ifValid(self.board, self.stone, adjX=1):
                    self.stoneX+=1
                last_move_sideways_time=time.time()
                
            if moving_down and time.time() - last_move_down_time>move_down_freq and self.ifValid(self.board, self.stone, adjY=1):
                self.stoneY+=1
                last_move_down_time=time.time()
                
            if time.time()-last_fall_time>self.fall_freq:
                if not self.ifValid(self.board, self.stone, adjY=1):
                    self.addToBoard(self.board, self.stone)
                    self.score+=self.deleteLine(self.board)
                    self.levelAndFreq()
                    self.stone=None
                else:
                    self.stoneY+=1
                    last_fall_time=time.time()
            
            #drawing everything on the screen
            self.window.fill(black)
            self.drawBoard(self.board)
            self.drawScore(self.score, self.level)
            self.drawNext(self.next_stone)
            if self.stone != None:
                self.drawStone(self.stone)
            pygame.display.update()
            self.clock.tick(maxfps)
                

if __name__ == '__main__' :
    App = Tetris()
    App.execute()
