#쪼꼬찾기

import random, pygame, sys, time
from pygame.locals import *

#SIZES
WINDOWWIDTH = 800
WINDOWHEIGHT = 650
CELLSIZE = 25
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



def main():

      global DISPLAYSURF, GAMEDISPLAYSURF, GAMEWINDOWWIDTH, GAMEWINDOWHEIGHT, CELLWIDTH, CELLHEIGHT, POOCOUNT, BASICFONT, CHOCOIMG
     
      pygame.init()

      DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT), RESIZABLE)
      BASICFONT = pygame.font.Font('source/Jalnan.ttf',18)
      pygame.display.set_caption('Choco Sweeper')
      CHOCOIMG = pygame.image.load('source/choco.png')
      pygame.display.set_icon(CHOCOIMG)

      startMusic = showStartScreen()
      CELLWIDTH, CELLHEIGHT, POOCOUNT = showLevelScreen()
      startMusic.stop()
      GAMEWINDOWWIDTH, GAMEWINDOWHEIGHT = CELLSIZE * CELLWIDTH + XMARGIN * 2, CELLSIZE * CELLHEIGHT + YMARGIN + CELLSIZE
      GAMEDISPLAYSURF = pygame.display.set_mode((GAMEWINDOWWIDTH, GAMEWINDOWHEIGHT), RESIZABLE)

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
                                    cell = board[index]
                                    if cell['flag'] == OPENED:
                                          flagCount = getFlagCount(board, cell)

                                          doubleTime = time.time()
                                          doubleCheck = checkDouble(doubleTime, event.pos)
                                          if doubleCheck == 1 and cell['count'] == flagCount:
                                                setAroundOpened(board, cell)

                              
                                          
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


def getFlagCount(board, cell):

      count = 0
      topLeft = getBoardIndex(cell['x']-1, cell['y']-1)
      topMiddle = getBoardIndex(cell['x'], cell['y']-1)
      topRight = getBoardIndex(cell['x']+1, cell['y']-1)
      middleLeft = getBoardIndex(cell['x']-1, cell['y'])
      middleRight = getBoardIndex(cell['x']+1, cell['y'])
      bottomLeft = getBoardIndex(cell['x']-1, cell['y']+1)
      bottomMiddle = getBoardIndex(cell['x'], cell['y']+1)
      bottomRight = getBoardIndex(cell['x']+1, cell['y']+1)

      if topLeft != None:
            if board[topLeft]['flag'] == FLAG:
                  count +=1
      if topMiddle != None:
            if board[topMiddle]['flag'] == FLAG:
                  count +=1
      if topRight != None:
            if board[topRight]['flag'] == FLAG:
                  count +=1   
      if middleLeft != None:
            if board[middleLeft]['flag'] == FLAG:
                  count +=1   
      if middleRight != None:
            if board[middleRight]['flag'] == FLAG:
                  count +=1
      if bottomLeft != None:
            if board[bottomLeft]['flag'] == FLAG:
                  count +=1
      if bottomMiddle != None:
            if board[bottomMiddle]['flag'] == FLAG:
                  count +=1
      if bottomRight != None:
            if board[bottomRight]['flag'] == FLAG:
                  count +=1

      return count          


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
      
      if cellx<0 or cellx > CELLWIDTH - 1 or celly<0 or celly > CELLHEIGHT - 1: #out of board
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
      
      if topLeft != None and board[topLeft]['flag'] != FLAG:
            board[topLeft]['flag'] = OPENED
      if topMiddle != None and board[topMiddle]['flag'] != FLAG:
            board[topMiddle]['flag'] = OPENED
      if topRight != None and board[topRight]['flag'] != FLAG:
            board[topRight]['flag'] = OPENED
      if middleLeft != None and board[middleLeft]['flag'] != FLAG:
            board[middleLeft]['flag'] = OPENED
      if middleRight != None and board[middleRight]['flag'] != FLAG:
            board[middleRight]['flag'] = OPENED
      if bottomLeft != None and board[bottomLeft]['flag'] != FLAG:
            board[bottomLeft]['flag'] = OPENED
      if bottomMiddle != None and board[bottomMiddle]['flag'] != FLAG:
            board[bottomMiddle]['flag'] = OPENED
      if bottomRight != None and board[bottomRight]['flag'] != FLAG:
            board[bottomRight]['flag'] = OPENED  


