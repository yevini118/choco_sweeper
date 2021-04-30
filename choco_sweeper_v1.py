#쪼꼬찾기

import random, pygame, sys, time
from pygame.locals import *

#SIZES
WINDOWWIDTH = 800
WINDOWHEIGHT = 650
GAMEWIDTH = 750
GAMEHEIGHT = 500
CELLSIZE = 25
CELLWIDTH = int(GAMEWIDTH/CELLSIZE)
CELLHEIGHT = int(GAMEHEIGHT/CELLSIZE)
MONITORWIDTH = CELLSIZE*5
MONITORHEIGHT = CELLSIZE*3

XMARGIN = CELLSIZE
YMARGIN = CELLSIZE*5

#RGB
BGCOLOR =(213, 192, 170)
LINECOLOR = (179, 140, 101)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 176, 80)
DARKGREEN = (56, 87, 35)
BLUE = (0, 112, 192)
DARKBLUE = (0, 32, 96)
RED = (255, 0, 0)
DARKRED = (192, 0, 0)
TRANSRED = (255, 0, 0, 60)
PINK = (227, 134, 134)
YELLOW = (255, 230, 153)


#SYNTAX SUGAR
POO = -1
NONE = 0
FLAG = -1
OPENED = 1

POOCOUNT = 110



def main():

      global DISPLAYSURF, BASICFONT, CHOCOIMG

      pygame.init()
      DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
      BASICFONT = pygame.font.Font('source/Jalnan.ttf',18)
      pygame.display.set_caption('Choco Sweeper')
      CHOCOIMG = pygame.image.load('source/choco.png')
      pygame.display.set_icon(CHOCOIMG)

      showStartScreen()
      while True:
            runGame()


def runGame():

      resetButton, boardSurf = drawBorder()
      board = getStartingBoard()
      startTime = 0
      
      while True:

            cellx, celly = None, None

            #click event
            for event in pygame.event.get():
                  if event.type == QUIT:
                        terminate()
                  elif event.type == MOUSEBUTTONUP:

                        cellx, celly =  getSpotClicked(board, event.pos[0], event.pos[1])
                        
                        if event.button == 1:  #left click
                              
                              if resetButton.collidepoint(event.pos): #resetButton pressed
                                    playButtonSound()
                                    return

                              elif boardSurf.collidepoint(event.pos) : #board pressed
                                    if startTime == 0: #timer on
                                          startTime = time.time()
                                    index = getBoardIndex(cellx, celly)
                                    setFlagOpened(board[index])
                                    
                        elif event.button == 3:  #right click
                              if boardSurf.collidepoint(event.pos):
                                    index = getBoardIndex(cellx, celly)
                                    setFlagFlag(board[index])
                                    
            
            for cell in board:
                  if cell['count'] == 0 and cell['flag'] == OPENED: #open cell if there`s no poo around
                        setAroundOpened(board, cell)
                        

            for cell in board:
                  if cell['count'] == POO and cell['flag'] == OPENED: #GAME OVER

                        for cell in board: #open all poo left
                              if cell['count'] == POO :
                                    setFlagOpened(cell)
                                    
                        drawBoard(board, startTime)
                        showGameOverScreen(board, cellx, celly)

                        if checkForNext(resetButton) == 1:
                              return
                        
            else:
                  drawBoard(board, startTime)

                  if getPooCount(board) == 0:
                        for cell in board:
                              if cell['flag'] == FLAG and cell['count'] != POO: #wrong flag
                                    break
                              if cell['flag'] == NONE and cell['count'] != POO: #not poo cell not opened
                                    break
                        else: #YOUWIN!
                              showYouWinScreen()
                              if checkForNext(resetButton) == 1:
                                    return


def getRandomPoo():

      poos = []

      while len(poos) < POOCOUNT :
            x = random.randint(0, CELLWIDTH-1)
            y = random.randint(0, CELLHEIGHT-1)
            poo = {'x': x, 'y': y}
            if poo not in poos:
                  poos.append(poo)

      return poos


def getStartingBoard():

      poos = getRandomPoo()

      board = []
      for x in range(CELLWIDTH):
            for y in range(CELLHEIGHT):

                  count = 0
                  if {'x': x, 'y': y} in poos:
                        count = POO
                  else:
                        if {'x': x-1, 'y': y-1} in poos:
                              count +=1
                        if {'x': x, 'y': y-1} in poos:
                              count +=1
                        if {'x': x+1, 'y': y-1} in poos:
                              count +=1
                        if {'x': x-1, 'y': y} in poos:
                              count +=1                              
                        if {'x': x+1, 'y': y} in poos:
                              count +=1                  
                        if {'x': x-1, 'y': y+1} in poos:
                              count +=1
                        if {'x': x, 'y': y+1} in poos:
                              count +=1
                        if {'x': x+1, 'y': y+1} in poos:
                              count +=1

                  cell = {'x': x, 'y': y, 'count' : count, 'flag': NONE}
                  board.append(cell)
                  
      return board


