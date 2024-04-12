# 꼬리잡기놀이

from collections import deque

N, M, K = map(int, input().split())

graph =[]

# team 의 머리 저장하는 부분
team = []

team_graph = [[-1]*N for _ in range(N)]

# 오른쪽 위 왼쪽 아래
dx = [0, -1, 0, 1]
dy = [1, 0, -1, 0]

for _ in range(N) :
    graph.append(list(map(int, input().split())))

for i in range(N) :
    for j in range(N) :
        if graph[i][j] == 1 :
            team.append([i, j])

def tail_change(x, y, x2, y2, idx) :
    print(graph)
    graph[x][y], graph[x2][y2] = 3, 1
    team[idx] = [x2, y2]
    print(graph)

def get_score_and_find_head_tail(x,y) :
    global score
    # 헤드좌표, 꼬리좌표, 해당 팀번호
    hx, hy, tx, ty, idx = -1, -1, -1, -1, -1

    visited =[[False]*N for _ in range(N)]
    q = deque()
    q.append([x, y, 1])
    visited[x][y] = True

    while q :
        nx, ny, nd = q.popleft()
        # 머리면 잡은애로부터 몇번쨰의 번호에 따라 점수 흑득
        if graph[nx][ny] == 1 :
            hx, hy = nx, ny
            score += nd**2
        elif graph[nx][ny] == 3 :
            tx, ty = nx, ny

        for k in range(4) :
            mx = nx +dx[k]
            my = ny +dy[k]
            if 0 <= mx < N and 0 <= my < N and graph[mx][my] !=0 and visited[mx][my] == False :
                # 꼬리에서 머리로 바로 못넘어가도록
                if graph[nx][ny] == 3 and graph[mx][my] == 1 :
                    continue
                visited[mx][my] = True
                q.append([mx, my, nd+1])

    for num, h in enumerate(team) :
        if hx == h[0] and hy == h[1] :
            idx = num
            break

    return [hx, hy, tx, ty, idx]

def left_to_right_shot(t) :
    #
    for i in range(N) :
        if graph[t][i] != 0 and graph[t][i] != 4:
            hx, hy, tx, ty, idx = get_score_and_find_head_tail(t, i)
            tail_change(hx, hy, tx, ty, idx)
            break

def down_to_up_shot(t) :
    for i in range(t) :
        if graph[N-1+i][t] != 0 and graph[N-1+i][t] != 4:
            hx, hy, tx, ty, idx = get_score_and_find_head_tail(N-1+i, t)
            tail_change(hx, hy, tx, ty, idx)
            break

def right_to_left_shot(t) :
    for i in range(t) :
        if graph[N-1-t][N-i-1] != 0 and graph[N-1-t][N-i-1] != 4:
            hx, hy, tx, ty, idx = get_score_and_find_head_tail(N-1-t, N-i-1)
            tail_change(hx, hy, tx, ty, idx)
            break
def up_to_down_shot(t) :
    for i in range(t) :
        if graph[i][N-1-t] != 0 and graph[N-1-t][N-i-1] != 4:
            hx, hy, tx, ty, idx = get_score_and_find_head_tail(i, N-1-t)
            tail_change(hx, hy, tx, ty, idx)
            break

def shot(t) :
    t = (t)%(4*N)

    if 0<= t < N :
        left_to_right_shot(t)
    elif N <= t < 2*N :
        down_to_up_shot(t-N)
    elif 2*N <= t < 3*N :
        right_to_left_shot(t-2*N)
    else :
        up_to_down_shot(t-3*N)


def team_move(x, y, num) :

    q = deque()

    visited = [[False]*N for _ in range(N)]
    # head는 값이 1임으로
    q.append([x, y, 1])

    check = False

    for i in range(4) :

        mx = x + dx[i]
        my = y + dy[i]

        if 0 <= mx < N and 0 <= my < N and graph[mx][my] !=0 :
            if graph[mx][my] == 3 :
                q.pop()
                check = True
                q.append([mx, my, 3])
                visited[x][y] = True
                graph[mx][my] = 1
                graph[x][y] = 2

    if check == True :
        nx, ny, nv = q.popleft()

        for i in range(4) :
            mx = nx + dx[i]
            my = ny + dy[i]

            if 0 <= mx < N and 0 <= my < N and graph[mx][my] != 0 and visited[mx][my] == False :
                graph[mx][my] = 3
                return
    if check == False :
        while q :
            nx, ny, nv = q.popleft()
            for i in range(4) :
                mx = nx + dx[i]
                my = ny + dy[i]

                if 0 <= mx < N and 0 <= my < N and graph[mx][my] != 0 and visited[mx][my] == False :

                    # 비어있는 칸이면
                    if graph[mx][my] == 4 :
                        # 현재 캐릭이 가진 값으로 이동
                        graph[mx][my] = nv
                        # 방문 처리
                        visited[mx][my] = True

                    # 뒤이어 나오는 친구들이면
                    elif graph[mx][my] == 2 :
                        q.append([mx, my, 2])
                        graph[nx][ny] = 4
                    # 꼬리인 경우
                    elif graph[mx][my] == 3 :
                        graph[nx][ny] = 3
                        graph[mx][my] = 4
                        visited[mx][my] = True

def all_team_move():
    for idx, head in enumerate(team) :
        hx, hy = head
        team_move(hx, hy, idx)


time = 0
score = 0
while time < K :
    all_team_move()
    shot(time)
    time +=1

print(score)