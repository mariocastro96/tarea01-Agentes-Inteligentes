#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
tarea_1.py
------------

Tarea de desarrollo de entornos y agentes
==========================================

1. Desarrolla un entorno similar al de los dos cuartos (el cual se
   encuentra en el módulo doscuartos_o.py), pero con tres cuartos en
   el primer piso, y tres cuartos en el segundo piso.
   
   El entorno se llamará `SeisCuartos`.

   Las acciones totales serán
   
   ```
   ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]
   ``` 
    
   La acción de `"subir"` solo es legal en el piso de abajo, en los cuartos de los extremos, 
   mientras que la acción de `"bajar"` solo es legal en el piso de arriba y en el cuarto de el centro (dos
   escaleras para subir, una escalera para bajar).

   Las acciones de subir y bajar son mas costosas en término de
   energía que ir a la derecha y a la izquierda, por lo que la función
   de desempeño debe de ser de tener limpios todos los cuartos, con el
   menor numero de acciones posibles, y minimizando subir y bajar en
   relación a ir a los lados. El costo de limpiar es menor a los costos
   de cualquier acción.

2. Diseña un Agente reactivo basado en modelo para este entorno y
   compara su desempeño con un agente aleatorio despues de 100 pasos
   de simulación.

3. Al ejemplo original de los dos cuartos, modificalo de manera que el
   agente solo pueda saber en que cuarto se encuentra pero no sabe si
   está limpio o sucio.

   A este nuevo entorno llamalo `DosCuartosCiego`.

   Diseña un agente racional para este problema, pruebalo y comparalo
   con el agente aleatorio.

4. Reconsidera el problema original de los dos cuartos, pero ahora
   modificalo para que cuando el agente decida aspirar, el 80% de las
   veces limpie pero el 20% (aleatorio) deje sucio el cuarto. Igualmente, 
   cuando el agente decida cambiar de cuarto, se cambie correctamente de cuarto el 90% de la veces
   y el 10% se queda en su lugar. Diseña
   un agente racional para este problema, pruebalo y comparalo con el
   agente aleatorio.

   A este entorno llámalo `DosCuartosEstocástico`.

Todos los incisos tienen un valor de 25 puntos sobre la calificación de
la tarea.

