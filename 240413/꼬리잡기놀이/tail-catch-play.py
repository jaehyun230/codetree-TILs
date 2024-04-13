from collections import deque
N, M, K = map(int, input().split())

graph = []

team = []

# 팀안에 좌표들 모임 순서대로
team_path = []

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

for _ in range(N) :
    graph.append(list(map(int, input().split())))

count = 0
for i in range(N) :
    for j in range(N) :
        # head인 경우
        if graph[i][j] == 1 :
            team.append([i, j, count])
            count +=1


def change_head_tail(num) :

    for idx, path in enumerate(team_path) :
        if idx == num :

            temp = path[::-1]

            hx, hy = temp[0][0], temp[0][1]

            tx, ty = temp[-1][0], temp[-1][1]
            graph[hx][hy] = 1
            graph[tx][ty] = 3
            team_path[num] = temp
            break

def catch(x, y) :
    global answer

    for idx, path in enumerate(team_path) :
        for i in range(len(path)) :
            if path[i][0] == x and path[i][1] == y :
                answer +=(i+1)**2
                # 잡은 위치의 머리와 꼬리를 바꿔야함
                change_head_tail(idx)

                break

def shot_left(t) :
    for i in range(N) :
        if graph[t][i] != 0 and graph[t][i] != 4 :
            catch(t, i)
            break

def shot_down(t) :
    for i in range(N-1, -1, -1) :
        if graph[i][t] != 0 and graph[i][t] != 4 :
            catch(i, t)
            break

def shot_right(t) :
    for i in range(N-1, -1, -1) :
        if graph[N-1-t][i] != 0 and graph[N-1-t][i] != 4 :
            catch(N-1-t, i)
            break
def shot_up(t) :
    for i in range(N) :
        if graph[i][N-1-t] != 0 and graph[i][N-1-t] != 4 :
            catch(i, N-1-t)
            break

def shot_ball(t) :
    t = t%(4*N)
    if 0 <= t < N :
        shot_left(t)
    elif N <= t < N*2 :
        shot_down(t-N)
    elif 2*N <= t < N*3 :
        shot_right(t-2*N)
    elif 3*N <= t < N*4 :
        shot_up(t-3*N)

def find_team_path(idx) :
    sx, sy, num = team[idx]
    q = deque()

    visited = [[False]*N for _ in range(N)]
    # 시작 헤드 값 확인
    q.append([sx, sy, 1])
    visited[sx][sy] = True
    path = []

    while q :
        nx, ny, value = q.popleft()
        path.append([nx, ny])
        for i in range(4) :
            mx = nx + dx[i]
            my = ny + dy[i]

            if 0 <= mx < N and 0 <= my < N and graph[mx][my] != 0  and graph[mx][my] != 4 and visited[mx][my] == False :
                # 머리에서 바로 꼬리로는 못가게 하도록
                if graph[mx][my] == 3 and value == 1 :
                    continue
                visited[mx][my] = True
                q.append([mx, my, graph[mx][my]])

    team_path.append(path)


def all_team_move() :

    for idx, path in enumerate(team_path) :


        result_move = []
        check = False
        temp_pos = [-1, -1]
        # 꼬리와 머리가 안이어져있는지 체크
        for i in range(4) :
            mx = path[0][0] + dx[i]
            my = path[0][1] + dy[i]

            if 0 <= mx < N and 0 <= my < N and graph[mx][my] != 0 :

                if graph[mx][my] == 3 :
                    check = True
                    break
                elif graph[mx][my] == 4 :
                    temp_pos = [mx, my]
                    break

        if check == True :
            result_move.append(path[-1])

            for j in range(len(path)-1) :
                result_move.append([path[j][0], path[j][1]])

        else :
            result_move.append(temp_pos)

            for j in range(len(path)-1) :
                result_move.append([path[j][0], path[j][1]])


        # 업데이트 전 이전 그래프 좌표들 업데이트
        for [x, y] in team_path[idx] :
            graph[x][y] = 4

        for pos_idx in range(len(result_move)) :
            x, y = result_move[pos_idx][0], result_move[pos_idx][1]
            if pos_idx == 0 :
                graph[x][y] = 1
            elif pos_idx == len(result_move)-1 :
                graph[x][y] = 3
            else :
                graph[x][y] = 2

        team_path[idx] = result_move



for i in range(M) :
    find_team_path(i)

time = 0
answer = 0
while time < K :
    # 모든 팀 이동
    all_team_move()
    #공 던지기
    shot_ball(time)
    time +=1

print(answer)