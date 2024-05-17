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
        # Inicializamos un nodo con la posición inicial
        node = Node("", grid.start, cost=0)

        # Inicializamos el diccionario de nodos explorados vacío
        explored = {}

        # Inicializamos la frontera con el nodo inicial
        frontier = StackFrontier()
        frontier.add(node)

        while not frontier.is_empty():
            # Elimizamos el primer nodo de la frontera
            node = frontier.remove()

            # Return if the node contains a goal state
            if node.state == grid.end:
                return Solution(node, explored)

            if node.state not in explored:
                # Marcamos el nodo como explorado (lo agregamos al diccionario)
                explored[node.state] = True

                # Exploramos los sucesores
                successors = grid.get_neighbours(node.state)


                for action, postion in successors.items():
                    if postion not in explored:
                        child_node = Node(
                            value="",
                            state=postion,
                            cost=node.cost + grid.get_cost(postion),
                            parent=node,
                            action=action)
                        frontier.add(child_node)

        return NoSolution(explored)