"""
__author__ = 'Mario Manuel Castro Escalante'

import entornos_o
from random import random
from random import choice
from random import shuffle

# Requiere el modulo entornos_o.py
# Usa el modulo doscuartos_o.py para reutilizar código
# Agrega los modulos que requieras de python
class DosCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de dos cuartos. Muy sencilla solo regrupa métodos.

    El estado se define como (robot, A, B)
    donde robot puede tener los valores "A", "B"
    A y B pueden tener los valores "limpio", "sucio"

    Las acciones válidas en el entorno son ("ir_A", "ir_B", "limpiar", "nada").
    Todas las acciones son válidas en todos los estados.

    Los sensores es una tupla (robot, limpio?)
    con la ubicación del robot y el estado de limpieza

    """
    def __init__(self, x0=["A", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios

        """
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        return acción in ("ir_A", "ir_B", "limpiar", "nada")

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x
        if acción is not "nada" or a is "sucio" or b is "sucio":
            self.desempeño -= 1
        if acción is "limpiar":
            self.x[" AB".find(self.x[0])] = "limpio"
        elif acción is "ir_A":
            self.x[0] = "A"
        elif acción is "ir_B":
            self.x[0] = "B"

    def percepción(self):
        return self.x[0], self.x[" AB".find(self.x[0])]


class DosCuartosCiego(entornos_o.Entorno):
    """
    Clase para un entorno de dos cuartos
    
    El robot no sabe si esta limpio o sucio por eso se le llama DosCuartosCiego
    
    """
    def __init__(self, x0=["A", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios

        """
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        return acción in ("ir_A", "ir_B", "limpiar", "nada")

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b = self.x
        if acción is not "nada" or a is "sucio" or b is "sucio":
            self.desempeño -= 1
        if acción is "limpiar":
            self.x[" AB".find(self.x[0])] = "limpio"
        elif acción is "ir_A":
            self.x[0] = "A"
        elif acción is "ir_B":
            self.x[0] = "B"

    def percepción(self):
        return self.x[0]


class DosCuartosEstocastico(entornos_o.Entorno):
    """
    Clase para un entorno de dos cuartos estocastico

    """
    def __init__(self, x0=["A", "sucio", "sucio"]):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios

        """
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        return acción in ("ir_A", "ir_B", "limpiar", "nada")

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")
        
        robot, a, b = self.x
        if acción is not "nada" or a is "sucio" or b is "sucio":
            self.desempeño -= 1
        if acción is "limpiar" and random() < .8:
            self.x[" AB".find(self.x[0])] = "limpio"
        elif acción is "ir_A" and random() < .9:
            self.x[0] = "A"
        elif acción is "ir_B" and random() < .9:
            self.x[0] = "B"

    def percepción(self):
        return self.x[0], self.x[" AB".find(self.x[0])]


class AgenteReactivoModeloDosCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio']

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' AB'.find(robot)] = situación

        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]
        return ('nada' if a == b == 'limpio' else
                'limpiar' if situación == 'sucio' else
                'ir_A' if robot == 'B' else 'ir_B')


class AgenteReactivoModeloCiego(entornos_o.Agente):
    
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio']

    def programa(self, percepción):
        robot = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        situación = self.modelo[' AB'.find(robot)]

        # Decide sobre el modelo interno
        a, b = self.modelo[1], self.modelo[2]
        
        if a == b == 'limpio':
            accion = 'nada'
        elif situación == 'sucio':
            accion = 'limpiar'
            self.modelo[' AB'.find(robot)] = 'limpio'
        elif robot == 'B':
            accion = 'ir_A'
        else:
            accion = 'ir_B'
        return accion




class SeisCuartos(entornos_o.Entorno):
    """
    Clase para un entorno de seis cuartos.
    
    Las acciones válidas en el entorno son ["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"] 
    con ciertas restricciones de que solo puedes subir o bajar si estas en los cuartos de los extremos.

    """
    def __init__(self, x0=["A", "sucio", "sucio","sucio","sucio","sucio","sucio"]):
        """
        Por default inicialmente el robot está en A y los dos cuartos
        están sucios

        """
        self.x = x0[:]
        self.desempeño = 0

    def acción_legal(self, acción):
        if self.x[0] == "A":
            return acción in ("ir_Derecha", "subir", "limpiar", "nada")
        elif self.x[0] == "C":
            return acción in ("ir_Izquierda", "subir", "limpiar", "nada")
        elif self.x[0] == "D":
            return acción in ("ir_Derecha", "bajar", "limpiar", "nada")
        elif self.x[0] == "F":
            return acción in ("ir_Izquierda", "bajar", "limpiar", "nada")
        elif self.x[0] == "B" or self.x[0] == "E":
            return acción in ("ir_Derecha", "ir_Izquierda", "limpiar", "nada")

    def transición(self, acción):
        if not self.acción_legal(acción):
            raise ValueError("La acción no es legal para este estado")

        robot, a, b, c, d, e, f = self.x
        if acción is not "nada" or a is "sucio" or b is "sucio":
            self.desempeño -= 1
        if acción is "limpiar":
            self.x[" ABCDEF".find(self.x[0])] = "limpio"
        elif acción is "ir_Derecha" and self.x[0] == "A":
            self.x[0] = "B"
        elif acción is "ir_Izquierda" and self.x[0] == "B":
            self.x[0] = "A"
        elif acción is "ir_Derecha" and self.x[0] == "B":
            self.x[0] = "C"
        elif acción is "ir_Izquierda" and self.x[0] == "C":
            self.x[0] = "B"
        elif acción is "subir" and self.x[0] == "A":
            self.desempeño -= 2
            self.x[0] = "D"
        elif acción is "subir" and self.x[0] == "C":
            self.desempeño -= 2
            self.x[0] = "F"
        elif acción is "ir_Derecha" and self.x[0] == "D":
            self.x[0] = "E"
        elif acción is "ir_Izquierda" and self.x[0] == "E":
            self.x[0] = "D"
        elif acción is "ir_Derecha" and self.x[0] == "E":
            self.x[0] = "F"
        elif acción is "ir_Izquierda" and self.x[0] == "F":
            self.x[0] = "E"
        elif acción is "bajar" and self.x[0] == "D":
            self.desempeño -= 2
            self.x[0] = "A"
        elif acción is "bajar" and self.x[0] == "F":
            self.desempeño -= 2
            self.x[0] = "C"
    
    def percepción(self):
        return self.x[0], self.x[" ABCDEF".find(self.x[0])]
    

class AgenteAleatorio(entornos_o.Agente):
    """
    Un agente que solo regresa una accion al azar entre las acciones legales

    """
    def __init__(self, acciones):
        self.acciones = acciones

    def programa(self, percepcion):
        return choice(self.acciones)


class AgenteAleatorioSeisCuartos(entornos_o.Agente):
    def __init__(self, acciones):
        self.acciones = acciones
    
    def acciones_legales(self, percepcion):
        lugar = percepcion
        azar = []
        if lugar[0] == "A":
            azar = ["ir_Derecha", "subir", "limpiar", "nada"]
        elif lugar[0] == "C":
            azar = ["ir_Izquierda", "subir", "limpiar", "nada"]
        elif lugar[0] == "D":
            azar = ["ir_Derecha", "bajar", "limpiar", "nada"]
        elif lugar[0] == "F":
            azar = ["ir_Izquierda", "bajar", "limpiar", "nada"]
        elif lugar[0] == "B" or lugar[0] == "E":
            azar = ["ir_Derecha", "ir_Izquierda", "limpiar", "nada"]
        shuffle(azar)
        
        accion = azar[1]
        return accion
    
    def programa(self, percepcion):
        return self.acciones_legales(percepcion)



       
        
class AgenteReactivoModeloSeisCuartos(entornos_o.Agente):
    """
    Un agente reactivo basado en modelo

    """
    def __init__(self):
        """
        Inicializa el modelo interno en el peor de los casos

        """
        self.modelo = ['A', 'sucio', 'sucio','sucio','sucio','sucio','sucio']

    def programa(self, percepción):
        robot, situación = percepción

        # Actualiza el modelo interno
        self.modelo[0] = robot
        self.modelo[' ABCDEF'.find(robot)] = situación

        # Decide sobre el modelo interno
        a, b, c, d, e, f = self.modelo[1], self.modelo[2], self.modelo[3], self.modelo[4], self.modelo[5], self.modelo[6]
        
        if a == b == c == d == e == f == 'limpio':
            accion = 'nada'
        elif situación == 'sucio':
            accion = 'limpiar'
        elif robot == 'A':
            accion = 'ir_Derecha'
        elif robot == 'B':
            accion = 'ir_Derecha'
        elif robot == 'C':
            accion = 'subir'
        elif robot == 'F':
            accion = 'ir_Izquierda'
        elif robot == 'E':
            accion = 'ir_Izquierda'
        elif robot == 'D':
            accion = 'nada'
        
        return accion
        
        

def test():
    """
    Prueba del entorno y los agentes

    """
    print("Prueba del entorno con un agente aleatorio")
    entornos_o.simulador(SeisCuartos(),
                         AgenteAleatorioSeisCuartos(["ir_Derecha", "ir_Izquierda", "subir", "bajar", "limpiar", "nada"]), 20)

    print("Prueba del entorno con un agente reactivo")
    entornos_o.simulador(SeisCuartos(), AgenteReactivoModeloSeisCuartos(), 20)

    print("Prueba del entorno con un agente reactivo con modelo")
    entornos_o.simulador(DosCuartos(), AgenteReactivoModeloDosCuartos(), 20)
    
    print("Prueba del entorno ciego con agente aleatorio")
    entornos_o.simulador(DosCuartosCiego(),AgenteAleatorio(['ir_A','ir_B','limpiar','nada']), 20)
    
    print("Prueba de Dos Cuartos Ciego con agente reactivo con modelo")
    entornos_o.simulador(DosCuartosCiego(), AgenteReactivoModeloCiego(), 20)

    print("Prueba de Dos Cuartos Estocastico con agente aleatorio")
    entornos_o.simulador(DosCuartosEstocastico(), AgenteAleatorio(['ir_A','ir_B','limpiar','nada']), 20)

    print("Prueba de Dos Cuartos Estocastico con agente reactivo con modelo")
    entornos_o.simulador(DosCuartosEstocastico(), AgenteReactivoModeloDosCuartos(), 20)
    
    
if __name__ == "__main__":
    test()
