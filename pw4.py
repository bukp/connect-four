class board:
    
    def __init__(self, grid = None):
        self.player = 1
        if grid == None:
            self.grid = [["." for _ in range(8)] for _ in range(8)]
    
    def __repr__(self):
        out = ""
        out += "".join([" "+str(i+1) for i in range(len(self.grid))])+"\n"
        out += "".join([" v" for i in range(len(self.grid))])+"\n"
        for i in self.grid:
            for j in i:
                out += " "+ j
            out += "\n"
        return out
    
    def copy(self):
        return board([[j for j in i] for i in self.grid])
    
    def play(self, col):
        self.grid[list(map(lambda x: x[col-1], self.grid)).count(".")-1][col-1] = "O" if self.player == 1 else "X"
        self.player = self.player%2+1
    
    def state(self):
        slices = []
        for i in range(len(self.grid)):
            slices.append("".join(map(lambda x: x[i-1], self.grid)))
            slices.append("".join(self.grid[i]))
            slices.append("".join(map(lambda x: self.grid[i+x][x], range(len(self.grid)-i))))
            slices.append("".join(map(lambda x: self.grid[x][x+i], range(len(self.grid)-i))))
            slices.append("".join(map(lambda x: self.grid[len(self.grid)-1-x][x+i], range(len(self.grid)-i))))
            slices.append("".join(map(lambda x: self.grid[len(self.grid)-1-x-i][x], range(len(self.grid)-i))))
        for i in slices:
            if "OOOO" in i:
                return 1
            elif "XXXX" in i:
                return 2
        return 0

test = board()
while True:
    test.play(int(input(">> ")))
    print(test)
    if test.state() != 0:
        print(f"Player {test.state()} won")
        break