def checkDouble(doubleTime,  firstPos):

      passTime = 0
      
      while( passTime < 0.5):
            passTime = time.time() - doubleTime
            for event in pygame.event.get():
                  if event.type == MOUSEBUTTONUP:
                        if event.pos == firstPos :
                              return 1
            
      else:
            return 0


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

      GAMEDISPLAYSURF.fill(BGCOLOR)

      resetButtonRect = pygame.Rect(GAMEWINDOWWIDTH/2-MONITORHEIGHT/2, CELLSIZE, MONITORHEIGHT, MONITORHEIGHT)
      pygame.draw.rect(GAMEDISPLAYSURF, LINECOLOR, resetButtonRect)
      resetButtonInnerRect = pygame.Rect(GAMEWINDOWWIDTH/2-(MONITORHEIGHT)/2+4, CELLSIZE+4, MONITORHEIGHT-8, MONITORHEIGHT-8)
      pygame.draw.rect(GAMEDISPLAYSURF, WHITE, resetButtonInnerRect)
  
      chocoImg_scale = pygame.transform.scale(CHOCOIMG, (MONITORHEIGHT-10,MONITORHEIGHT-10))
      chocox = GAMEWINDOWWIDTH/2-(MONITORHEIGHT)/2+5
      chocoy = CELLSIZE+5
      GAMEDISPLAYSURF.blit(chocoImg_scale, (chocox, chocoy))
      
      pooCountRect = pygame.Rect(CELLSIZE, CELLSIZE, MONITORWIDTH, MONITORHEIGHT)
      pygame.draw.rect(GAMEDISPLAYSURF, LINECOLOR, pooCountRect)
      pooCountInnerRect = pygame.Rect(CELLSIZE+4, CELLSIZE+4, MONITORWIDTH-8, MONITORHEIGHT-8)
      pygame.draw.rect(GAMEDISPLAYSURF, WHITE, pooCountInnerRect)

      timerRect = pygame.Rect(GAMEWINDOWWIDTH - CELLSIZE*6, CELLSIZE, MONITORWIDTH, MONITORHEIGHT)
      pygame.draw.rect(GAMEDISPLAYSURF, LINECOLOR, timerRect)  
      timerInnerRect = pygame.Rect(GAMEWINDOWWIDTH - CELLSIZE*6+4, CELLSIZE+4, MONITORWIDTH-8, MONITORHEIGHT-8)
      pygame.draw.rect(GAMEDISPLAYSURF, WHITE, timerInnerRect)

      boardRect = pygame.Rect(XMARGIN, YMARGIN, CELLSIZE*CELLWIDTH, CELLSIZE*CELLHEIGHT)
        
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
                  pygame.draw.rect(GAMEDISPLAYSURF, WHITE, cellRect)

                  if cell['count'] == POO:
                        GAMEDISPLAYSURF.blit(pooImg_scale, (posx, posy))
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
                        GAMEDISPLAYSURF.blit(cellStatusFont, cellStatusRect)  

            elif cell['flag'] == FLAG:
                  
                  GAMEDISPLAYSURF.blit(flagImg_scale, (posx+2, posy+2))

            elif cell['flag'] == NONE:
                  
                  cellRect = pygame.Rect(posx, posy, CELLSIZE, CELLSIZE)
                  pygame.draw.rect(GAMEDISPLAYSURF, BGCOLOR, cellRect)
                  
      #draw lines of cell
      for x in range(XMARGIN, GAMEWINDOWWIDTH, CELLSIZE):
            pygame.draw.line(GAMEDISPLAYSURF, LINECOLOR, (x, YMARGIN), (x, GAMEWINDOWHEIGHT-CELLSIZE), 3)
      for y in range(YMARGIN, GAMEWINDOWHEIGHT, CELLSIZE):
            pygame.draw.line(GAMEDISPLAYSURF, LINECOLOR, (XMARGIN, y), (GAMEWINDOWWIDTH-CELLSIZE, y), 3) 

      #draw counter
      count = getPooCount(board)
      countFont = pygame.font.Font('source/Jalnan.ttf',45)
      countSurf = countFont.render(str(count), True, PINK)
      countRect = countSurf.get_rect()
      countRect.center = (CELLSIZE*3.5, CELLSIZE*2.5)
      countBGRect = pygame.Rect(CELLSIZE, CELLSIZE, MONITORWIDTH-10, MONITORHEIGHT-10)
      countBGRect.center = (CELLSIZE*3.5, CELLSIZE*2.5)
      pygame.draw.rect(GAMEDISPLAYSURF, WHITE, countBGRect)
      GAMEDISPLAYSURF.blit(countSurf, countRect)

      #draw timer
      nowTime = time.time()
      passTime = int(nowTime - startTime)
      if startTime == 0 :
            passTime = 0
      timerFont = pygame.font.Font('source/Jalnan.ttf',45)
      timerSurf = timerFont.render(str(passTime), True, PINK)
      timerRect = timerSurf.get_rect()
      timerRect.center = (GAMEWINDOWWIDTH - CELLSIZE*3.5, CELLSIZE*2.5)
      pygame.draw.rect(GAMEDISPLAYSURF, WHITE, timerRect)
      GAMEDISPLAYSURF.blit(timerSurf, timerRect)

      pygame.display.update()


