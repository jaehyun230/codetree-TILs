aircon = []

n, m, k = map(int ,input().split())

graph = []
workhouse = []

wall = [
    [[] for _ in range(n)] for _ in range(n)
    ]

#실제 시원함 상태 그래프
graph_air = [[0] * n for _ in range(n)]

#왼 위 오른쪽 아래
wind_dx = [0, -1, 0, 1]
wind_dy = [-1, 0, 1, 0]

#3칸별로 왼 위 오 아
# dx = [-1, 0, 1, -1, -1, -1, -1, 0, 1, 1, 1, 1]
# dy = [-1, -1, -1, -1, 0, 1, 1, 1, 1, -1, 0, 1
dx = [[-1, 0, 1], [0, 0, 0], [-1, 0, 1], [0, 0, 0]]
dy = [[0, 0, 0], [-1, 0, 1], [0, 0, 0], [-1, 0, 1]]

for _ in range(n) :
    graph.append(list(map(int ,input().split())))

for _ in range(m) :
    a, b, d = map(int, input().split())
    wall[a-1][b-1].append(d)
    if d == 1 :
        wall[a-2][b-1].append(3)
    elif d == 2 :
        wall[a-1][b-2].append(4)

for i in range(n) :
    for j in range(n) :
        if graph[i][j] == 1 :
            workhouse.append([i, j])
        elif graph[i][j] >= 2 :
            aircon.append([i, j, graph[i][j]-2 ])

def dfs_wind(x, y, d, p, add_graph) :

    add_graph[x][y] = max(add_graph[x][y], p)

    for i in range(3) :
        mx = x + dx[d][i]
        my = y + dy[d][i]

        if 0 <= mx < n and 0 <= my < n :

            if dx[d][i] == -1 and (1 in wall[x][y]) :
                continue
            if dx[d][i] == 1 and (3 in wall[x][y]) :
                continue
            if dy[d][i] == 1 and (4 in wall[x][y]) :
                continue
            if dy[d][i] == -1 and (2 in wall[x][y]) :
                continue

            mmx = mx +wind_dx[d]
            mmy = my +wind_dy[d]

            if 0 <= mmx < n and 0 <= mmy < n :
                if wind_dx[d] == -1 and (1 in wall[mx][my]) :
                    continue
                if wind_dx[d] == 1 and (3 in wall[mx][my]) :
                    continue
                if wind_dy[d] == 1 and (4 in wall[mx][my]) :
                    continue
                if wind_dy[d] == -1 and (2 in wall[mx][my]) :
                    continue
                if p > 1 :
                    dfs_wind(mmx, mmy, d, p-1, add_graph)


def wind() :

    total_add_graph = [[0]*n for _ in range(n)]
    for air in aircon :
        x, y, d = air

        # 바람 날리기 시작하는 기점
        mx = x + wind_dx[d]
        my = y + wind_dy[d]
        add_graph = [[0]*n for _ in range(n)]
        # 초기 바람세기 5
        dfs_wind(mx, my, d, 5, add_graph)

        for i in range(n) :
            for j in range(n) :
                total_add_graph[i][j] += add_graph[i][j]

    return total_add_graph


def confusewind() :
    temp_graph = [[0]* n for _ in range(n)]

    for i in range(n) :
        for j in range(n) :

            for k in range(4) :
                mx = i + wind_dx[k]
                my = j + wind_dy[k]

                if 0 <= mx < n and 0 <= my < n :
                    differ = abs(graph_air[i][j] - graph_air[mx][my])//4
                    if graph_air[i][j] > graph_air[mx][my] :
                        temp_graph[i][j] -= differ
                        temp_graph[mx][my] += differ
                    else :
                        temp_graph[i][j] += differ
                        temp_graph[mx][my] -= differ

    return temp_graph



def out_wind_minuse() :
    for i in range(n) :
        if graph_air[n-1][i] > 0 :
            graph_air[n-1][i] -=1
        if graph_air[0][i] > 0 :
            graph_air[0][i] -=1

        if graph_air[i][0] > 0 and i !=0 and i != n-1 :
            graph_air[i][0] -=1

        if graph_air[i][n-1] > 0 and i !=0 and i != n-1:
            graph_air[i][n-1] -=1

def checker() :
    for house in workhouse :
        a,b = house
        if graph_air[a][b] < k :
            return False

    return True

def calculate_air(adder) :
    global graph_air
    for i in range(n) :
        for j in range(n) :
            graph_air[i][j] +=adder[i][j]

time = 1
while time < 101 :
    #에어컨 바람불기
    addgraph = wind()

    calculate_air(addgraph)

    #바람섞기
    temper = confusewind()
    calculate_air(temper)
    #외벽깍기
    out_wind_minuse()
    if checker() :
        break
    #조건만족확인시 break
    time+=1

if k >= 101 :
    print(-1)
else :
    print(time)