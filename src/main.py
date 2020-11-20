from board import Board
import random, re



def minimax(b: Board, depth, maximizing, alpha, beta, x, y):
    if depth == 0:
        return b.evaluate_point(x, y)
    if b.get_empty_spaces() == 0:
        return 0
    if maximizing:
        best = -10000
        for u in b.used_positions:
            for n in b.gen_neighbours(u[0], u[1]):
                if b.is_empty(n[0], n[1]):
                    b.set_value(n[0]+1, n[1]+1, 1)
                    best = max(best, minimax(b, depth-1, not maximizing, alpha, beta, n[0], n[1]))
                    b.clear_value(n[0], n[1])
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        return best
        return best
    else:
        best = 10000
        for u in b.used_positions:
            for n in b.gen_neighbours(u[0], u[1]):
                if b.is_empty(n[0], n[1]):
                    b.set_value(n[0]+1, n[1]+1, 2)
                    best = min(best, minimax(b, depth-1, not maximizing, alpha, beta, x, y)) 
                    b.clear_value(n[0], n[1])
                    beta = min(beta, best)
                    if beta <= alpha:
                        return best
        return best

def findBestMove(b: Board):
    best_value = -1000000
    visited = set()
    loses = set()
    max_points = set()
    high_local = -10000
    local_x, local_y = 0, 0
    # local_y = 0
    for u in b.used_positions:
        for n in b.gen_neighbours(u[0], u[1]):
            if n in visited:
                continue
            visited.add(n)
            if b.is_empty(n[0], n[1]):
                b.set_value(n[0]+1, n[1]+1, 2)
                move_value = minimax(b, 3, True, -10000, 10000, n[0], n[1])
                b.clear_value(n[0], n[1])
                local = b.evaluate_point(n[0], n[1])
                print(f"({n[0]+1}, {chr(n[1]+65)}) | {move_value} | {local}")
                if move_value > best_value:
                    res_x, res_y = n[0], n[1]
                    # res_y = n[1]
                    best_value = move_value
                    max_points.clear()
                if move_value == best_value:
                    max_points.add((n[0], n[1], local))
                if local > high_local:
                    high_local = local
                    local_x, local_y = n[0], n[1]
                    if high_local > best_value:
                        res_x, res_y = local_x, local_y
                        best_value = high_local
                if move_value == -1000:
                    loses.add((n[0], n[1]))
    if best_value > 1000:
        return res_x, res_y
    if len(loses) == 1:
        return loses.pop()
    elif len(loses) > 1:
        counter = 0
        for l in loses:
            if not b.if_lose_in_this_round(l[0], l[1]):
                counter += 1
                lose_x, lose_y = l[0], l[1]
                # lose_y = l[1]
        for l in loses:
            if b.if_lose_in_this_round(l[0], l[1]):
                return l[0], l[1]
        if counter >= 2:
            return lose_x, lose_y
    max_local_points = (0, 0, 0)
    for item in max_points:
        if item[2] > max_local_points[2]:
            max_local_points = tuple(item)
    return max_local_points[0], max_local_points[1]

def game():
    b = Board()
    player = 2
    a = ""
    b.print_board()
    while not b.check_result()[0]:
        if player == 2:
            a = input("Insert the position in format X:Y\n")
            m = re.match(r'[A-O]:[1-15]', a)
            if m:
                inp = a.split(':')
                moved = b.set_value(int(inp[1]), int(ord(inp[0]))-65+1, 2)
            else:
                print("Incorrect position")
                continue
        else:
            ai_x, ai_y = findBestMove(b)
            moved = b.set_value(ai_x+1, ai_y+1, 1)
            print(f"AI moved {ai_x+1} | {chr(ai_y+65)}")
        b.print_board()
        if moved:
            if player == 1:
                player += 1
            else:
                player -= 1
    if player == 1:
        print("O wins")
    elif player == 2:
        print("X wins!")
    print("DONE")

if __name__ == '__main__':
    game()