# Author: Jonathan Jengo

Values = range(1, 10)
Width = 9
Height = 9

class SudokuSolver(object):

    # Solve a given unsolved sudoku puzzle
    def solve(self, rows):
        root = Node(rows)
        result = self.backtracking_search(root)
        return result.get_values() if result else None

    # Recursively search for solution node as CSP
    def backtracking_search(self, node):
        
        if node.complete:
            return node
        tile = self.select_unassigned_variable(node)

        if tile:
            for constraint in tile.constraints:
                tile.value = constraint
                next_node = Node(node.get_values())
                result = self.backtracking_search(next_node)
                if result:
                    return result
                tile.value = 0
        return None

    # Use MRV to select the variable with fewest legal constraints
    def select_unassigned_variable(self, node):
        
        tile = None
        for y in range(Height):
            for x in range(Width):

                num_constraints = len(node.tiles[y][x].constraints)
                if not num_constraints:
                    continue
                if not tile or num_constraints < len(tile.constraints):
                    tile = node.tiles[y][x]
                if num_constraints == 1:
                    return tile

        return tile

class Node(object):

    # Populate tiles and generate variable constraints
    def __init__(self, values):

        self.tiles = []
        self.complete = True

        for y in range(Height):
            row = []
            for x in range(Width):
                tile = Tile(values[y][x])
                if not tile.value:
                    self.complete = False
                row.append(tile)
            self.tiles.append(row)

        if not self.complete:
            self.generate_constraints()

    # Generate all constraints for this variable
    def generate_constraints(self):
        for y in range(Height):
            for x in range(Width):
                tile = self.tiles[y][x]
                tile.constraints = self.get_constraints_at(y, x)
        self.arc_consistency()

    # Constraints for a tile at x,y
    def get_constraints_at(self, y, x):
        constraints = []
        if not self.tiles[y][x].value:
            for value in Values:
                if self.forward_check(value, y, x):
                    constraints.append(value)
        return constraints

    # Column, row and 3x3 box cannot have more than one value
    def forward_check(self, value, ypos, xpos):

        for i in range(Height):
            if ypos != i and self.tiles[i][xpos].value == value:
                return False
        for i in range(Width):
            if xpos != i and self.tiles[ypos][i].value == value:
                return False
            
        xstart = int(xpos / 3) * 3
        ystart = int(ypos / 3) * 3
        for y in range(ystart, ystart + 3):
            for x in range(xstart, xstart + 3):
                if xpos == x and ypos == y:
                    continue
                if self.tiles[y][x].value == value:
                    return False
        
        return True
    
    # Get all row, column and 3x3 arcs in both directions.
    def get_arcs(self, y, x):

        arcs = []
        start = Point(x, y)

        for i in range(Height):
            if i != y and self.tiles[i][x].constraints:
                end = Point(x, i)
                arcs.append(Arc(start, end))
                arcs.append(Arc(end, start))
            if i != x and self.tiles[y][i].constraints:
                end = Point(i, y)
                arcs.append(Arc(start, end))
                arcs.append(Arc(end, start))

        xstart = int(x / 3) * 3
        ystart = int(y / 3) * 3
        for j in range(ystart, ystart + 3):
            for i in range(xstart, xstart + 3):
                if (i == x and j == y) or not self.tiles[j][i].constraints:
                    continue
                end = Point(i, j)
                arcs.append(Arc(start, end))
                arcs.append(Arc(end, start))

        return arcs

    # Do arc consistency checking on the tiles
    def arc_consistency(self):
        arcs = []
        for y in range(Height):
            for x in range(Width):
                if self.tiles[y][x].constraints:
                    arcs.extend(self.get_arcs(y, x))
        for arc in arcs:
            self.remove_inconsistent_values(arc)

    # Remove values not caught by forward checking.
    def remove_inconsistent_values(self, arc):
        
        consistent = []
        start_tile = self.tiles[arc.start.y][arc.start.x]
        end_tile = self.tiles[arc.end.y][arc.end.x]

        # Any value that is not empty satisfies the constraint
        for start_value in start_tile.constraints:
            for end_value in end_tile.constraints:
                if start_value != end_value:
                    consistent.append(start_value)
                    break

        start_tile.constraints = consistent

    def get_values(self):
        values = []
        for y in range(Height):
            values.append([self.tiles[y][x].value for x in range(Width)])
        return values

class Tile(object):
    def __init__(self, value):
        self.value = value
        self.constraints = []

class Arc(object):
    def __init__(self, start, end):
        self.start = start
        self.end = end

class Point(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
