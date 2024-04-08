# 상 좌 하 우 팩맨 우선순위 이동
dx = [-1, 0, 1, 0]
dy = [0, -1, 0, 1]

ddx = [-1, -1, 0, 1, 1, 1, 0, -1]
ddy = [0, -1, -1, -1, 0, 1, 1, 1]

m, t = map(int, input().split())

dead_monster = [[0]*4 for _ in range(4)]

# 현재 그래프에 있는 몬스터 수
now_graph = [[0]*4 for _ in range(4)]

monster = []
eggmonster = []

# 팩맨 초기 좌표 r, c
r, c = map(int ,input().split())
packman = [r-1, c-1]

#몬스터 위치 및 방향 정보
for _ in range(m) :
    a, b, d = map(int, input().split())
    monster.append([a-1, b-1, d-1])
    now_graph[a-1][b-1] +=1

def duplicate() :

    num = len(monster)
    for i in range(num) :
        eggmonster.append(monster[i])

def update_monster(x, y, x2, y2, d, idx) :
    #현재 위치 감소
    now_graph[x][y] -=1
    monster[idx] = [x2, y2, d]
    now_graph[x2][y2] +=1


def monstermove() :

    num = len(monster)
    for i in range(num) :
        x, y, d = monster[i]

        # 자신 방향 대로 움직일 수 있는 경우
        mx = x + ddx[d]
        my = y + ddy[d]

        if 0 <= mx < 4 and 0 <= my < 4 and dead_monster[mx][my] == 0 and (mx != packman[0] or my != packman[1]) :
            update_monster(x, y, mx, my ,d, i)

        else :
            for l in range(1, 8) :
                md = (d+l)%8

                mx = x +ddx[md]
                my = y +ddy[md]

                if 0 <= mx < 4 and 0 <= my < 4 and dead_monster[mx][my] == 0 and (mx !=packman[0] or my != packman[1]) :
                    update_monster(x, y, mx, my, md, i)
                    break


def packmove(count,x, y, path) :
    global caneat
    global resultpath

    # 초기화
    if count == 0 :
        caneat = -1
        resultpath = []

    if count == 3 :
        temp = []
        point = 0
        for mx, my in path :
            if [mx, my] not in temp :
                temp.append([mx, my])
                point +=now_graph[mx][my]

        if caneat < point :
            caneat = point
            resultpath = path

    else :
        for i in range(4) :
            mx = x + dx[i]
            my = y + dy[i]
            if 0 <= mx < 4 and 0 <= my < 4 :
                packmove(count +1, mx, my, path+[[mx, my]])

def dead_monster_count() :
    for i in range(4) :
        for j in range(4) :
            if dead_monster[i][j] >= 1 :
                dead_monster[i][j] -=1

def egg_to_baby() :

    while eggmonster :
        a, b, c = eggmonster.pop()
        monster.append([a, b, c])
        now_graph[a][b] +=1


caneat = -1
resultpath = []

while t > 0 :
    duplicate()
    monstermove()
    packmove(0, packman[0], packman[1], [])
    dead_monster_count()


    temp_monsters = []
    for monst in monster :
        x, y, d = monst
        if [x, y] in resultpath :
            continue
        else :
            temp_monsters.append(monst)

    monster = temp_monsters

    for i in range(len(resultpath)) :
        a, b = resultpath[i]
        if now_graph[a][b] > 0 :
            now_graph[a][b] = 0
            dead_monster[a][b] = 2

        if i == len(resultpath) -1 :
            packman = [a, b]

    egg_to_baby()

    t -=1

print(len(monster))