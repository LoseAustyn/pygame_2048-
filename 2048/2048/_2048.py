
import pygame
import random
import sys
from functools import reduce
from collections import Iterable

#   初始化pygame
pygame.init()   



"""
画面
"""
#   方块大小
BlockSize = 100

#   方块间隔
BlockGap = 13

#   背景颜色
BgColor = '#92877d'

#   方块颜色
#   数字：['方块的背景颜色','方块内的数字颜色']
def get_num_color(num):
    BlockColor = {
        2: ['#eee4da', '#776e65'],
        4: ['#ede0c8', '#776e65'],
        8: ['#f2b179', '#f9f6f2'],
        16: ['#f59563', '#f9f6f2'],
        32: ['#f67c5f', '#f9f6f2'],
        64: ['#f65e3b', '#f9f6f2'],
        128: ['#edcf72', '#f9f6f2'], 
        256: ['#edcc61', '#f9f6f2'],
        512: ['#edc850', '#f9f6f2'],
        1024: ['#edc53f', '#f9f6f2'], 
        2048: ['#edc22e', '#f9f6f2'],
        4096: ['#eee4da', '#776e65'],
        }
    return BlockColor[num]


#   显示游戏布局
def draw_GameTable(screen):
    for i in range(4):
        for j in range(4):
            x = BlockGap * (j + 1) + BlockSize * j
            y = BlockGap * (i + 1) + BlockSize * i
            pygame.draw.rect(screen, pygame.Color('#f9f6f2'), (x, y, BlockSize, BlockSize))

#   显示方块上的数字
def draw_Nums(screen, TempTable):
    #   准备字体等
    FontSize = BlockSize - 50
    Font = pygame.font.SysFont("Arial", FontSize)
    #   遍历数字
    for i, line in enumerate(TempTable):
        for j, num in enumerate(line):
            if num != 0:
                #   计算显示位置（x坐标、y坐标）
                x = BlockGap * (j + 1) + BlockSize * j
                y = BlockGap * (i + 1) + BlockSize * i
                #   获取颜色
                FontColor = pygame.Color(get_num_color(num)[1])
                #   显示数字
                Text = Font.render(str(num), True, FontColor)
                #   get_rect()是一个处理矩形图像的方法，返回值包含矩形的居中属性
                TextRect = Text.get_rect()
                #   显示的位置
                TextRect.centerx, TextRect.centery = x + BlockSize / 2, y + BlockSize / 2
                #   用对应的数字背景色，重新绘制这个方块
                pygame.draw.rect(screen, pygame.Color(get_num_color(num)[0]), (x, y, BlockSize,BlockSize))
                screen.blit(Text, TextRect)


