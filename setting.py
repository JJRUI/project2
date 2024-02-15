import pyautogui


screen_width, screen_height = pyautogui.size()
window_width = 400
window_height = 560
X = (screen_width - window_width) // 2
Y = (screen_height - window_height) // 2


def house(x, y):
    M = 8
    # 列表用于存储棋盘位置的步数
    chessboard = [[0] * M for _ in range(M)]
    dr = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
    return chessboard, dr, (x, y)

def get_next_moves(p, dr, chessboard):
    x, y = p
    next_moves = []
    for dx, dy in dr:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(chessboard) and 0 <= ny < len(chessboard[0]) and chessboard[nx][ny] == 0:
            next_moves.append((nx, ny))
    next_moves.sort(key=lambda m: len(get_valid_moves(m, dr, chessboard)))    # 从大到小排序得到最优路径
    return next_moves

def get_valid_moves(p, dr, chessboard):
    x, y = p
    valid_moves = []
    for dx, dy in dr:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(chessboard) and 0 <= ny < len(chessboard[0]) and chessboard[nx][ny] == 0:
            valid_moves.append((nx, ny))
    return valid_moves

# 深度优先遍历
def DFS(p, k, dr, chessboard, path):
    x, y = p
    chessboard[x][y] = k
    path.append((x, y))

    if k == len(chessboard) * len(chessboard[0]):
        return True

    # 找出最优路径
    next_moves = get_next_moves(p, dr, chessboard)
    for move in next_moves:
        if DFS(move, k + 1, dr, chessboard, path):
            return True

    chessboard[x][y] = 0  # 清0
    path.pop()  # 回溯：删除前一步
    return False

def knights_tour(x, y):
    chessboard, dr, start_position = house(x, y)
    path = []
    DFS(start_position, 1, dr, chessboard, path)
    return path