def drawErrorMessage(message):

      #errorMessageBackground
      errorBackRect = pygame.Rect(0, 0, 500, 40)
      errorBackRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT - 40)
      pygame.draw.rect(DISPLAYSURF, WHITE, errorBackRect)

      errorMessageSurf = BASICFONT.render( message , True, PINK)
      errorMessageRect = errorMessageSurf.get_rect()
      errorMessageRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT - 40)
      pygame.draw.rect(DISPLAYSURF, WHITE, errorMessageRect)
      DISPLAYSURF.blit(errorMessageSurf, errorMessageRect)   
      

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
                  
                        if startRect1.collidepoint((event.pos[0], event.pos[1])):
                              playButtonSound()
                              return startMusic


def showLevelScreen():

      while True :
            #pattern
            DISPLAYSURF.fill(WHITE)
            patternImg = pygame.image.load('source/pattern.png')
            patternx, patterny = 0,0
            DISPLAYSURF.blit(patternImg, (patternx, patterny))

            #level
            levelFont = pygame.font.Font('source/Jalnan.ttf',80)
            levelSurf = levelFont.render('- LEVEL -', True, LINECOLOR)
            levelRect = levelSurf.get_rect()
            levelRect.center = (WINDOWWIDTH/2, 150)
            DISPLAYSURF.blit(levelSurf, levelRect)

            shadowFont = pygame.font.Font('source/Jalnan.ttf', 80)
            shadowSurf = shadowFont.render('- LEVEL -', True, PINK)
            shadowRect = shadowSurf.get_rect()
            shadowRect.center = (WINDOWWIDTH/2+6, 150+6)
            DISPLAYSURF.blit(shadowSurf, shadowRect)

            levelBasicFont = pygame.font.Font('source/Jalnan.ttf', 50)

            beginnerSurf = levelBasicFont.render(' 초급 : 15 x 10 ', True, LINECOLOR)
            beginnerRect = beginnerSurf.get_rect()
            beginnerRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT - 360)
            beginnerLineRect = pygame.Rect(beginnerRect.x -4, beginnerRect.y-4, beginnerRect.w+8, beginnerRect.h+8)
            pygame.draw.rect(DISPLAYSURF, BGCOLOR, beginnerLineRect)
            pygame.draw.rect(DISPLAYSURF, WHITE, beginnerRect)
            DISPLAYSURF.blit(beginnerSurf, beginnerRect)

            intermediateSurf = levelBasicFont.render(' 중급 : 20 x 20 ', True, LINECOLOR)
            intermediateRect = intermediateSurf.get_rect()
            intermediateRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT - 270)
            intermediateLineRect = pygame.Rect(intermediateRect.x -4, intermediateRect.y-4, intermediateRect.w+8, intermediateRect.h+8)
            pygame.draw.rect(DISPLAYSURF, BGCOLOR, intermediateLineRect)
            pygame.draw.rect(DISPLAYSURF, WHITE, intermediateRect)
            DISPLAYSURF.blit(intermediateSurf, intermediateRect)

            advancedSurf = levelBasicFont.render(' 고급 : 30 x 20 ', True, LINECOLOR)
            advancedRect = advancedSurf.get_rect()
            advancedRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT - 180)
            advancedLineRect = pygame.Rect(advancedRect.x -4, advancedRect.y-4, advancedRect.w+8, advancedRect.h+8)
            pygame.draw.rect(DISPLAYSURF, BGCOLOR, advancedLineRect)
            pygame.draw.rect(DISPLAYSURF, WHITE, advancedRect)
            DISPLAYSURF.blit(advancedSurf, advancedRect)

            customSurf = levelBasicFont.render(' 커스텀 :  ? x ? ', True, LINECOLOR)
            customRect = customSurf.get_rect()
            customRect.center = (WINDOWWIDTH/2, WINDOWHEIGHT - 90)
            customLineRect = pygame.Rect(customRect.x -4, customRect.y-4, customRect.w+8, customRect.h+8)
            pygame.draw.rect(DISPLAYSURF, BGCOLOR, customLineRect)
            pygame.draw.rect(DISPLAYSURF, WHITE, customRect)
            DISPLAYSURF.blit(customSurf, customRect)

            pygame.display.update()
            
            for event in pygame.event.get():
                  if event.type == QUIT:
                        terminate()
                  elif event.type == MOUSEBUTTONUP:

                        if beginnerRect.collidepoint((event.pos[0], event.pos[1])):
                              playButtonSound()
                              return 15, 10, 20

                        elif intermediateRect.collidepoint((event.pos[0], event.pos[1])):
                              playButtonSound()
                              return 20, 20, 80

                        elif advancedRect.collidepoint((event.pos[0], event.pos[1])):
                              playButtonSound()
                              return 30, 20, 120

                        elif customRect.collidepoint((event.pos[0], event.pos[1])):
                              playButtonSound()
                              wNum, hNum, pNum = showCustomScreen(customRect)
                              if wNum ==0 and hNum==0 and pNum==0:
                                    continue
                              return wNum, hNum , pNum

                              



