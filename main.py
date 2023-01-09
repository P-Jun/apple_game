from apple import *
import time
import pyautogui as pg
mx = 0
cnt = 0

def click_play():
    pg.click(x=1332, y=362, button="left")

def click_restart():
    pg.click(x=1492, y=405, button="left")

click_play()
time.sleep(1)
while True:
    cnt+=1
    board = init_board()
    #print_board(board)
    tmp = greedy_search(board)
    time.sleep(100)
    
    if tmp > mx:
        mx = tmp
        pg.screenshot(
            f'C:/Users/SOGANG/Desktop/apple_game/score_imgs/{mx}.png')

    click_restart()    
    click_play()

    print(f'\r{cnt} round : max score : {mx}')
    time.sleep(1)