#   游戏结束画面
def game_over(screen):
    #   big字号大小
    font_size_big = 60
    #   small字号大小
    font_size_small = 25
    #   字体颜色
    font_color = (255, 255, 255)
    #   选择字体
    font_big = pygame.font.SysFont("Arial", font_size_big)
    font_small = pygame.font.SysFont("Arial", font_size_small)
    #   onvert_alpha相对于convert，保留了图像的Alpha 通道信息，即保留图片的透明部分
    surface = screen.convert_alpha()
    #   游戏结束背景画面颜色填充
    surface.fill((238,228,218,2))
    #   gameover
    text = font_big.render('Game Over!', True, '#776e65')
    text_rect = text.get_rect()
    text_rect.centerx, text_rect.centery = width / 2, height / 2 - 50
    #   在游戏结束的画面上显示gameover
    surface.blit(text, text_rect)
    #   按钮设置
    button_width, button_height = 100, 40
    button_start_x_left = width / 2 - button_width - 20
    button_start_x_right = width / 2 + 20
    button_start_y = height / 2 - button_height / 2 + 20
    #   按钮背景绘制
    pygame.draw.rect(surface, '#776e65', (button_start_x_right, button_start_y, button_width, button_height))
    #   退出按钮
    text_quit = font_small.render('Quit', True, font_color)
    text_quit_rect = text_quit.get_rect()
    text_quit_rect.centerx, text_quit_rect.centery = button_start_x_right + button_width / 2, button_start_y + button_height / 2
    #   按钮内字的绘制
    surface.blit(text_quit, text_quit_rect)
    #    设置时钟对结束画面进行帧控制，节省资源使用
    clock = pygame.time.Clock()
    while True:
        screen.blit(surface, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False        
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button:
                if text_quit_rect.collidepoint(pygame.mouse.get_pos()):
                    return False     
        pygame.display.update()
        clock.tick(60)


"""
游戏逻辑设计
"""
#   判断

##  是否gameover?
def judge_if_game_over(field):
    #    如果所有的判断函数都为0，就返回not 0，即非0
    return not any([judge_move_left(field),
                   judge_move_right(field),
                   judge_move_up(field),
                   judge_move_down(field)])

##  能否移动
def judge_move_up(TempTable):
    #   将游戏布局行列交换，从而将能否向上的判断变成能否向左的判断
    TempTable = [list(row) for row in zip(*TempTable)]
    return judge_move_left(TempTable)

def judge_move_down(TempTable):
    #   将游戏布局行列交换，从而将能否向上的判断变成能否向右的判断
    TempTable = [list(row) for row in zip(*TempTable)]
    return judge_move_right(TempTable)

def judge_move_left(TempTable):
    #   只要游戏布局的任意一行可以向左移动， 就返回True
    for row in TempTable:
        for i in range(3):
            #   如果判断的左边的数为0，右边的数不为0，则说明可以向左移动
            if row[i] == 0 and row[i + 1] != 0:
                return True
            elif row[i] != 0 and row[i + 1] == row[i]:
            #   如果判断的左边的数不为0，且左右2个数相等，则说明可以向左移动
                return True
    return False

def judge_move_right(TempTable):
    #   对游戏布局的每一行元素进行镜像反转，从而将能否向右的判断变成能否向左的判断
    return judge_move_left([row[::-1] for row in TempTable])


#   移动实现
def move_up(TempTable):
    #   行列转换
    TempTable = [list(row) for row in zip(*TempTable)]
    #   向左
    TempTable = move_left(TempTable)
    #   再次行列转换复原
    return [list(row) for row in zip(*TempTable)]

def move_down(TempTable):
    #   行列转换
    TempTable = [list(row) for row in zip(*TempTable)]
    #   向右移动
    TempTable = move_right(TempTable)
    #   再次行列转换复原
    return [list(row) for row in zip(*TempTable)]

def move_left(TempTable):
    for i, row in enumerate(TempTable):
        #   1.用sorted排序把这一行的非0数字向前放，把0向后放。例如之前是[0, 2, 2, 2]-->[2, 2, 2, 0]
        row = sorted(row, key=lambda x: 1 if x == 0 else 0)
        #   2.依次循环判断两个数是否相等，如果相等 第一个*2 第二个数变成0。例如[2, 2, 2, 0]-->[4, 0, 2, 0]
        for index in range(3):
            if row[index] == row[index + 1]:
                row[index] *= 2
                row[index + 1] = 0
        #   3.移除空隙，即非0靠左，0靠右。例如[4, 0, 2, 0]-->[4, 2, 0, 0]
        row = sorted(row, key=lambda x: 1 if x == 0 else 0)
        #   4.  更新数字列表，因为这一行已经是操作之后的了
        TempTable[i] = row
    return TempTable

def move_right(TempTable):
    #   对游戏布局的每一行元素进行镜像反转
    TempTable = [row[::-1] for row in TempTable]
    #   再向左移动
    move_left(TempTable)
    #   再一次对游戏布局的每一行元素进行镜像反转
    return [row[::-1] for row in TempTable]


#   移动
def move(TempTable,direction):
    #   用字典存储判断各个方向是否可移动对应的函数
    judge_move_func_dict = {
        'left': judge_move_left,
        'right': judge_move_right,
        'up': judge_move_up,
        'down': judge_move_down
        }
    #   用字典存储各个方向移动的函数
    move_func_dict = {
        'left': move_left,
        'right': move_right,
        'up': move_up,
        'down': move_down
        }
    #   调用对应的函数，判断是否可以朝这个方向移动
    result = judge_move_func_dict[direction](TempTable)
    #   用于在后台查看玩家操作是否被游戏响应
    print("%s方向是否可以移动：" % direction, result)
    #   如果可以移动
    if result:
        #   进行移动
        TempTable = move_func_dict[direction](TempTable)
        #   调用随机函数在空位生成新的随机数
        random_num(TempTable)
    #   将新的布局返回
    return TempTable



#   随机数生成，生成在任意位置, 需要表格布局参数
def random_num(TempTable):

    #   找到空位，并用list记录起来
    positions = list()
    for row,line in enumerate(TempTable):
        for col,num in enumerate(line):
            if num == 0:
                positions.append((row,col))

    #   随机挑选一个空位
    row,line = random.choice(positions)
    #   从2和4中随机一个塞进去，2为4的2倍出现概率
    TempTable[row][line] = random.choice([2,2,4])



#   计算当前游戏得分数
def get_Score(TempTable):
    def sum_all(x, y):
        if isinstance(x, Iterable):
           return sum(x) + sum(y)
        return x + sum(y)
    return reduce(sum_all, TempTable)

#   显示分数
def draw_Score(screen, score):
    font_size_big = 40
    font_color = '#f9f6f2'
    font_big = pygame.font.SysFont("Arial", font_size_big)
    score = font_big.render(str(score), True, font_color)
    score2 = font_big.render('Score:', True, font_color)
    screen.blit(score2, (490, 15))
    screen.blit(score, (490, 65))



"""
主程序
"""
def runningGame(Screen):
    #   设置时钟固定帧率，减少资源使用
    clock = pygame.time.Clock()

    #   设置4x4的游戏表格布局，并用于记录每个位置上的数字，默认为0
    GameTable = [[0 for _ in range(4)]for _ in range(4)]
    #   随机生成两个数字
    for _ in range(2):
        random_num(GameTable)
    #   记录分数
    score = get_Score(GameTable)


    while True:

        #   游戏事件检测
        for event in pygame.event.get():
            #   点击窗口右上角×从而结束游戏
            if event.type == pygame.QUIT:
                return False

            #   按键事件检测
            if event.type == pygame.KEYDOWN:
                #   检测方向按键
                if event.key in [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]:
                    #   按键方向记录
                    direstion = {pygame.K_UP: 'up',
                                 pygame.K_DOWN: 'down',
                                 pygame.K_LEFT: 'left',
                                 pygame.K_RIGHT: 'right'}[event.key]
                    #   用于在后台查看玩家操作是否被游戏响应
                    print("玩家按下：",direstion)
                    #   进行移动（同时检测移动）
                    GameTable = move(GameTable,direstion)
                    #   每一次移动后对局面进行检测，看是否gameover
                    if judge_if_game_over(GameTable):
                        print("游戏结束")
                        return
                    #   在进行一次按键操作后计算分数
                    score = get_Score(GameTable)
        
        #   显示背景
        screen.fill(BgColor)
        #   显示游戏布局
        draw_GameTable(screen)
        #   显示数字
        draw_Nums(screen,GameTable)
        #   显示分数
        draw_Score(screen, score)
        #   刷新窗口
        pygame.display.update()
        #   FPS（每秒钟画面帧数）
        clock.tick(60)



"""
显示
"""
#   设置窗口大小
size = width,height = 640,480
#   加载窗口
screen = pygame.display.set_mode(size)   


"""
运行游戏
"""
running = True
#   设置游戏启动状态
while running:
    #   运行一次游戏
    running = runningGame(screen)
    #   游戏结束
    game_over(screen)

