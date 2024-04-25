from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

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
        frontier = QueueFrontier()
        frontier.add(node) 
        
        while True:
            if frontier.is_empty():
                return NoSolution() #REVISAR
            
            node = frontier.pop()

            successors = grid.get_neighbours(node.state)

            for action, position in successors.items():
                p_solucion = node.state #revisar
                if p_solucion not in explored:
                    p_node = Node(
                        value=p_solucion,
                        state = node, 
                        cost = node.cost + grid.get_cost(position),
                        parent = node, 
                        action = action
                    )

                    if p_solucion == grid.end:
                        return Solution(p_node)
                    
                    explored[p_solucion.state] = p_node #revisar

                    frontier.add(p_node)

"""        # Add the node to the explored dictionary
        explored[node.state] = True
        
        return NoSolution(explored)"""