def getBoardIndex(cellx, celly):
      
      if cellx<0 or cellx> CELLWIDTH - 1 or celly<0 or celly> CELLHEIGHT - 1: #out of board
            return None
      else:
            return cellx * CELLHEIGHT + celly


def getPosOfCell(cellx, celly):
      x = cellx*CELLSIZE + XMARGIN
      y = celly*CELLSIZE + YMARGIN

      return (x, y)


def getSpotClicked(board, x, y):
      for cell in board:
            cellx, celly = cell['x'], cell['y']
            posx, posy = getPosOfCell(cellx, celly)
            cellRect = pygame.Rect(posx, posy, CELLSIZE, CELLSIZE)
            if cellRect.collidepoint(x, y):
                  return (cellx, celly)
      return (None, None)


def getPooCount(board):

      count = POOCOUNT
      for cell in board:
            if cell['flag'] == FLAG:
                  count -=1

      return count
                              
      
def setFlagOpened(cell):

      if cell['flag'] == NONE:
            cell['flag'] = OPENED  
  

def setFlagFlag(cell):

      if cell['flag'] == NONE:
            cell['flag'] = FLAG
                  
      elif cell['flag'] == FLAG:
            cell['flag'] = NONE
                              

def setAroundOpened(board, cell):

      topLeft = getBoardIndex(cell['x']-1, cell['y']-1)
      topMiddle = getBoardIndex(cell['x'], cell['y']-1)
      topRight = getBoardIndex(cell['x']+1, cell['y']-1)
      middleLeft = getBoardIndex(cell['x']-1, cell['y'])
      middleRight = getBoardIndex(cell['x']+1, cell['y'])
      bottomLeft = getBoardIndex(cell['x']-1, cell['y']+1)
      bottomMiddle = getBoardIndex(cell['x'], cell['y']+1)
      bottomRight = getBoardIndex(cell['x']+1, cell['y']+1)
      
      if topLeft != None:
            board[topLeft]['flag'] = OPENED
      if topMiddle != None:
            board[topMiddle]['flag'] = OPENED
      if topRight != None:
            board[topRight]['flag'] = OPENED
      if middleLeft != None:
            board[middleLeft]['flag'] = OPENED
      if middleRight != None:
            board[middleRight]['flag'] = OPENED
      if bottomLeft != None:
            board[bottomLeft]['flag'] = OPENED
      if bottomMiddle != None:
            board[bottomMiddle]['flag'] = OPENED
      if bottomRight != None:
            board[bottomRight]['flag'] = OPENED  


def checkForNext(resetButton) :

      while True:
            for event in pygame.event.get():
                  if event.type == QUIT:
                        terminate()
                  elif event.type == MOUSEBUTTONUP:

                        if event.button == 1:  #left click
                  
                              if resetButton.collidepoint(event.pos):
                                    playButtonSound()
                                    return 1            


def drawBorder():

      DISPLAYSURF.fill(BGCOLOR)

      resetButtonRect = pygame.Rect(WINDOWWIDTH/2-MONITORHEIGHT/2, CELLSIZE, MONITORHEIGHT, MONITORHEIGHT)
      pygame.draw.rect(DISPLAYSURF, LINECOLOR, resetButtonRect)
      resetButtonInnerRect = pygame.Rect(WINDOWWIDTH/2-(MONITORHEIGHT)/2+4, CELLSIZE+4, MONITORHEIGHT-8, MONITORHEIGHT-8)
      pygame.draw.rect(DISPLAYSURF, WHITE, resetButtonInnerRect)
  
      chocoImg_scale = pygame.transform.scale(CHOCOIMG, (MONITORHEIGHT-10,MONITORHEIGHT-10))
      chocox = WINDOWWIDTH/2-(MONITORHEIGHT)/2+5
      chocoy = CELLSIZE+5
      DISPLAYSURF.blit(chocoImg_scale, (chocox, chocoy))
      
      pooCountRect = pygame.Rect(CELLSIZE, CELLSIZE, MONITORWIDTH, MONITORHEIGHT)
      pygame.draw.rect(DISPLAYSURF, LINECOLOR, pooCountRect)
      pooCountInnerRect = pygame.Rect(CELLSIZE+4, CELLSIZE+4, MONITORWIDTH-8, MONITORHEIGHT-8)
      pygame.draw.rect(DISPLAYSURF, WHITE, pooCountInnerRect)

      timerRect = pygame.Rect(WINDOWWIDTH - CELLSIZE*6, CELLSIZE, MONITORWIDTH, MONITORHEIGHT)
      pygame.draw.rect(DISPLAYSURF, LINECOLOR, timerRect)  
      timerInnerRect = pygame.Rect(WINDOWWIDTH - CELLSIZE*6+4, CELLSIZE+4, MONITORWIDTH-8, MONITORHEIGHT-8)
      pygame.draw.rect(DISPLAYSURF, WHITE, timerInnerRect)

      boardRect = pygame.Rect(XMARGIN, YMARGIN, CELLSIZE*30, CELLSIZE*20)
        
      pygame.display.update()

      return resetButtonRect, boardRect


