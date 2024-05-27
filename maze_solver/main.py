# maze solving
def maze_solver(mazes):
    # depth-first algorithm
    def navigate(x, y, path, maze):
        # if we reach the goal, return the path
        if maze[x][y] == 'G':
            return path + 'G'
        # mark the current position as visited
        maze[x] = maze[x][:y] + '#' + maze[x][y+1:]
        # try in four directions
        for dx, dy, direction in [(0, 1, 'R'), (0, -1, 'L'), (1, 0, 'D'), (-1, 0, 'U')]:
            nx = x + dx
            ny = y + dy
            # if the next position is valid and not #
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != '#':
                res = navigate(nx, ny, path + direction, maze)
                # if we find the path to the goal, give it back
                if res:
                    return res
        # if no path is found, backtrack
        return None

    solutions = []

    for maze in mazes:
        # find the start position
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if maze[i][j] == 'S':
                    # start navigate from the start position
                    solution = navigate(i, j, 'S', maze)
                    solutions.append(solution)
                    break

    return solutions


mazes = [] # list of mazes
input_list = [] # list of mazes from the input_file

with open("input.txt", "r") as input_file:

    for i in input_file:
        i = i.strip().replace(' ', '')
        input_list.append(i) # add maze-line to input_list

        if i == '':
            input_list.remove(i)

input_mazes = []
sublist = []

for item in input_list:
    if len(item) == 1:  # if the item is a seperated letter A B C
        if sublist:  # if the sublist is not empty, append it to the input_mazes
            input_mazes.append(sublist)
            sublist = []  # reset sublist for the next iteration
    else:
        sublist.append(item)  # add non-letter items to the sublist

# append the last sublist
if sublist:
    input_mazes.append(sublist)

for i in input_mazes: # add every maze from the input_file in the list of mazes
    mazes.append(i)

# print the solutions
solutions = maze_solver(mazes)
for i, solution in enumerate(solutions, 1):
    print(f"{chr(ord('a')+i-1).upper()}\n{' '.join(solution[0:])}\n")
