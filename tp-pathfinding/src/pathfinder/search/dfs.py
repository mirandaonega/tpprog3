from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)
        if node.state == grid.end:
            return Solution(node) #revisar
        frontier = StackFrontier()
        frontier.add(node) 


        # Initialize the explored dictionary to be empty
        expanded = {} 
        
        while True:
            if frontier.is_empty():
                return NoSolution() #REVISAR
            
            node = frontier.pop()

            if node.state in expanded:
                continue
        
            expanded[node.state] = node

            successors = grid.get_neighbours(node.state)

            for action, position in successors.items():
                p_solucion = node.state #revisar

                if p_solucion not in expanded:
                    p_node = Node(
                        value=p_solucion,
                        state = node, 
                        cost = node.cost + grid.get_cost(position),
                        parent = node, 
                        action = action
                    )

                if p_solucion == grid.end:
                    return Solution(p_node)
                
                frontier.add(p_node)
        
        # Add the node to the explored dictionary
        expanded[node.state] = True
        
        return NoSolution(expanded)