def drawBoard(board, startTime):

      pooImg = pygame.image.load('source/poo.png')
      pooImg_scale = pygame.transform.scale(pooImg, (CELLSIZE, CELLSIZE))
      flagImg = pygame.image.load('source/paw.png')
      flagImg_scale = pygame.transform.scale(flagImg, (CELLSIZE-3, CELLSIZE-3))
      
      #draw inside of cell
      for cell in board:

            posx, posy = getPosOfCell(cell['x'], cell['y'])

            if cell['flag'] == OPENED:
                   
                  cellRect = pygame.Rect(posx, posy, CELLSIZE, CELLSIZE)
                  pygame.draw.rect(DISPLAYSURF, WHITE, cellRect)

                  if cell['count'] == POO:
                        DISPLAYSURF.blit(pooImg_scale, (posx, posy))
                  else:
                        if cell['count'] == 0:
                              color = WHITE
                        elif cell['count'] == 1:
                              color = BLUE
                        elif cell['count'] == 2:
                              color = GREEN
                        elif cell['count'] == 3: 
                              color = RED
                        elif cell['count'] == 4:
                              color = DARKBLUE
                        elif cell['count'] == 5:
                              color = DARKRED
                        elif cell['count'] == 6:
                              color = DARKGREEN
                        elif cell['count'] == 7:
                              color = BLACK
                        elif cell['count'] == 8:    
                              color = PINK       

                        cellStatusFont = BASICFONT.render(str(cell['count']), True, color)
                        cellStatusRect = cellStatusFont.get_rect()
                        cellStatusRect.topleft = (posx+7, posy+4)
                        DISPLAYSURF.blit(cellStatusFont, cellStatusRect)  

            elif cell['flag'] == FLAG:
                  
                  DISPLAYSURF.blit(flagImg_scale, (posx+2, posy+2))

            elif cell['flag'] == NONE:
                  
                  cellRect = pygame.Rect(posx, posy, CELLSIZE, CELLSIZE)
                  pygame.draw.rect(DISPLAYSURF, BGCOLOR, cellRect)
                  
      #draw lines of cell
      for x in range(XMARGIN, WINDOWWIDTH, CELLSIZE):
            pygame.draw.line(DISPLAYSURF, LINECOLOR, (x, YMARGIN), (x, WINDOWHEIGHT-CELLSIZE), 3)
      for y in range(YMARGIN, WINDOWHEIGHT, CELLSIZE):
            pygame.draw.line(DISPLAYSURF, LINECOLOR, (XMARGIN, y), (WINDOWWIDTH-CELLSIZE, y), 3) 

      #draw counter
      count = getPooCount(board)
      countFont = pygame.font.Font('source/Jalnan.ttf',45)
      countSurf = countFont.render(str(count), True, PINK)
      countRect = countSurf.get_rect()
      countRect.center = (CELLSIZE*3.5, CELLSIZE*2.5)
      countBGRect = pygame.Rect(CELLSIZE, CELLSIZE, MONITORWIDTH-10, MONITORHEIGHT-10)
      countBGRect.center = (CELLSIZE*3.5, CELLSIZE*2.5)
      pygame.draw.rect(DISPLAYSURF, WHITE, countBGRect)
      DISPLAYSURF.blit(countSurf, countRect)

      #draw timer
      nowTime = time.time()
      passTime = int(nowTime - startTime)
      if startTime == 0 :
            passTime = 0
      timerFont = pygame.font.Font('source/Jalnan.ttf',45)
      timerSurf = timerFont.render(str(passTime), True, PINK)
      timerRect = timerSurf.get_rect()
      timerRect.center = (WINDOWWIDTH - CELLSIZE*3.5, CELLSIZE*2.5)
      pygame.draw.rect(DISPLAYSURF, WHITE, timerRect)
      DISPLAYSURF.blit(timerSurf, timerRect)

      pygame.display.update()


