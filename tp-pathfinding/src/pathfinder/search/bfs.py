from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Encontrar un camino entre dos puntos de la cuadrícula usando Búsqueda Primero por Anchura

        Args:
            grid (Grid): cuadrícula de puntos
            
        Returns:
            Solution: solución encontrada
        """
        # Inicializamos un nodo con la posición inicial
        node = Node("", grid.start, cost=0)

        # Inicializamos el diccionario de nodos explorados
        explored = {node.state: True}

        if node.state == grid.end:
            return Solution(node, explored)

        # Inicializamos la frontera con el nodo inicial
        frontier = QueueFrontier()
        frontier.add(node)

        while not frontier.is_empty():          # Mientras la frontera no esté vacía
            # Eliminamos el primer nodo de la frontera
            node = frontier.remove()

            # Exploramos los sucesores
            successors = grid.get_neighbours(node.state)


            for action, postion in successors.items():
                child_node = Node(
                    value="",
                    state=postion,
                    cost=node.cost + grid.get_cost(postion),
                    parent=node,
                    action=action)

                # Si encontramos un nodo con el valor objetivo, lo retornamos
                if child_node.state == grid.end:
                    return Solution(child_node, explored)
                
                if child_node.state not in explored:
                    explored[child_node.state] = True
                    frontier.add(child_node)

        return NoSolution(explored)