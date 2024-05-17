from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node
from typing import Callable

def dis_manhattan(node, destino) -> int:
    return sum(abs(a-b) for a, b in zip(node.state, destino))

class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid, heuristica: Callable[[Node, tuple[int, int]], int] = dis_manhattan) -> Solution:
        """ Encontrar el camino entre dos puntos en una grilla usando GBFS 

        Args:
            grid (Grid): Grilla de puntos
        Returns:
            Solution: Solución encontrada
        """

        # Inicializamos un nodo en el estado inicial
        node = Node("", grid.start, 0)
        if node.state == grid.end:
            return Solution(node) 

        # Inicializamos el diccionario de los explorados
        explored = {node.state: node}
        frontier = PriorityQueueFrontier()

        # Agrego el nodo a la frontera
        frontier.add(node, heuristica(node, grid.end))

        while True:

            # Chequeamos que la frontera no esté vacía
            if frontier.is_empty():
                return NoSolution(explored) 

            node = frontier.pop()

            # Evaluamos si el nodo es un estado solución
            if node.state == grid.end:
                return Solution(node, explored)
            
            # Si no, exploro sus vecinos
            sucessors = grid.get_neighbours(node.state)

            for action, position in sucessors.items():
                c_cost = node.cost + grid.get_cost(position)

                # Chequeamos que la posición no haya sido explorado o que haya sifo pero a un costo menor
                if position not in explored or c_cost < explored[position].cost:
                    c_node = Node(
                        value="",
                        state=position,
                        cost=c_cost,
                        parent=node,
                        action=action)
                    
                    # Agremos a los explorados el nuevo nodo
                    explored[c_node.state] = c_node
                    frontier.add(c_node, heuristica(c_node, grid.end))
        
        return NoSolution(explored)
