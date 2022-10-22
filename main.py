import pygame

#Initializing screen objects
SIZE = 600
sqnum = 50
border = SIZE / (12 * sqnum)
sqlen = (SIZE + border) / sqnum

pygame.init()
screen = pygame.display.set_mode((SIZE , SIZE))
pygame.display.set_caption('path finder')

ad = pygame.Rect(-1, -1, sqlen, sqlen)
running = True
rightclick = 'start'

drawn = list()
empty = list()
grid = list()
checked = list()
recntlychecked = list()

for x in range(sqnum):
    for y in range(sqnum):
        square = pygame.Rect((x*sqlen, y*sqlen) , (sqlen - border , sqlen - border))
        drawn.append(square)

for x in range(sqnum):
    grid.append([])
    for y in range(sqnum):
        grid[x].append(0)
        square = pygame.Rect((x*sqlen, y*sqlen) , (sqlen - border , sqlen - border))
        grid[x][y] = [square, 0]

start = drawn[0]
end = drawn[sqnum ** 2 - 1]
clicked = False
paths = list()

#-----------------------------------------------------------------------------------------------------------------------

#MAIN LOOP
while running:
    calculate = False
    screen.fill((0, 0, 0))
    for sq in drawn:
        if sq not in checked:
            pygame.draw.rect(screen, (0, 250, 0), sq)
    for sq in checked:
        pygame.draw.rect(screen, (0, 150, 0), sq)
    for path in paths:
        if end in path:
            for sq in path:
                pygame.draw.rect(screen, (100, 0, 0), sq)
    pygame.draw.rect(screen, (0 , 50 , 0), start)
    pygame.draw.rect(screen, (0 , 50 , 0), end)
    pygame.display.update()

    #Waiting For events
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
            break
        if e.type == pygame.MOUSEBUTTONDOWN:
            pos_x, pos_y = pygame.mouse.get_pos()
            if e.button == 1:
                for row in grid:
                    for sq in row:
                        sq[1] = 0
                clicked = True
                checked = list()
                paths = list()
                for sq in empty:
                    if pos_x in range(sq.left, sq.right) and pos_y in range(sq.top, sq.bottom):
                        clicked = False
                        empty.remove(sq)
                        drawn.append(sq)
            if e.button == 3:
                if rightclick == 'start':
                    for sq in drawn:
                        if pos_x in range(sq.left, sq.right) and pos_y in range(sq.top, sq.bottom):
                            start = sq
                            for row in grid:
                                for sq in row:
                                    sq[1] = 0
                            rightclick = 'end'
                            checked = list()
                            paths = list()
                elif rightclick == 'end':
                    for sq in drawn:
                        if pos_x in range(sq.left, sq.right) and pos_y in range(sq.top, sq.bottom):
                            end = sq
                            for row in grid:
                                for sq in row:
                                    sq[1] = 0
                            rightclick = 'start'
                            checked = list()
                            paths = list()
        if e.type == pygame.MOUSEBUTTONUP:
            if e.button == 1:
                clicked = False
        if e.type == pygame.KEYDOWN:
            calculate = True

    if clicked:
        pos_x, pos_y = pygame.mouse.get_pos()
        for sq in drawn:
            if pos_x in range(sq.left, sq.right) and pos_y in range(sq.top, sq.bottom) and sq != start and sq != end:
                drawn.remove(sq)
                empty.append(sq)

#path finding algorithm
    if calculate:
        pathlen = 0
        for row in grid:
            for sq in row:
                if sq[0] == start:
                    for x, y in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
                        if grid.index(row) + x in range(len(grid)) and row.index(sq) + y in range(len(grid)):
                            if (grid[grid.index(row) + x] in grid or grid[grid.index(row) + x][
                                row.index(sq) + y] in row):
                                ad = grid[grid.index(row) + x][row.index(sq) + y][0]
                                if grid[grid.index(row) + x][row.index(sq) + y][0] in drawn \
                                        and not grid[grid.index(row) + x][row.index(sq) + y][1]:
                                    grid[grid.index(row) + x][row.index(sq) + y][1] = 1
                                    checked.append(ad)
                                    recntlychecked.append(ad)
                    sq[1] = 1
                    break
        for sq in checked:
            pygame.draw.rect(screen, (0, 150, 0), sq)
        pygame.display.update()
        ad = pygame.Rect(-1, -1, sqlen, sqlen)
        oldchecked = list()
        oldrecentlychecked = list()
        for s in checked:
            paths.append([s])
        while ad != end and checked != oldchecked:
            pathlen += 1
            oldrecentlychecked = recntlychecked[:]
            recntlychecked = list()
            oldchecked = checked[:]
            for adj in oldrecentlychecked:
                for row in grid:
                    if [adj, 1] in row:
                        for x, y in [(-1, 0), (0, -1), (1,0), (0,1)]:
                            if grid.index(row) + x in range(len(grid)) and row.index([adj, 1]) + y in range(len(row)):
                                ad = grid[grid.index(row) + x][row.index([adj, 1]) + y][0]
                                if grid[grid.index(row) + x][row.index([adj, 1]) + y][0] in drawn \
                                        and not grid[grid.index(row) + x][row.index([adj, 1]) + y][1]:
                                    checked.append(ad)
                                    recntlychecked.append(ad)
                                    grid[grid.index(row) + x][row.index([adj, 1]) + y][1] = 1
                                    for path in paths:
                                        if adj in path and ad not in path:
                                            if len(path) <= pathlen:
                                                path.append(ad)
                                            else:
                                                paths.append(path[:len(path)-1] + [ad])
                                            break
                                if ad == end: break
                        if ad == end: break
                if ad == end:
                    checked = oldchecked[:]
                    break
            for sq in checked:
                pygame.draw.rect(screen, (0, 150, 0), sq)
            pygame.display.update()
        for path in paths:
            if end in path:
                for sq in path:
                    pygame.draw.rect(screen, (100, 0, 0), sq)
                    pygame.display.update()

