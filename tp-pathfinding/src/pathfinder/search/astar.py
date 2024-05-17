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
        """Encontrar el camino entre dos puntos en una grilla usando A*
        Args:
            grid (Grid): Grilla de puntos

        Returns:
            Solution: Solución encontrada
        """
        # Inicializamos un nodo en el estado inicial
        node = Node("", grid.start, 0)
        frontier = PriorityQueueFrontier()
        frontier.add(node, node.cost + h(node.state, grid.end))

        # Inicializamos el diccionario de los explorados
        explored =  {node.state: node.cost}
        
        
        while True:
            
            # Chequeamos que la frontera no esté vacía
            if frontier.is_empty():
                return NoSolution(explored) 
            
            node = frontier.pop()
        
            # Encontramos un nodo con el valor objetvio, retonamos
            if node.state == grid.end:
                return Solution(node, explored)        

            # Exploramos los sucesores
            successors = grid.get_neighbours(node.state)

            # Iteramos por cada acción  y calculamos el costo de llegar a esta
            for action, position  in successors.items():
                child_cost = node.cost + grid.get_cost(position)
                
                # Chequeamos que la posición no haya sido explorado o que haya sifo pero a un costo menor
                if position not in explored or child_cost < explored[position]:
                    child_node = Node(
                        value="",
                        state=position,
                        cost=child_cost,
                        parent=node,
                        action=action)
                    
                    # Agremos a los explorados el nuevo nodo
                    explored[child_node.state] = child_cost
                    a_star_cost = child_node.cost + h(child_node.state, grid.end)
                    frontier.add(child_node, a_star_cost)
        
        return NoSolution(explored)
