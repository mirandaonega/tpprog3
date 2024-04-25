from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)

        # Initialize the explored dictionary to be empty
        explored = {node.state: node} 
        frontier = PriorityQueueFrontier()
        frontier.add(node, node.cost)

        while True:
            #
            if frontier.is_empty():
                return NoSolution(explored)
            
            node = frontier.pop()

            if node.state==grid.end:
                return Solution(node, explored)
            
            successors = grid.get_neighbours(node.state)

            for action, position in successors.items():
                c_cost = node.cost + grid.get_cost(position)

                if position not in explored or c_cost < explored[position].cost:
                    c_node = Node(
                        value="",
                        state = position, 
                        cost = c_cost,
                        parent = node, 
                        action = action
                    )

                frontier.add(c_node, c_node.cost)
                explored[c_node.state] = c_node
        
        # Add the node to the explored dictionary
        explored[node.state] = True
        
        return NoSolution(explored)
