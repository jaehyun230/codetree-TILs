# 판크기, m개의턴, P의 산타수, 루돌프 힘, 산타 힘
N, M, P, C, D = map(int, input().split())

# 산타 이동 우선 순위 - 상 우 하 좌 - 뒤에 4개는 루돌프 대각선 움직임 추가
dx = [-1, 0, 1 ,0, -1, -1, 1, 1]
dy = [0, 1, 0 ,-1, -1, 1, -1, 1]

# 게임 판에 산타 위치
graph = [[-1] *N for _ in range(N)]
# 산타
santa = [[-1, -1]] * P
# 산타 탈락 여부 - True면 게임 살아있음
santa_alive = [True] * P
# 산타 기절 상태 시간 확인
santa_stun = [-1] * P
# 산타 얻은 점수
santa_score = [0] * P
# 루돌프 시작 좌표
sr, sc = map(int, input().split())
# 루돌프 좌표
dolpe = [sr-1, sc-1]
# 산타 초기 좌표
for _ in range(P) :
    # 산타 번호, 초기 좌표
    pn, pc, pr = map(int, input().split())
    santa[pn-1] = [pc-1, pr-1]


def santa_graph_update() :
    global graph
    # 판 초기화
    graph = [[-1]*N for _ in range(N)]

    for idx in range(P) :
        # 산타가 탈락 상태면 패스
        if santa_alive[idx] == False :
            continue
        # 산타 좌표
        sx, sy = santa[idx]
        # 해당 위치 산타 번호 나두기
        graph[sx][sy] = idx

def find_short_path() :
    nx, ny = dolpe[0], dolpe[1]

    target_x, target_y = -1, -1
    result_dist = 2501
    for idx in range(P) :
        # 탈락한 산타 아니면 거리 재기
        if santa_alive[idx] == False :
            continue
        sx, sy = santa[idx]
        # 거리는 x좌표차이 제곱 + y좌표차이 제곱
        dist = (nx-sx)**2 + (ny-sy)**2
        if dist < result_dist :
            result_dist = dist
            target_x, target_y = sx, sy
        # 거리는 같지만 행이 더 큰경우
        elif dist == result_dist and target_x < sx :
            result_dist = dist
            target_x, target_y = sx, sy
        # 거리와 행이 같지만 열이 더 큰경우
        elif dist == result_dist and target_x == sx and target_y < sy :
            result_dist = dist
            target_x, target_y = sx, sy

    return  target_x, target_y, result_dist


def push(direct, santa_num, check) :

    sx, sy = santa[santa_num]

    mx = sx + dx[direct] * check
    my = sy + dy[direct] * check
    if 0 <= mx < N and 0 <= my < N:
        # 산타 위치 업데이트
        santa[santa_num] = [mx, my]
        # 밀린 위치에 다른 산타가 있는경우 해당 방향으로 푸쉬하기
        if graph[mx][my] != -1:
            push(direct, graph[mx][my], check)

    # 격자 밖으로 밀린경우 탈락 처리
    else:
        santa_alive[santa_num] = False


    # 충돌시 힘 / 방향 / 해당위치 산타번호 / 순방향 역방향 체크 - 루돌프/산타 충돌 방향 다름
def crash(power, direct, santa_num, check) :
    global time
    # time +1 시간 까지 행동 불가능 해짐
    santa_stun[santa_num] = time+1

    # 산타 위치
    sx, sy = santa[santa_num]
    # 밀쳐내서 날라갈 산타 위치
    mx = sx + dx[direct] * power * check
    my = sy + dy[direct] * power * check
    # 밀린 파워 만큼 산타 점수 흑득
    santa_score[santa_num] += power
    # 밀린 위치가 판 안에 존재 할 경우
    if 0 <= mx < N and 0 <= my < N :
        # 산타 위치 업데이트
        santa[santa_num] = [mx, my]

        # 밀린 위치에 다른 산타가 있는경우 해당 방향으로 푸쉬하기
        if graph[mx][my] != -1 and graph[mx][my] != santa_num:
            push(direct, graph[mx][my], check)

    else :
       santa_alive[santa_num] = False


def alive_santa_point() :
    for i in range(P) :
        # 살아있다면 점수 +1
        if santa_alive[i] == True :
            santa_score[i] +=1


def move_dolpe(target_x, target_y) :
    global dolpe

    # 루돌프 현재 위치
    cx, cy = dolpe[0], dolpe[1]

    result_d = 2501
    result_x, result_y = -1, -1
    result_direct = -1

    for i in range(8) :
        mx = cx + dx[i]
        my = cy + dy[i]

        if 0 <= mx < N and 0 <= my < N :

            md = (mx-target_x)**2 + (my-target_y)**2
            # 거리가 짧으면 위치 업데이트
            if md < result_d :
                result_d = md
                result_x, result_y = mx, my
                # 방향
                result_direct = i

    dolpe[0], dolpe[1] = result_x, result_y
    # 이동한 위치에 산타가 존재 한다면
    if graph[result_x][result_y] != -1 :
        # 충돌 - 루돌프 힘, 방향, 해당위치 산타 번호
        crash(C, result_direct, graph[result_x][result_y], 1)

def move_santa(t) :
    global dolpe
    # 루돌프 현재 위치
    cx, cy = dolpe[0], dolpe[1]

    for idx in range(P) :
        # 탈락 산타 무시
        if santa_alive[idx] == False :
            continue
        # 현재 시간이상이면 스턴 상태인 것
        if santa_stun[idx] >= t :
            continue

        # 산타 위치
        sx, sy = santa[idx]
        # 현재 산타와 루돌프 거리
        now_dist = (cx-sx)**2 + (cy-sy)**2
        # 최종 산타 위치
        rx, ry = sx, sy
        # 최종 산타 방향
        rd = -1
        # 산타 가능한 움직임 방향
        for i in range(4) :
            mx = sx + dx[i]
            my = sy + dy[i]

            # 격자판 안이고 해당 위치에 산타가 없는 경우
            if 0 <= mx < N and 0 <= my < N and graph[mx][my] == -1 :
                # 움직였을 떄 거리
                move_dist = (cx-mx)**2 + (cy-my)**2
                if move_dist < now_dist :
                    rx, ry = mx, my
                    now_dist = move_dist
                    rd = i

        # 제자리 상태면 변하는거 없음
        if rd == -1 :
            continue

        # 산타가 루돌프와 충돌
        if rx == cx and ry == cy :
            santa[idx] = [rx, ry]
            crash(D, rd, idx, -1)

        # 충돌아니고 움직인 경우 위치 업데이트
        else :
            santa[idx] = [rx, ry]
        # 산타는 매번 움직일때 마다 위치 업데이트 해줘야함 - 해당위치 산타있으면 못가기 때문
        santa_graph_update()



# 게임 시작 전 산타 위치 셋팅
santa_graph_update()
time = 0
while time < M :

    tx, ty, td = find_short_path()
    # 생존한 산타가 없는 경우 임
    if td == 2501 :
        break
    # 루돌프 먼저 움직임
    move_dolpe(tx, ty)
    # 산타 움직이기전 상호작용 같은 행동한 위치들 업데이트
    santa_graph_update()
    # 산타 움직임
    move_santa(time)
    # 산타들 움직이고 나서 위치들 다시 업데이트
    santa_graph_update()
    # 생존한 산타들 점수 +1
    alive_santa_point()
    time +=1
    # print(graph, dolpe, santa_score)

for score in santa_score :
    print(score, end = " ")