def showStartScreen():

      #bgm
      startMusic = pygame.mixer.Sound('source/Pop Goes The Weasel.mp3')
      startMusic.play()


      
      #pattern
      DISPLAYSURF.fill(WHITE)
      patternImg = pygame.image.load('source/pattern.png')
      patternx, patterny = 0,0
      DISPLAYSURF.blit(patternImg, (patternx, patterny))

      #title
      titleFont = pygame.font.Font('source/Jalnan.ttf',100)
      titleSurf1 = titleFont.render('CHOCO', True, LINECOLOR)
      titleRect1 = titleSurf1.get_rect()
      titleRect1.center = (WINDOWWIDTH/2, 100)
      DISPLAYSURF.blit(titleSurf1, titleRect1)
      
      titleSurf2 = titleFont.render('SWEEPER', True, LINECOLOR)
      titleRect2 = titleSurf2.get_rect()
      titleRect2.center = (WINDOWWIDTH/2, 200)
      DISPLAYSURF.blit(titleSurf2, titleRect2)

      shadowFont = pygame.font.Font('source/Jalnan.ttf', 100)
      shadowSurf1 = shadowFont.render('CHOCO', True, PINK)
      shadowRect1 = shadowSurf1.get_rect()
      shadowRect1.center = (WINDOWWIDTH/2+7, 100+7)
      DISPLAYSURF.blit(shadowSurf1, shadowRect1)
      
      shadowSurf2 = shadowFont.render('SWEEPER', True, PINK)
      shadowRect2 = shadowSurf2.get_rect()
      shadowRect2.center = (WINDOWWIDTH/2+7, 200+7)   
      DISPLAYSURF.blit(shadowSurf2, shadowRect2)

      #chocoImg  
      chocoImg_scale = pygame.transform.scale(CHOCOIMG, (300,300))
      chocox = WINDOWWIDTH/2-150
      chocoy = 230
      DISPLAYSURF.blit(chocoImg_scale, (chocox, chocoy))

      #start
      startFont = pygame.font.Font('source/Jalnan.ttf',50)
      startSurf1 = startFont.render('START', True, LINECOLOR)
      startRect1 = startSurf1.get_rect()
      startRect1.center = (WINDOWWIDTH/2, 550)
      startSurf2 = startFont.render('START', True, YELLOW)
      startRect2 = startSurf2.get_rect()
      startRect2.center = (WINDOWWIDTH/2, 550)

      heartSurf = startFont.render('♡', True, PINK)
      heartRect1 = heartSurf.get_rect()
      heartRect1.center = (WINDOWWIDTH/2 - 120, 550)
      heartRect2 = heartSurf.get_rect()
      heartRect2.center = (WINDOWWIDTH/2 + 120, 550)
      DISPLAYSURF.blit(heartSurf, heartRect1)
      DISPLAYSURF.blit(heartSurf, heartRect2)

      #copyright
      copyrightFont = BASICFONT.render('ⓒ2021.yevini All rights reserved', True, BGCOLOR)
      copyrightRect = copyrightFont.get_rect()
      copyrightRect.bottomleft = (CELLSIZE, WINDOWHEIGHT - CELLSIZE)
      DISPLAYSURF.blit(copyrightFont, copyrightRect)  

      
      while True:

            DISPLAYSURF.blit(startSurf1, startRect1)
            pygame.display.update()
            pygame.time.wait(300)
            DISPLAYSURF.blit(startSurf2, startRect2)
            pygame.display.update()
            pygame.time.wait(300)

            for event in pygame.event.get():
                  if event.type == QUIT:
                        terminate()
                  elif event.type == MOUSEBUTTONUP:
                        mousex, mousey = event.pos
                        if startRect1.collidepoint((mousex, mousey)):
                              startMusic.stop()
                              buttonSound = pygame.mixer.Sound('source/buttonsound.mp3')
                              buttonSound.play()
                              return

