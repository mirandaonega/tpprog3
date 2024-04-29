from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node
from typing import Callable

def manhattan_distance(origen, destino):
    x1,y1 = origen
    x2,y2 = destino
    return abs(x1 - x2) + abs(y1 - y2)


class AStarSearch:
    @staticmethod
    def search(grid: Grid, h: Callable[[Node, tuple[int, int]], int] = manhattan_distance ) -> Solution:
        """Find path between two points in a grid using A* Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start, 0)
        frontier = PriorityQueueFrontier()
        frontier.add(node, node.cost + h(node.state, grid.end))

        # Initialize the explored dictionary to be empty
        explored =  {node.state: node.cost}
        
        
        while True:
            
            if frontier.is_empty():
                return NoSolution(explored) 
            
            node = frontier.pop()
        
            # Return if the node contains a goal state
            if node.state == grid.end:
                return Solution(node, explored)        

            successors = grid.get_neighbours(node.state)

            for action, position  in successors.items():
                child_cost = node.cost + grid.get_cost(position)

                if position not in explored or child_cost < explored[position]:
                    child_node = Node(
                        value="",
                        state=position,
                        cost=child_cost,
                        parent=node,
                        action=action)
                    
                    explored[child_node.state] = child_cost
                    a_star_cost = child_node.cost + h(child_node.state, grid.end)
                    frontier.add(child_node, a_star_cost)
        
        return NoSolution(explored)