def showCustomScreen(customRect):

      message = "가로 15~60 세로 10~30 의 숫자를 입력하세요."
      drawErrorMessage(message)

      pygame.draw.rect(DISPLAYSURF, WHITE, customRect)

      customWidthSurf = BASICFONT.render(' 가로 : ', True, LINECOLOR)
      customWidthRect = customWidthSurf.get_rect()
      customWidthRect.center = (WINDOWWIDTH/2 - 140, WINDOWHEIGHT - 90)
      pygame.draw.rect(DISPLAYSURF, WHITE, customWidthRect)
      DISPLAYSURF.blit(customWidthSurf, customWidthRect)   

      customHeightSurf = BASICFONT.render(' 세로 : ', True, LINECOLOR)
      customHeightRect = customHeightSurf.get_rect()
      customHeightRect.center = (WINDOWWIDTH/2 - 30, WINDOWHEIGHT - 90)
      pygame.draw.rect(DISPLAYSURF, WHITE, customHeightRect)
      DISPLAYSURF.blit(customHeightSurf, customHeightRect)   

      customPooSurf = BASICFONT.render(' 지뢰 : ', True, LINECOLOR)
      customPooRect = customPooSurf.get_rect()
      customPooRect.center = (WINDOWWIDTH/2 + 90, WINDOWHEIGHT - 90) 
      pygame.draw.rect(DISPLAYSURF, WHITE, customPooRect)
      DISPLAYSURF.blit(customPooSurf, customPooRect) 

      customWTBoxRect = pygame.Rect(0, 0, 40, 30)
      customWTBoxRect.center = (WINDOWWIDTH/2 - 85, WINDOWHEIGHT - 90)
      customWTBoxLineRect = pygame.Rect(customWTBoxRect.x -4, customWTBoxRect.y-4, customWTBoxRect.w+8, customWTBoxRect.h+8)
      pygame.draw.rect(DISPLAYSURF, BGCOLOR, customWTBoxLineRect)
      pygame.draw.rect(DISPLAYSURF, WHITE, customWTBoxRect) 

      customHTBoxRect = pygame.Rect(0, 0, 40, 30)
      customHTBoxRect.center = (WINDOWWIDTH/2 + 25, WINDOWHEIGHT - 90)
      customHTBoxLineRect = pygame.Rect(customHTBoxRect.x -4, customHTBoxRect.y-4, customHTBoxRect.w+8, customHTBoxRect.h+8)
      pygame.draw.rect(DISPLAYSURF, BGCOLOR, customHTBoxLineRect)
      pygame.draw.rect(DISPLAYSURF, WHITE, customHTBoxRect) 

      customPTBoxRect = pygame.Rect(0, 0, 40, 30)
      customPTBoxRect.center = (WINDOWWIDTH/2 + 145, WINDOWHEIGHT - 90)
      customPTBoxLineRect = pygame.Rect(customPTBoxRect.x -4, customPTBoxRect.y-4, customPTBoxRect.w+8, customPTBoxRect.h+8)
      pygame.draw.rect(DISPLAYSURF, BGCOLOR, customPTBoxLineRect)
      pygame.draw.rect(DISPLAYSURF, WHITE, customPTBoxRect)  

      customButtonFont = pygame.font.Font('source/Jalnan.ttf', 30)
      customButtonSurf = customButtonFont.render('OK', True, LINECOLOR)
      customButtonRect = customButtonSurf.get_rect()
      customButtonRect.center = (WINDOWWIDTH/2 + 215, WINDOWHEIGHT - 90)
      customButtonLineRect = pygame.Rect(customButtonRect.x -4, customButtonRect.y-4, customButtonRect.w+8, customButtonRect.h+8)
      pygame.draw.rect(DISPLAYSURF, BGCOLOR, customButtonLineRect)
      pygame.draw.rect(DISPLAYSURF, WHITE, customButtonRect)
      DISPLAYSURF.blit(customButtonSurf, customButtonRect)

      customBackFont = pygame.font.Font('source/Jalnan.ttf', 30)
      customBackSurf = customBackFont.render(' < ', True, LINECOLOR)
      customBackRect = customBackSurf.get_rect()
      customBackRect.center = (WINDOWWIDTH/2 - 215, WINDOWHEIGHT - 90)
      customBackLineRect = pygame.Rect(customBackRect.x -4, customBackRect.y-4, customBackRect.w+8, customBackRect.h+8)
      pygame.draw.rect(DISPLAYSURF, BGCOLOR, customBackLineRect)
      pygame.draw.rect(DISPLAYSURF, WHITE, customBackRect)
      DISPLAYSURF.blit(customBackSurf, customBackRect)


      textType = None

      wText = ""
      hText = ""
      pText = ""

      wNum = 0
      hNum = 0
      pNum = 0

      wColor = BGCOLOR
      hColor = BGCOLOR
      pColor = BGCOLOR

      while(True):
            
            for event in pygame.event.get():
                  if event.type == QUIT:
                        terminate()
                  elif event.type == MOUSEBUTTONUP:

                        if customWTBoxRect.collidepoint((event.pos[0], event.pos[1])): 
                              wColor = LINECOLOR
                              hColor = BGCOLOR
                              pColor = BGCOLOR                              
                              textType = 'W'
                        elif customHTBoxRect.collidepoint((event.pos[0], event.pos[1])): 
                              hColor = LINECOLOR
                              wColor = BGCOLOR
                              pColor = BGCOLOR
                              textType = 'H'                              
                        elif customPTBoxRect.collidepoint((event.pos[0], event.pos[1])):      
                              pColor = LINECOLOR
                              wColor = BGCOLOR
                              hColor = BGCOLOR
                              textType = 'P'
                        elif customButtonRect.collidepoint((event.pos[0], event.pos[1])):    
                              playButtonSound()

                              try :
                                    wNum = int(wText)
                                    hNum = int(hText)
                                    pNum = int(pText)
                              except ValueError :
                                    message = "1~100 사이의 숫자를 입력하세요!"
                                    drawErrorMessage(message)
                              else:
                                    
                                    if wNum < 15 or wNum > 60:
                                          message = "15~60 사이의 가로 숫자를 입력하세요!"
                                          drawErrorMessage(message)
                                    elif hNum < 10 or hNum > 30:
                                          message = "10~30 사이의 세로 숫자를 입력하세요!"
                                          drawErrorMessage(message)
                                    elif pNum < 1:
                                          message = "0보다 큰 지뢰의 숫자를 입력하세요!"
                                          drawErrorMessage(message)
                                    elif pNum >= wNum * hNum:
                                          message = "칸 수보다 적은 지뢰의 숫자를 "
                                          drawErrorMessage(message)
                                    else:
                                          return wNum, hNum, pNum
                        elif customBackRect.collidepoint((event.pos[0], event.pos[1])):
                              playButtonSound()
                              return 0, 0, 0


                  elif event.type == KEYDOWN: 
                        if textType == 'W':
                              if event.key == K_BACKSPACE:
                                    wText = wText[:-1]
                              else:
                                    if len(wText) < 2:
                                          wText += event.unicode
                        elif textType == 'H':
                              if event.key == K_BACKSPACE:
                                    hText = hText[:-1]
                              else:
                                    if len(hText) < 2:
                                          hText += event.unicode
                        elif textType == 'P':
                              if event.key == K_BACKSPACE:
                                    pText = pText[:-1]
                              else:
                                    if len(pText) < 2:
                                          pText += event.unicode

            customWTBoxRect = pygame.Rect(0, 0, 40, 30)
            customWTBoxRect.center = (WINDOWWIDTH/2 - 85, WINDOWHEIGHT - 90)
            customWTBoxLineRect = pygame.Rect(customWTBoxRect.x -4, customWTBoxRect.y-4, customWTBoxRect.w+8, customWTBoxRect.h+8)
            pygame.draw.rect(DISPLAYSURF, wColor, customWTBoxLineRect)
            pygame.draw.rect(DISPLAYSURF, WHITE, customWTBoxRect) 

            customHTBoxRect = pygame.Rect(0, 0, 40, 30)
            customHTBoxRect.center = (WINDOWWIDTH/2 + 25, WINDOWHEIGHT - 90)
            customHTBoxLineRect = pygame.Rect(customHTBoxRect.x -4, customHTBoxRect.y-4, customHTBoxRect.w+8, customHTBoxRect.h+8)
            pygame.draw.rect(DISPLAYSURF, hColor, customHTBoxLineRect)
            pygame.draw.rect(DISPLAYSURF, WHITE, customHTBoxRect) 

            customPTBoxRect = pygame.Rect(0, 0, 40, 30)
            customPTBoxRect.center = (WINDOWWIDTH/2 + 145, WINDOWHEIGHT - 90)
            customPTBoxLineRect = pygame.Rect(customPTBoxRect.x -4, customPTBoxRect.y-4, customPTBoxRect.w+8, customPTBoxRect.h+8)
            pygame.draw.rect(DISPLAYSURF, pColor, customPTBoxLineRect)
            pygame.draw.rect(DISPLAYSURF, WHITE, customPTBoxRect)  

            customWTextSurf = BASICFONT.render( wText, True, LINECOLOR)
            customWTextRect = customWTextSurf.get_rect()
            customWTextRect.center = (WINDOWWIDTH/2 - 85, WINDOWHEIGHT - 90)
            pygame.draw.rect(DISPLAYSURF, WHITE, customWTextRect)
            DISPLAYSURF.blit(customWTextSurf, customWTextRect)  

            customHTextSurf = BASICFONT.render( hText, True, LINECOLOR)
            customHTextRect = customHTextSurf.get_rect()
            customHTextRect.center = (WINDOWWIDTH/2 + 25, WINDOWHEIGHT - 90)
            pygame.draw.rect(DISPLAYSURF, WHITE, customHTextRect)
            DISPLAYSURF.blit(customHTextSurf, customHTextRect) 

            customPTextSurf = BASICFONT.render( pText, True, LINECOLOR)
            customPTextRect = customPTextSurf.get_rect()
            customPTextRect.center = (WINDOWWIDTH/2 + 145, WINDOWHEIGHT - 90)
            pygame.draw.rect(DISPLAYSURF, WHITE, customPTextRect)
            DISPLAYSURF.blit(customPTextSurf, customPTextRect) 

            pygame.display.update()




