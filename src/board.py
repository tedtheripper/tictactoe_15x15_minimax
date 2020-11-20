class Board:
    elements = []
    # . = 0
    # X = 1
    # O = 2
    used_positions = []
    def __init__(self):
        for i in range(0, 15):
            self.elements.append(list())
            for j in range(0, 15):
                self.elements[i].append(0)

    def set_value(self, pos_x, pos_y, value):
        if(pos_x < 1 or pos_x > 15 or pos_y < 1 or pos_y > 15):
            print("Wrong position(set)")
            return False
        if(self.elements[pos_x-1][pos_y-1] != 0):
            print(f"Move {pos_y}:{chr(65+pos_x-1)} forbidden")
            return False
        self.elements[pos_x-1][pos_y-1] = value
        self.used_positions.append((pos_x-1, pos_y-1))
        return True

    def clear_value(self, pos_x, pos_y):
        if(pos_x < 0 or pos_x > 14 or pos_y < 0 or pos_y > 14):
            print("Wrong position(clear)")
            return False
        self.elements[pos_x][pos_y] = 0
        self.used_positions.remove((pos_x, pos_y))
        return True

    def check_result(self):
        def check_vertical(x, y):
            temp = self.elements[x][y]
            if temp == 0:
                return False
            for i in range(1, 5):
                if x+i > 14:
                    return False
                if self.elements[x+i][y] != temp:
                    return False
            return True
        def check_horizontal(x, y):
            temp = self.elements[x][y]
            if temp == 0:
                return False
            for i in range(1, 5):
                if y+i > 14:
                    return False
                if self.elements[x][y+i] != temp:
                    return False
            return True
        def check_skew_up(x, y):
            temp = self.elements[x][y]
            if temp == 0:
                return False
            for i in range(1, 5):
                if x-i < 0 or y+i > 14:
                    return False
                if self.elements[x-i][y+i] != temp:
                    return False
            return True
        def check_skew_down(x, y):
            temp = self.elements[x][y]
            if temp == 0:
                return False
            for i in range(1, 5):
                if x+i > 14 or y+i > 14:
                    return False
                if self.elements[x+i][y+i] != temp:
                    return False
            return True
        for u in self.used_positions:
            if check_horizontal(u[0], u[1]) or check_vertical(u[0], u[1]) or check_skew_up(u[0], u[1]) or check_skew_down(u[0], u[1]):
                return True, self.elements[u[0]][u[1]]
        return False, None

    def get_empty_spaces(self):
        res = 0
        for i in range(0, 15):
            for j in range(0, 15):
                if self.elements[i][j] == 0:
                    res += 1
        return res

    def is_empty(self, x, y):
        if self.elements[x][y] == 0:
            return True
        return False

    def gen_neighbours(self, x, y):
        all_possible = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y+1), (x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1)]
        final_neighbours = []
        for pos in all_possible:
            if pos[0] < 0 or pos[1] < 0 or pos[0] > 14 or pos[1] > 14:
                continue
            final_neighbours.append(pos)
        return final_neighbours

    def evaluate_point(self, x, y):
        def evaluate_horizontal(x, y, dir, length, times):
            result = 0
            counter = 1
            if times == 0:
                return 0
            for i in range(1, length):
                if y+dir*i < 0 or y+dir*i > 14:
                    # return result
                    return 0
                if not self.is_empty(x, y+dir*i):
                    if self.elements[x][y+dir*i] == 1:
                        result += counter*100
                        counter += 1
                    else:
                        # if y-dir >= y-dir*(4-i+1):
                        #     for j in range(y-dir*(4-i+1), y-dir):
                        #         if not self.is_empty(x, j) and self.elements[x][j] == 2:
                        #             return 0
                        # else:
                        #     for j in range(y-dir, y-dir*(4-i+1)):
                        #         if not self.is_empty(x, j) and self.elements[x][j] == 2:
                        #             return 0
                        eeval = evaluate_horizontal(x, y, -dir, (5-i), times-1)
                        if eeval == 0:
                            return 0
                        return eeval
                result += 1
            return result 
        def evaluate_vertical(x, y, dir, length, times):
            result = 0
            counter = 1
            if times == 0:
                return 0
            for i in range(1, length):
                if x+dir*i < 0 or x+dir*i > 14:
                    # return result
                    return 0
                if not self.is_empty(x+dir*i, y):
                    if self.elements[x+dir*i][y] == 1:
                        result += counter*100
                        counter += 1
                    else:
                        eeval = evaluate_vertical(x, y, -dir, (5-i), times-1)
                        if eeval == 0:
                            return 0
                        return eeval
                result += 1
            return result 
        def evaluate_skew(x, y, dir, length, times):
            result = 0
            counter = 1
            if times == 0:
                return 0
            for i in range(1, 5):
                if x+dir*i < 0 or x+dir*i > 14 or y+dir*i < 0 or y+dir*i > 14:
                    # return result
                    return 0
                if not self.is_empty(x+dir*i, y+dir*i):
                    if self.elements[x+dir*i][y+dir*i] == 1:
                        result += counter*100
                        counter += 1
                    else:
                        eeval = evaluate_skew(x, y, -dir, (5-i), times-1)
                        if eeval == 0:
                            return 0
                        return eeval
                result += 1
            return result 
        def evaluate_anti_skew(x, y, dir, length, times):
            result = 0
            counter = 1
            if times == 0:
                return 0
            for i in range(1, 5):
                if x+dir*i < 0 or x+dir*i > 14 or y-dir*i < 0 or y-dir*i > 14:
                    # return result
                    return 0
                if not self.is_empty(x+dir*i, y-dir*i):
                    if self.elements[x+dir*i][y-dir*i] == 1:
                        result += counter*100
                        counter += 1
                    else:
                        eeval = evaluate_anti_skew(x, y, -dir, (5-i), times-1)
                        if eeval == 0:
                            return 0
                        return eeval
                result += 1
            return result
        
        res = 0
        res += evaluate_horizontal(x, y, 1, 5, 2)
        res += evaluate_vertical(x, y, 1, 5, 2)
        res += evaluate_skew(x, y, 1, 5, 2)
        res += evaluate_anti_skew(x, y, 1, 5, 2)
        res += evaluate_horizontal(x, y, -1, 5, 2)
        res += evaluate_vertical(x, y, -1, 5, 2)
        res += evaluate_skew(x, y, -1, 5, 2)
        res += evaluate_anti_skew(x, y, -1, 5, 2)
        if self.check_result()[0]:
            if self.check_result()[1] == 1:
                return res
            else:
                return -1000
        return res
        
    def if_lose_in_this_round(self, x, y):
        self.set_value(x+1, y+1, 2)
        if self.check_result()[0] and self.check_result()[1] == 2:
            self.clear_value(x, y)
            return True
        self.clear_value(x, y)
        return False
        
    def print_board(self):
        print("   ", end = "")
        for x in range(0, 15):
            print(chr(65+x), end=" ")
        print()
        for i in range(0, 15):
            if(i+1 < 10):
                print(i+1, end="  ")
            else:
                print(i+1, end=" ")
            for j in range(0, 15):
                param = ""
                if self.elements[i][j] == 0:
                    param = "."
                elif self.elements[i][j] == 1:
                    param = "X"
                elif self.elements[i][j] == 2:
                    param = "O"
                else:
                    param = "ERROR"
                print(param, end=" ")
            print()
