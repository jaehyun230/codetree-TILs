from collections import deque
n, m = map(int, input().split())

graph = []

fire = []

for _ in range(n) :
    graph.append(list(map(int, input().split())))

for i in range(n) :
    for j in range(m) :
        if graph[i][j] == 2 :
            fire.append([i, j])


dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def bfs() :
    global answer

    q = deque()

    visited = [[False]*m for _ in range(n)]
    for a, b in fire :
        q.append([a, b])
        visited[a][b] = True

    while q :
        x, y = q.popleft()
        for k in range(4) :
            mx = x + dx[k]
            my = y + dy[k]
            if 0 <= mx < n and 0 <= my < m and visited[mx][my] == False and graph[mx][my] == 0 :
                visited[mx][my] = True
                q.append([mx, my])

    count = 0
    for i in range(n) :
        for j in range(m) :
            if graph[i][j] == 0 and visited[i][j] == False :
                count +=1

    answer = max(answer ,count)

#방화벽 설치 갯수 카운트
def dfs(count) :
    if count == 3 :
        bfs()

    else :
        for i in range(n) :
            for j in range(m) :
                if graph[i][j] == 0 :
                    graph[i][j] = 1
                    dfs(count+1)
                    graph[i][j] = 0

answer = 0
dfs(0)
print(answer)