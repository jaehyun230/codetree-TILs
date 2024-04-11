# 판 사이즈, 도망자 수, 나무 수, 게임 턴 수
N, M, H, K = map(int, input().split())

#게임판
graph = [[0] * N for _ in range(N)]

#도망자
runner = []
#도망자 생존 여부
runner_alive = [True] * M

center = N//2
# 술래 시작 위치 , 현재 방향, 방향 전환 까지 남은 횟수, 방향전환 후 내 걸음 수, 2번 방향전환 마다 걸음 수 +=1, 거꾸로 도는 상태 체크
player = [center, center, 0, 1, 1, 2, False]

# 위 오 아 왼 -> 술래 방향
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

# 도망자 방향 1 -> 오른쪽시작,  2 -> 아래쪽시작
ddx = [-1, 0, 1, 0]
ddy = [0, 1, 0, -1]

for _ in range(M) :
    runner_x, runner_y, runner_d = map(int, input().split())
    #도망자 집어넣기
    runner.append([runner_x-1, runner_y-1, runner_d])

for _ in range(H) :
    tree_x, tree_y = map(int, input().split())
    # 해당 위치 나무로 바꾸기
    graph[tree_x-1][tree_y-1] = 1

# 도망자가 거리 3이하라서 도망 치려고 할 때
def run_move(rx, ry, rd, idx) :

    mx, my = rx +dx[rd], ry + dy[rd]

    #격자판 내부일 때
    if 0 <= mx < N and 0 <= my < N :
        # 이동하려는 칸이 술래 위치일 때
        if mx == player[0] and my == player[1] :
            runner[idx] = [rx, ry, rd]
        else :
            runner[idx] = [mx, my, rd]

    # 만약 격자 벗어나면 방향 전환
    else :
        rd = (rd+2)%4

        nmx, nmy = rx + dx[rd], ry + dy[rd]

        if 0 <= nmx < N and 0 <= nmy < N :
            # 방향전환해서 갈려는 곳이 술래 있으면 이동 x 방향 정보만 바뀜
            if nmx == player[0] and nmy == player[1] :
                runner[idx] = [rx, ry, rd]
            # 방향 전환해서 갈려는곳 술래 없으면 해당 이동한 위치로 업데이트
            else :
                runner[idx] = [nmx, nmy, rd]




def runner_move() :
    for idx in range(M) :
        # 도망자가 이미 잡힌 경우 패스
        if runner_alive[idx] == False :
            continue
        rx, ry, rd = runner[idx]

        # 도망자가 술래와의 거리가 3이하인 경우 도망
        if abs(rx-player[0]) + abs(ry-player[1]) <= 3 :
            run_move(rx, ry, rd, idx)

def catch(x, y, d, t) :
    global answer

    for i in range(3) :
        mx = x + dx[d]*i
        my = y + dy[d]*i

        # 격자 안에 있고 해당 위치에 나무가 없는 경우
        if 0 <= mx < N and 0 <= my < N and graph[mx][my] != 1 :

            for idx in range(M) :
                # 이미 잡힌 도망자는 패스
                if runner_alive[idx] == False :
                    continue
                rx, ry, rd = runner[idx]

                # 잡힌 도망자
                if rx == mx and ry == my :
                    runner_alive[idx] = False
                    answer +=t



def player_move(t) :
    global player
    # 술래 시작 위치 , 현재 방향, 방향 전환 까지 남은 횟수, 방향전환 후 내 걸음 수, 2번 방향전환 마다 걸음 수 +=1, 거꾸로 도는 상태 체크
    nx, ny, nd, need_d, next_d, count, check = player

    if check == False :

        # 현재 방향으로 이동
        mx, my = nx + dx[nd], ny + dy[nd]

        need_d -=1
        # 방향 전환까지 남은 횟수가 0 될경우
        if need_d == 0 :
            nd = (nd+1)%4

            count -=1
            # 방향전환횟수 2번 채워지면 다음부터 초기화 걸음 수 +=1
            if count == 0 :
                next_d +=1
                count = 2

            need_d = next_d

        # 방향 전환 지점 도착 한 경우
        if mx == 0 and my == 0 :
            check = True
            nd = (nd+2)%4
            count = 3
            next_d -=1
            need_d = next_d

        player = [mx, my, nd, need_d, next_d, count, check]



    # 역방향 가는 상태인 경우
    else :

        mx, my = nx + dx[nd], ny + dy[nd]

        need_d -=1
        # 방향 전환 남은 횟수 0
        if need_d == 0 :
            nd = (nd-1)%4

            count -=1
            # 방향 전환 카운트 다 떨어지면 필요 걸음 수 변경
            if count == 0 :
                next_d -=1
                count =2

            need_d = next_d

        if mx == center and my == center :
            check = False
            nd = 0
            count = 2
            need_d = 1
            next_d = 1

        player = [mx, my, nd, need_d, next_d, count, check]

    # 현재 위치에서 바라보는 방향으로 잡기
    catch(mx, my, nd, t)

time = 1
answer = 0
while time < K+1 :

    # 도망자 먼저 움직임
    runner_move()
    # 다음 술래 움직임
    player_move(time)
    time +=1

print(answer)