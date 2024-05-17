"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo, y los empates se resuelvan de forma aleatoria.
Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""


from __future__ import annotations
from problem import OptProblem
from random import choice
from time import time

class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Determinar las acciones que se pueden aplicar y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val ==
                        max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un optimo local 
            # (diferencia de valor objetivo no positiva)
            if diff[act] <= 0:

                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            else:

                actual = problem.result(actual, act)
                value = value + diff[act]
                self.niters += 1


class HillClimbingReset(LocalSearch):
    """Algoritmo de ascension de colinas con reinicio aleatorio."""

    def solve(self, problem):
         # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)
        
        # Utilizaremos estos valores al aplicar los reinicios aleatorios
        self.value = float('-inf')
        reinicios = 3

        while True:

            # Determinamos las acciones que se pueden aplicar y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Buscamos las acciones que generan el mayor incremento de valor objetivo
            max_acts = [act for act, val in diff.items() if val ==
                        max(diff.values())]

            # Elegimos una acción aleatoria
            act = choice(max_acts)

            # Retornamos si estamos en un optimo local (diferencia de valor objetivo no positiva)
            if diff[act] <= 0:
                reinicios -= 1
                if self.value < value:
                    self.tour = actual
                    self.value = value
                
                # Si los reinicios son mayores a 0, volvemos a empezar
                if reinicios > 0:
                    actual = problem.random_reset()
                    value = problem.obj_val(actual)
                
                else:
                    end = time()
                    self.time = end-start
                    return

            # Si no nos movemos al sucesor
            else:
                actual = problem.result(actual, act)
                value = value + diff[act]
                self.niters += 1


# Definimos una clase para la lista tabú
class TabuList():
  def __init__(self, size: int) -> None:
    self.lista = [] 
    self.size = size
  
  # Mantiene el largo de la lista quitando elementos de esta como criterio de parada
  def add(self, action: tuple) -> None:
    """Agrega una accion a la lista tabú."""
    self.lista.append(action)
    if len(self.lista) > self.size:
      self.lista.pop(0)


class Tabu(LocalSearch):
    """Algoritmo de busqueda tabu."""

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion."""

        # Inicio del reloj
        start = time()

        # Inicializamos el problema
        actual = problem.init
        mejor_estado = actual

        # Iniciamos la lista con un tamaño de 10 y determinamos el valor objetivo
        l_tabu = TabuList(10)
        val_objetivo = problem.obj_val(problem.init)

        while self.niters < 700:
           
           # Determinar las acciones que se pueden aplicar y las diferencias en valor objetivo que resultan
           diff = problem.val_diff(actual)

           # Revisamos que la accion o su opuesta no esté en la lista tabú
           sucesores = {vecino: valor for vecino, valor in diff.items() if vecino not in l_tabu.lista and vecino[::-1] }

            # Eligimos la que tenga un mayor incremento de valor objetivo
           no_tabues = [act for act, val in sucesores.items() 
                        if val == max(sucesores.values())] 
           
           # Nos movemos al sucesor
           sucesor_selec = choice(no_tabues)

           actual = problem.result(actual, sucesor_selec)
           valor = problem.obj_val(actual)

           # Agregamos la acción que llevó al mejor vecino a la lista tabú para evitar que se repita en el futuro
           l_tabu.add(sucesor_selec)
           self.niters += 1
           
           # Si el valor objetivo del nuevo estado es mejor que el mejor valor objetivo encontrado hasta ahora, se actualiza el mejor estado y el mejor valor objetivo.
           if val_objetivo < valor:
              mejor_estado = actual
              val_obejtivo = valor

        self.tour = mejor_estado
        self.value = val_obejtivo
        end = time()
        self.time = end-start
         
        return mejor_estado