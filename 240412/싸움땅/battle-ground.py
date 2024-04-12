N, M, K = map(int, input().split())

graph = [
    [[]for _ in range(N)] for _ in range(N)
]

player = []

player_graph = [[-1]*N for _ in range(N)]

player_score = [0] * M

# d에 따른 방향 값
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

for idx in range(N) :
    guns = list(map(int, input().split()))
    for i in range(N) :
        # 총이 없는 경우 패스
        if guns[i] != 0 :
            graph[idx][i].append(guns[i])

for idx in range(M) :
    # 초기 좌표, 방향, 기본 스텟
    x, y, d, s = map(int, input().split())
    # 플레이어 위치, 방향, 기초스텟, 가지고있는 총 공격력, 플레이어 번호
    player.append([x-1, y-1, d, s, 0])


def player_update() :
    for idx, play in enumerate(player) :
        x, y, _, _, _ = play
        player_graph[x][y] = idx

def lose(num) :

    x, y, d, s, g = player[num]
    drop_gun(x, y, g)

    mx, my = x +dx[d], y +dy[d]

    # 움직이려는 위치가 구역내고 총든사람이 없어야한다
    if 0 <= mx < N and 0 <= my < N and player_graph[mx][my] == -1 :
        player_graph[x][y] = -1
        player_graph[mx][my] = num
        power = get_gun(mx, my)
        player[num] = [mx, my, d, s, power]
        return

    else :
        for i in range(3) :
            d = (d+1)%4

            mx, my = x + dx[d], y + dy[d]

            # 움직일수 있는 위치 찾았으면 이동과 업데이트 후 종료
            if 0 <= mx < N and 0 <= my < N and player_graph[mx][my] == -1:
                player_graph[x][y] = -1
                player_graph[mx][my] = num
                power = get_gun(mx, my)
                player[num] = [mx, my, d, s, power]
                return

def win(num, point) :
    player_score[num] +=point

    x, y, d, s, g = player[num]
    drop_gun(x, y, g)
    power  = get_gun(x, y)
    player[num] = [x, y, d, s, power]
    player_graph[x][y] = num

def fight(num1, num2) :

    x, y, d, s, g = player[num1]
    x2, y2, d2, s2, g2 = player[num2]

    point = abs((s+g)-(s2+g2))

    # 기초스텟과 총 공격력 합
    if s+g > s2 +g2 :
        # 진사람이 떨어진 총을 주울 경우도 있기 때문에 이긴사람 나중에 처리
        lose(num2)
        win(num1, point)
    # 같은 경우 기초스텟 높은사람 승리
    elif s+g == s2+g2 :
        if s > s2 :
            lose(num2)
            win(num1, point)
        else :
            lose(num1)
            win(num2, point)
    else :
        lose(num1)
        win(num2, point)

def get_gun(gx, gy) :
    global graph
    if graph[gx][gy] :
        # 총 정렬
        graph[gx][gy].sort()
        power = graph[gx][gy].pop()

        return power
    # 해당 위치 총 없는 경우
    else :
        return 0


def drop_gun(gx, gy, power) :
    # 총이 있는 상태면 떨어트리기 -> 0 은 총없는 것
    if power != 0 :
        graph[gx][gy].append(power)

def all_player_move() :

    for idx, play in enumerate(player) :
        # 위치, 방향, 기초, 총,번호
        x, y, d, s, g = play

        mx = x + dx[d]
        my = y + dy[d]

        if 0 <= mx < N and 0 <= my < N :
            # 만약 해당 위치에 플레이어가 존재 한다면
            if player_graph[mx][my] != - 1 and idx != player_graph[mx][my] :
                player_graph[x][y] = -1
                player[idx] = [mx, my, d, s, g]
                fight(idx, player_graph[mx][my])
            # 존재하지 않으면 편하게 이동
            else :
                player_graph[x][y] = -1
                player_graph[mx][my] = idx
                # 현재 총버리기
                drop_gun(mx, my, g)
                # 가장 좋은 총 줍기
                power = get_gun(mx, my)
                #플레이어 정보 업데이트
                player[idx] = [mx, my, d, s, power]

        # 격자안 아니면 방향 반대로 이동
        else :
            d = (d+2)%4

            mx = x + dx[d]
            my = y + dy[d]

            if player_graph[mx][my] != -1 and idx != player_graph[mx][my]:
                fight(idx, graph[mx][my])

            else :
                player_graph[x][y] = -1
                player_graph[mx][my] = idx
                drop_gun(mx, my, g)
                power = get_gun(mx, my)
                # 플레이어 정보 업데이트
                player[idx] = [mx, my, d, s, power]


time = 0
player_update()
while time < K :
    all_player_move()


    time +=1

for score in player_score :
    print(score, end = " ")