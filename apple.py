import pyautogui as pg

#init list by capture
def init_board():
    location_dict = {}
    im = pg.screenshot()

    for i in range(1, 10):
        locations = pg.locateAll(f"apple_imgs/{i}.png", im)
        for item in locations:
            location_dict[item] = i
    #17*10개의 사과를 찾아야 함
    assert len(location_dict) == 170, "Plz Check Game Screen"

    #높이 정렬
    locations = sorted(location_dict.items(), key=lambda x: x[0].top)
    board = [] # [position, number]
    for i in range(10):
        #한 줄 추가, x 좌표로 정렬
        board.append(locations[i*17:i*17+17])
        board[-1] = sorted(board[-1])

    for (x, i) in enumerate(board):
        for (y, j) in enumerate(i):
            board[x][y] = [j[0], j[1]]

    return board

#print game_board
def print_board(board):
    print("-"*33)
    for line in board:
        for obj in line:
            print(obj[1], end=" ")
        print()
    print("-"*33)

#remove apple box_st to box_ed
def drag_apple(box_st, box_ed):
    drag_st_box = box_st[0]
    drag_end_box = box_ed[0]

    pg.moveTo(drag_st_box.left, drag_st_box.top)
    pg.moveTo(drag_st_box.left - 3, drag_st_box.top - 3, 0.1)
    pg.mouseDown()
    pg.moveTo(drag_end_box.left + 17, drag_end_box.top + 17)
    pg.moveTo(drag_end_box.left + 20, drag_end_box.top + 20, 0.1)
    pg.mouseUp()

#set apple score to zero
def remove_apple(board, st, ed):
    for x in range(st[0],ed[0]+1):
        for y in range(st[1], ed[1]+1):
            board[x][y][1]=0

#find action list of now board
#return : [((xs, ys), (xe,ye), cnt), .... ]
def find_action(board):
    ret = []
    tmp_ret = set()
    pos = [(x, y) for x in range(10) for y in range(17)]
    for (xs, ys) in pos:
        for xe in range(xs, 10):
            for ye in range(ys, 17):
                search_sum = 0
                cnt = 0
                ty = 0
                #최적화 하자
                for x in range(xs, xe + 1):
                    for y in range(ys, ye + 1):
                        apple_num = board[x][y][1]
                        if apple_num != 0:
                            cnt+=1
                            search_sum += apple_num
                            if search_sum > 10:
                                break
                        ty = y

                    if search_sum > 10:
                        break
                    if search_sum == 10:
                        if x == xe and ty == ye:
                            tmp_ret.add(100000000*xs+1000000*ys+10000*xe+100*ye+cnt)
                        break
    for cache in tmp_ret:
        xs = cache//100000000
        ys = cache//1000000%100
        xe = cache//10000%100
        ye = cache//100%100
        cnt = cache%100
        ret.append(((xs, ys), (xe,ye), cnt))
    return ret

#play game board with greedy method
def greedy_search(board):
    score = 0
    while(1):
        actions = find_action(board)
        if len(actions) == 0:
            break
        action = actions[0]
        st, ed = action[0], action[1]
        box_s, box_e = board[st[0]][st[1]], board[ed[0]][ed[1]]
        score += action[2]

        drag_apple(box_s, box_e)
        remove_apple(board, st, ed)
        #print_board(board)
        #print(f"\rSolved: {score}/170", end="              ")
    return score