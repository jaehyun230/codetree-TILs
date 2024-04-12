from collections import deque

# 이동 우선 순위
dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]

# 행이작은 / 열이작은 우선순위
base_camp = []

N, M = map(int, input().split())
# 게임 판
graph = []
# 게임에 참여한 손님들 -> 자신의 현재 좌표와, 목적지 좌표가 필요할거 같음
play_guest = []
# 아직 참여안한 손님들
guest = deque()
# 게임 끝난 참가자
end_guest = [False] * M

for _ in range(N) :
    graph.append(list(map(int, input().split())))

# 참여자 목적지 정보
for _ in range(M) :
    gx, gy = map(int, input().split())
    guest.append([gx-1, gy-1])

# 어느 방향으로 한걸음 가야할지 찾기
def find_one_step(sx, sy, tx, ty) :
    q = deque()
    # 3번쨰 값이 시작 방향
    visited = [[False]*N for _ in range(N)]

    for i in range(4) :
        mx = sx + dx[i]
        my = sy + dy[i]
        if 0 <= mx < N and 0 <= my < N and graph[mx][my] != -1 and visited[mx][my] == False :
            visited[mx][my] = True
            q.append([mx, my, mx, my])
        if mx == tx and my == ty :
            return mx, my

    while q :
        x, y, x2, y2 = q.popleft()

        for i in range(4) :
            mx = x + dx[i]
            my = y + dy[i]
            if 0 <= mx < N and 0 <= my < N and graph[mx][my] != -1 and visited[mx][my] == False :
                visited[mx][my] = True
                q.append([mx, my, x2, y2])
            if mx == tx and my == ty :
                # 첫 걸음 좌표 리턴
                return x2, y2

def move_play_guest() :

    temp = []

    for idx, g in enumerate(play_guest) :
        if end_guest[idx] == True :
            continue
        sx, sy, tx, ty = g
        rx, ry = find_one_step(sx, sy, tx, ty)
        temp.append([rx, ry, tx, ty, idx])

    # 모두가 이동한 후에 이동한 걸음에 대해 도착하였는지 확인하고 도착하였으면 도착 업데이트 후 해당 부분 이동 불가
    for data in temp :
        result_x, result_y, target_x, target_y, guest_num = data

        if result_x == target_x and result_y == target_y :
            end_guest[guest_num] = True
            graph[result_x][result_y] = -1

        play_guest[guest_num] = [result_x, result_y, target_x, target_y]

def find_start_point(sx, sy) :

    q = deque()
    q.append([sx, sy, 0])
    visited = [[False]*N for _ in range(N)]
    visited[sx][sy] = True

    # 임시 거리값 저장
    now_dist = 1000
    # 찾을 시작할 지점 값 초기화
    result_x, result_y = -1, -1

    while q :
        x, y, d = q.popleft()
        for i in range(4) :
            mx = x + dx[i]
            my = y + dy[i]
            # 해당이 격자판 내부에 존재하고 이동 불가지역이 아닌 경우
            if 0 <= mx < N and 0 <= my < N and graph[mx][my] != -1 and visited[mx][my] == False and d < now_dist :
                visited[mx][my] = True
                q.append([mx, my, d+1])
                # 해당 지점이 베이스 캠프인 경우
                if graph[mx][my] == 1 :
                    if d +1 < now_dist :
                        now_dist = d+1
                        result_x, result_y = mx, my
                    elif d + 1 == now_dist and mx < result_x :
                        result_x, result_y = mx, my
                    elif d + 1 == now_dist and mx == result_x and my < result_y :
                        result_x, result_y = mx, my


    return result_x, result_y


def check_end() :
    if guest :
        return False

    for g in end_guest :
        if g == False :
            return False

    return True

time = 0
while True :
    #격자에 있는 사람이 가고 싶은 편의점 방향을 향해 1칸 움직임
    move_play_guest()
    #편의점에 도착 했다면 해당 편의점은 이제 지날 수 없게됨 ( 모두 이동한 뒤 이루어짐)
    # 아직 시작하지 않은 손님이 있으면 1명 뺴내고 그사람 시작
    if guest :
        # guest의 목적 편의점 위치
        tx, ty = guest.popleft()
        # 시작 지점 찾기
        sx, sy = find_start_point(tx, ty)
        play_guest.append([sx, sy, tx, ty])
        # 시작으로 사용한 해당 베이스캠프 이제 이동 사용 불가
        graph[sx][sy] = -1
        # print(sx, sy, tx, ty)

    time +=1
    if check_end() == True :
        break

print(time)