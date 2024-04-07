import sys

n, m, kill_year, c  = map(int, input().split())

graph = []

cantgraph = [[0]*n for _ in range(n)]

for _ in range(n) :
    graph.append(list(map(int, input().split())))

dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

ddx = [-1, -1, 1, 1]
ddy = [-1, 1, -1, 1]

def tree_grouth() :
    add_temp = [[0]*n for _ in range(n)]

    for i in range(n) :
        for j in range(n) :
            if graph[i][j] >= 1 :
                for k in range(4) :
                    mx = i + dx[k]
                    my = j + dy[k]
                    if 0 <= mx < n and 0 <= my < n and graph[mx][my] >= 1 :
                        add_temp[i][j] +=1

    for i in range(n) :
        for j in range(n) :
            graph[i][j] += add_temp[i][j]


def tree_generate() :
    add_temp = [[0]*n for _ in range(n)]

    for i in range(n) :
        for j in range(n) :
            if graph[i][j] >=1 :
                temp = []
                for k in range(4) :
                    mx = i + dx[k]
                    my = j + dy[k]
                    if 0<= mx < n and 0 <= my < n and graph[mx][my] == 0 and cantgraph[mx][my] == 0 :
                        temp.append([mx, my])

                for a, b in temp :
                    add_temp[a][b] += graph[i][j]//len(temp)

    for i in range(n) :
        for j in range(n) :
            graph[i][j] += add_temp[i][j]

# 제초제 기간 조절
def tree_count() :
    for i in range(n) :
        for j in range(n) :
            if cantgraph[i][j] > 0 :
                cantgraph[i][j] -=1

def find_score(x, y) :

    count = graph[x][y]

    keep = [1] * 4

    for i in range(1, kill_year+1) :
        for k in range(4) :
            if keep[k] == 0 :
                continue
            mx = x + ddx[k]*i
            my = y + ddy[k]*i
            if 0 <= mx < n and 0 <= my < n and graph[mx][my] >= 1 :
                count += graph[mx][my]
            else :
                keep[k] = 0

    return count



def find_kill() :
    a, b, count = -1, -1, -1

    for i in range(n) :
        for j in range(n) :
            if graph[i][j] >= 1 :
                score = find_score(i, j)
                if score > count :
                    a, b = i, j
                    count = score

    return (a, b, count)

# 죽이고 더이상 못 자라나게 기간 c
def kill(x, y) :

    graph[x][y] = 0
    cantgraph[x][y] = c

    keep = [1] * 4

    for i in range(1, kill_year+1) :
        for k in range(4) :
            if keep[k] == 0:
                continue

            mx = x + ddx[k]*i
            my = y + ddy[k]*i
            if 0 <= mx < n and 0 <= my < n and graph[mx][my] >=1 :
                graph[mx][my] = 0
                cantgraph[mx][my] = c
            else :
                keep[k] = 0

def tree_kill() :
    global answer
    a, b, count = find_kill()
    if count != -1 :
        kill(a,b)
        answer += count


time = 0
answer = 0
while time < m :
    tree_grouth()
    # print(graph)
    tree_generate()
    # print(graph)
    # 제초제 뿌리기 전에 년도 바꾸기
    tree_count()
    tree_kill()

    time +=1

print(answer)