# This is our main drives file. It will be responsible for handling user input and displaying the current GameState

import pygame as p
import ChessEngine
WIDTH = HEIGHT = 512
DIMENSION = 8 #dimensions of a chess board are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15 #for animations
IMAGES = {}


#Initialize a global dictionary of images. This will be called once in the main.
def loadImages():
    pieces = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piece in pieces:
        #using a for loop to make the code more efficient
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))
        #we can access an image by saying 'IMAGES['wp']

#The main driver for the code. This will handle user input and updating the graphics

def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("White"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made
    loadImages() #only do this once, before the while loop
    running = True 
    sqSelected = () #no square is selected, keeps tracks of the last click of the user (tuple: row, column)
    playerClicks = [] #keeps track of player clicks (two tuples: [(row1, column1), (row2, column2)])
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() #(x, y) location of the mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): #the user selected the same square twice
                    sqSelected = () #deselect
                    playerClicks = [] #clear player clicks
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected) #append for both first and second clicks
                if len(playerClicks) == 1 and gs.board[row][col] == "--":
                    sqSelected = ()
                    playerClicks = []
                if len(playerClicks) == 2: #after the 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    for i in range(len(validMoves)):
                        if move == validMoves[i]:
                            gs.makeMove(move)
                            moveMade = True
                            sqSelected = () #resets players clicks
                            playerClicks = []
                    if not moveMade:
                        playerClicks = [sqSelected]
            #key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True
        if moveMade:
            animateMove(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            
        drawGameState(screen, gs, validMoves, sqSelected)
        clock.tick(MAX_FPS)
        p.display.flip()

#highlight the square selected and moves for piece selected
def highlightSquares(screen, gs, validMoves, sqSelected):
    if sqSelected != ():
        r, c = sqSelected
        if gs.board[r][c][0] == ('w' if gs.whiteToMove else 'b'): #sqSelected is a piece that can be moved
            #highlight the selected square
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100) #transparency value -> 0 transparent, 255 opaque
            s.fill(p.Color('blue'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            #highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (SQ_SIZE * move.endCol, SQ_SIZE * move.endRow))

def drawGameState(screen, gs, validMoves, sqSelected):
    drawBoard(screen) #draw squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) #draw pieces on top of the squres

#draw the squares on the board, the top left square is light
def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

#draw the pieces on the board using the current GameState.board
def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--": #not an empty square
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

#animating a move
def animateMove(move, screen, board, clock):
    global colors
    coords = [] #list of cooords that the animation will move through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 10 #frames to move on square
    frameCount = (abs(dR) + abs(dC)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = (move.startRow + dR * frame / frameCount, move.startCol + dC * frame / frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #erase the piece moved from its ending square
        color = colors[(move.endRow + move.endCol) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, move.endRow * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        #draw captured piece onto rectangle
        if move.pieceCaptured != '--':
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        #draw moving piece
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
