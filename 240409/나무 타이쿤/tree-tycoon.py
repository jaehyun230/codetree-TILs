# 이동규칙 8가지 d
dx = [0, -1, -1, -1, 0, 1, 1, 1]
dy = [1, 1, 0, -1, -1, -1, 0, 1]

# 대각선 체크
ddx = [-1, -1, 1, 1]
ddy = [-1, 1, -1, 1]


n , m = map(int, input().split())

graph = []

# 영양제 위치
bitamin = []
# 초기 특수 영양제 위치
bitamin.append([n-1, 0])
bitamin.append([n-2, 0])
bitamin.append([n-1, 1])
bitamin.append([n-2, 1])

# 땅 상태
for _ in range(n) :
    graph.append(list(map(int, input().split())))


def move_bitamin(d, move_count) :
    global  bitamin

    temp2 = []

    for x, y in bitamin :

        mx = x +dx[d]*move_count
        my = y +dy[d]*move_count

        # 범위 벗어나도 지구돈거처럼 이동
        mx = (mx)%n
        my = (my)%n
        # 해당 위치 영양제 효과로 1 증가
        graph[mx][my] +=1

    for x, y in bitamin :
        mx = x + dx[d] * move_count
        my = y + dy[d] * move_count
        # 범위 벗어나도 지구돈거처럼 이동
        mx = (mx) % n
        my = (my) % n
        temp2.append([mx, my])

        #해당 영양제 위치에 대각선 으로 1이상 확인하여 높이 증가 시키기
        for i in range(4) :
            mmx = mx + ddx[i]
            mmy = my + ddy[i]

            if 0 <= mmx < n and 0 <= mmy < n and graph[mmx][mmy] >= 1 :
                graph[mx][my] +=1

    # 썻던 영양제 제거
    temp = []

    for i in range(n) :
        for j in range(n) :
            if graph[i][j] >= 2 and [i, j] not in temp2 :
                temp.append([i, j])
                graph[i][j] -=2

    bitamin = temp



def play(d, move_count) :
    move_bitamin(d, move_count)


# 이동 규칙 입력 받기
for _ in range(m) :
    d, move_count = map(int, input().split())
    # m번 이동 규칙에 따라 플레이
    play(d-1, move_count) #방향 0번부터 카운트 되게함

answer = 0

for i in range(n) :
    for j in range(n) :
        answer += graph[i][j]

print(answer)