def showYouWinScreen():

      happyChocoImg = pygame.image.load('source/happychoco.png')      
      chocoImg_scale = pygame.transform.scale(happyChocoImg, (MONITORHEIGHT-10,MONITORHEIGHT-10))
      chocox = WINDOWWIDTH/2-(MONITORHEIGHT)/2+5
      chocoy = CELLSIZE+5
      DISPLAYSURF.blit(chocoImg_scale, (chocox, chocoy)) 

      winFont = pygame.font.Font('source/Jalnan.ttf',50)
      winSurf1 = winFont.render('YOU', True, LINECOLOR)
      winRect1 = winSurf1.get_rect()
      winRect1.center = (WINDOWWIDTH/2-120, CELLSIZE*2.5)
      
      winSurf2 = winFont.render('WIN!', True, LINECOLOR)
      winRect2 = winSurf2.get_rect()
      winRect2.center = (WINDOWWIDTH/2+120, CELLSIZE*2.5)

      shadowFont = pygame.font.Font('source/Jalnan.ttf', 50)
      shadowSurf1 = shadowFont.render('YOU', True, PINK)
      shadowRect1 = shadowSurf1.get_rect()
      shadowRect1.center = (WINDOWWIDTH/2-120+4, CELLSIZE*2.5+4)
      
      shadowSurf2 = shadowFont.render('WIN!', True, PINK)
      shadowRect2 = shadowSurf2.get_rect()
      shadowRect2.center = (WINDOWWIDTH/2+120+4, CELLSIZE*2.5+4)  


      DISPLAYSURF.blit(shadowSurf1, shadowRect1)
      DISPLAYSURF.blit(shadowSurf2, shadowRect2)
      DISPLAYSURF.blit(winSurf1, winRect1)
      DISPLAYSURF.blit(winSurf2, winRect2)

      pygame.display.update()
            
      

def showGameOverScreen(board, cellx, celly):

      pooSound = pygame.mixer.Sound('source/poosound.mp3')
      pooSound.play()

      cryingChocoImg = pygame.image.load('source/cryingchoco.png')      
      chocoImg_scale = pygame.transform.scale(cryingChocoImg, (MONITORHEIGHT-10,MONITORHEIGHT-10))
      chocox = WINDOWWIDTH/2-(MONITORHEIGHT)/2+5
      chocoy = CELLSIZE+5
      DISPLAYSURF.blit(chocoImg_scale, (chocox, chocoy)) 


      overFont = pygame.font.Font('source/Jalnan.ttf',50)
      overSurf1 = overFont.render('GAME', True, LINECOLOR)
      overRect1 = overSurf1.get_rect()
      overRect1.center = (WINDOWWIDTH/2-140, CELLSIZE*2.5)
      
      overSurf2 = overFont.render('OVER', True, LINECOLOR)
      overRect2 = overSurf2.get_rect()
      overRect2.center = (WINDOWWIDTH/2+130, CELLSIZE*2.5)

      shadowFont = pygame.font.Font('source/Jalnan.ttf', 50)
      shadowSurf1 = shadowFont.render('GAME', True, PINK)
      shadowRect1 = shadowSurf1.get_rect()
      shadowRect1.center = (WINDOWWIDTH/2-140+4, CELLSIZE*2.5+4)
      
      shadowSurf2 = shadowFont.render('OVER', True, PINK)
      shadowRect2 = shadowSurf2.get_rect()
      shadowRect2.center = (WINDOWWIDTH/2+130+4, CELLSIZE*2.5+4)  


      DISPLAYSURF.blit(shadowSurf1, shadowRect1)
      DISPLAYSURF.blit(shadowSurf2, shadowRect2)
      DISPLAYSURF.blit(overSurf1, overRect1)
      DISPLAYSURF.blit(overSurf2, overRect2)

      posx, posy = getPosOfCell(cellx, celly)

      pooSurf = DISPLAYSURF.convert_alpha()
      pooSurf.fill((0,0,0,0))
      pooRect = pygame.Rect(posx, posy, CELLSIZE, CELLSIZE)
      pygame.draw.rect(pooSurf, TRANSRED, pooRect)


      for cell in board:
            if cell['count'] != POO and cell['flag'] == FLAG:
                  posx, posy = getPosOfCell(cell['x'], cell['y'])
                  pooRect = pygame.Rect(posx, posy, CELLSIZE, CELLSIZE)
                  pygame.draw.rect(pooSurf, TRANSRED, pooRect)                  


      DISPLAYSURF.blit(pooSurf, (0,0))

      pygame.display.update()


def playButtonSound():
      buttonSound = pygame.mixer.Sound('source/buttonsound.mp3')
      buttonSound.play()
            
            
def terminate():
      pygame.quit()
      sys.exit()

if __name__ == '__main__':
      main()


      
      
      



























      
      