def showYouWinScreen():

      yeahSound = pygame.mixer.Sound('source/yeah.mp3')
      yeahSound.play()

      happyChocoImg = pygame.image.load('source/happychoco.png')      
      chocoImg_scale = pygame.transform.scale(happyChocoImg, (MONITORHEIGHT-10,MONITORHEIGHT-10))
      chocox = GAMEWINDOWWIDTH/2-(MONITORHEIGHT)/2+5
      chocoy = CELLSIZE+5
      GAMEDISPLAYSURF.blit(chocoImg_scale, (chocox, chocoy)) 

      pygame.display.update()
            
      

def showGameOverScreen(board, cellx, celly):

      pooSound = pygame.mixer.Sound('source/poosound.mp3')
      pooSound.play()

      cryingChocoImg = pygame.image.load('source/cryingchoco.png')      
      chocoImg_scale = pygame.transform.scale(cryingChocoImg, (MONITORHEIGHT-10,MONITORHEIGHT-10))
      chocox = GAMEWINDOWWIDTH/2-(MONITORHEIGHT)/2+5
      chocoy = CELLSIZE+5
      GAMEDISPLAYSURF.blit(chocoImg_scale, (chocox, chocoy)) 

      posx, posy = getPosOfCell(cellx, celly)

      pooSurf = GAMEDISPLAYSURF.convert_alpha()
      pooSurf.fill((0,0,0,0))
      pooRect = pygame.Rect(posx, posy, CELLSIZE, CELLSIZE)
      pygame.draw.rect(pooSurf, TRANSRED, pooRect)


      for cell in board:
            if cell['count'] != POO and cell['flag'] == FLAG:
                  posx, posy = getPosOfCell(cell['x'], cell['y'])
                  pooRect = pygame.Rect(posx, posy, CELLSIZE, CELLSIZE)
                  pygame.draw.rect(pooSurf, TRANSRED, pooRect)                  


      GAMEDISPLAYSURF.blit(pooSurf, (0,0))

      pygame.display.update()


def playButtonSound():
      buttonSound = pygame.mixer.Sound('source/buttonsound.mp3')
      buttonSound.play()
            
            
def terminate():
      pygame.quit()
      sys.exit()

if __name__ == '__main__':
      main()


      