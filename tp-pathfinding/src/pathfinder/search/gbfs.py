from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node

def dis_manhattan(node, destino) -> int:
    return sum(abs(a-b) for a, b in zip(node.state, destino))

class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Greedy Best First Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)
        if node.state == grid.end:
            return Solution(node) #revisar

        # Initialize the explored dictionary to be empty
        explored = {node.state: node}
        frontier = PriorityQueueFrontier
        frontier.add(node, heuristica(node, grid.end))

        while True:
            if frontier.is_empty():
                return NoSolution() #REVISAR

            node = frontier.pop()

            if node.state == grid.end:
                return Solution(node, explored)
            
            sucessors = grid.get_neighbours(node.state)

            for action, position in sucessors.items():
                c_cost = node.cost + grid.get_cost(position)

                if position not in explored or c_cost < explored[position].cost:
                    c_node = Node(
                        value="",
                        state=position,
                        cost=c_cost,
                        parent=node,
                        action=action)
                    explored[c_node.state] = c_node
                    frontier.add(c_node, heuristica(c_node, grid.end))
        
        return NoSolution(explored)
