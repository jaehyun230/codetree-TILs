from collections import deque

N, M, Q = map(int, input().split())
# 게임 판 (벽 / 함정)
graph =[]
# 기사 모음
knights = []
# 기사들이 위치한 좌표
knights_graph = [[-1]*N for _ in range(N)]

knights_alive = [True] * M

knights_score = [0] * M

# 위 오 아 왼
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

for _ in range(N) :
    graph.append(list(map(int, input().split())))

for idx in range(M) :
    r, c, h, w, k = map(int, input().split())
    knights.append([r-1, c-1, h, w, k, idx])

def knight_graph_update() :
    global knights_graph

    knights_graph = [[-1]* N for _ in range(N)]

    for idx in range(M) :
        # 기사가 죽은경우 패스
        if knights_alive[idx] == False :
            continue

        r, c, h, w, k, num = knights[idx]
        # 해당 위치에 idx 기사가 차지하고있음
        for i in range(r, r+h) :
            for j in range(c, c+w) :
                knights_graph[i][j] = idx



def order(num, d) :

    move_set = set()
    move_set.add(num)
    q = deque()
    q.append(num)

    visited =[[False] *N for _ in range(N)]

    damage_temp = [0] * M

    while q :
        knight_num = q.popleft()
        r, c, h, w, k, _ = knights[knight_num]

        for i in range(r, r+h) :
            for j in range(c, c+w) :
                mx = i + dx[d]
                my = j + dy[d]

                if 0 <= mx < N and 0 <= my < N and visited[mx][my] == False and graph[mx][my] != 2 :
                    visited[mx][my] = True
                    if knights_graph[mx][my] != -1 :
                        # 해당 기사 아직 연쇄작용 한적없으면 연쇄 작용 등록
                        if knights_graph[mx][my] not in move_set :
                            move_set.add(knights_graph[mx][my])
                            q.append(knights_graph[mx][my])

                    if graph[mx][my] == 1 :
                        damage_temp[knight_num] +=1


                # 아닌 경우가 하나라도 있으면 이동 불가 -> 벽 or 범위 밖으로 이동
                else :
                    return

    # 명령 받은 기사는 체력 안깍임
    damage_temp[num] = 0

    for idx in move_set :
        # 현재 기사 정보들
        nr, nc, nh, nw, nk, nnum = knights[idx]
        # 체력 이상의 피해 받으면 죽음 처리
        if nk <= damage_temp[idx] :
            knights_alive[idx] = False
            continue

        # 받은 피해 기록 및 스코어 기록
        knights_score[idx] += damage_temp[idx]
        nk -= damage_temp[idx]

        mr, mc = nr + dx[d], nc + dy[d]
        # 기사 정보 업데이트
        knights[idx] = [mr, mc, nh, nw, nk, nnum]

    knight_graph_update()

knight_graph_update()
for _ in range(Q) :
    num, direct = map(int, input().split())
    order(num-1, direct)

answer = 0

for idx in range(M) :
    if knights_alive[idx] == True :
        answer += knights_score[idx]

print(answer)