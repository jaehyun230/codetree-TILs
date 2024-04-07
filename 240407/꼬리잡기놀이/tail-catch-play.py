import sys
from collections import deque

n, m, k = map(int, input().split())

# print(n, m, k)

graph = []
score = [0] * m
tims = []

head = []

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

for _ in range(n) :
    data = list(map(int, input().split()))
    graph.append(data)


number = 0
for i in range(n) :
    for j in range(n) :
        if graph[i][j] == 1 :
            head.append([i, j, number])
            number +=1


def change_head_tail(h, t) :
    for i in range(len(head)) :
        # print(head[i], h)
        if h[0][0] == head[i][0] and h[0][1] == head[i][1] :
            head[i][0] = t[0][0]
            head[i][1] = t[0][1]

            # print("헤드업뎃")

    # 그래프상 꼬리 머리 업데이트
    graph[h[0][0]][h[0][1]] = 3
    graph[t[0][0]][t[0][1]] = 1
    # print("머리 꼬리 바뀜", h, t)

# 점수를 찾은 후 머리와 꼬리 바꿀 필요 있음
def find_score(a, b) :
    global answer

    q = deque()
    # 3번째는 n번쨰 찾기위함
    q.append([a, b, 1])

    visited =[[False]*n for _ in range(n)]
    visited[a][b] = True
    temp_head = []
    temp_tail = []

    while q :
        x, y, d = q.pop()
        if graph[x][y] == 1 :
            temp_head.append([x, y])
            answer += d**2
            # print("d 번쨰가 잡음", d)

        elif graph[x][y] == 3 :
            temp_tail.append([x, y])

        for k in range(4) :
            mx = x + dx[k]
            my = y + dy[k]
            if 0 <= mx < n and 0 <= my < n and graph[mx][my] != 0 and graph[mx][my] != 4 and visited[mx][my] == False :
                visited[mx][my] = True
                if graph[x][y] == 3 and graph[mx][my] == 1 :
                    visited[mx][my] = False
                    continue
                q.append((mx, my, d+1))

    change_head_tail(temp_head, temp_tail)

def leftshot(t) :
    for i in range(n) :
        if graph[t][i] != 0 and graph[t][i] != 4 :
            find_score(t, i)
            break
        else :
            continue
def downshot(t) :
    for i in range(n-1, -1, -1) :
        if graph[i][t] != 0 and graph[i][t] != 4 :
            find_score(i, t)
            break
        else :
            continue

def rightshot(t) :
    for i in range(n-1, -1, -1) :
        if graph[n-1-t][i] != 0 and graph[n-1-t][i] != 4 :
            find_score(n-1-t, i)
            break
        else :
            continue

def upshot(t) :
    for i in range(n) :
        if graph[i][n-1-t] != 0 and graph[i][n-1-t] != 4 :
            find_score(i, n-1-t)
            break
        else :
            continue

def shot_ball(t) :
    t = t%(4*n)
    #왼쪽에서 공 날라옴
    if 0 <= t < n :
        leftshot(t)
    #아래쪽에서 공 날라옴
    elif n <= t < 2*n :
        downshot(t-n)
    elif 2*n<= t < 3*n :
        rightshot(t-2*n)
    elif 3*n<= t < 4*n :
        upshot(t-3*n)

def team_move(h) :
    q = deque()
    a, b,  c = h
    #head 라서 1
    q.append((a, b, c, 1))

    # 머리와 꼬리로 전체가 이루어진 경우도 생각 필요
    for i in range(4) :
        ma = a +dx[i]
        mb = b + dy[i]
        if 0 <= ma < n and 0 <= mb < n and graph[ma][mb] == 3 :
            graph[ma][mb] = 1
            graph[a][b] = -2
            head[c] = [ma, mb, c]
            a, b = ma, mb
            q.pop()

    if not q :
        for i in range(4) :
            ma = a + dx[i]
            mb = b + dy[i]
            if 0 <= ma < n and 0 <= mb < n :
                if graph[ma][mb] == 2 :
                    graph[ma][mb] = 3
                elif graph[ma][mb] == -2 :
                    graph[ma][mb] = 2


    while q :
        x, y, c, pos = q.pop()
        for k in range(4) :
            mx = x + dx[k]
            my = y + dy[k]
            if 0<= mx < n and 0 <= my < n and graph[mx][my] != 0 :
                if graph[mx][my] == 4 :
                    graph[mx][my] = pos

                    # head 위치 업데이트
                    if pos == 1 :
                        head[c] = [mx, my, c]

                    # 해당위치는 꼬리
                    if graph[x][y] != 3 :
                        graph[x][y] = 4

                elif graph[mx][my] == 3 :
                    graph[x][y] = 3
                    graph[mx][my] = 4

                else :
                    q.append((mx, my, c, graph[mx][my]))

def move() :
    for i in range(len(head)) :
        team_move(head[i])

time = 0
answer = 0
while time < k :

    move()
    shot_ball(time)
    time +=1
# print(graph)
print(answer)