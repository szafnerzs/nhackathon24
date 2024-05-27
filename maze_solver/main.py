from collections import deque

def maze_solver(mazes):
	def navigation(start, maze):
		queue = deque()  # specific type of storage
		queue.append((start, ''))  # stores current position and the road taken
		visited = set()  # already visited positions
		while queue:
			current_position, road = queue.popleft()
			x, y = current_position

			if maze[x][y] == 'G':  # reached G
				return road + 'G'
			visited.add((x, y))
			directions = [(0, 1, 'R'), (0, -1, 'L'), (1, 0, 'D'), (-1, 0, 'U')]

			# check all possible directions
			for direction in directions:
				dx, dy, move = direction
				new_position = (x + dx, y + dy)
				nx, ny = new_position

				# check if the new position is valid and not visited
				if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][
					ny] != '#' and new_position not in visited:
					queue.append((new_position, road + move))
					visited.add(new_position)
		return None

	solutions = []

	for maze in mazes:
		for i in range(len(maze)):
			for j in range(len(maze[0])):
				# find the starting position
				if maze[i][j] == 'S':
					solution = navigation((i, j), maze)
					solutions.append(solution)
					break

	return solutions


mazes = []  # list of mazes
input_list = []  # list of mazes from the input_file

with open("input.txt", "r") as input_file:
	for i in input_file:
		i = i.strip().replace(' ', '')
		input_list.append(i)  # add maze-line to input_list

		if i == '':
			input_list.remove(i)

input_mazes = []
sublist = []

for item in input_list:
	if len(item) == 1:  # if the item is a seperated letter A B C
		if sublist:  # if the sublist is not empty, append it to the input_mazes
			input_mazes.append(sublist)
			sublist = []  # reset sublist for the next loop
	else:
		sublist.append(item)  # add non-letter items to the sublist

# append the last sublist
if sublist:
	input_mazes.append(sublist)

for i in input_mazes:  # add every maze from the input_file in the list of Ímazes
	mazes.append(i)

# print the solutions
solutions = maze_solver(mazes)
for i, solution in enumerate(solutions, 1):
			print(f"{chr(ord('a') + i - 1).upper()}\n{' '.join(solution[0:])}\n")

