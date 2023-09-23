import numpy as np
import graph
import sys
import collections

def main():

    # Le poids des arcs de ce graphe correspondent aux capacités
    g = example()

    # Le poids des arcs de ce graphe correspondent au flot
    flow = fordFulkerson(g, "s", "t")

    print(flow)
    
# Fonction créant un graphe sur lequel sera appliqué l'algorithme de Ford-Fulkerson
def example():
    
    # Exercice 1
    g = graph.Graph(np.array(["s", "a", "b", "c", "d", "e", "t"]))
    g.addArc("s", "a", 8)
    g.addArc("s", "c", 4)
    g.addArc("s", "e", 6)
    g.addArc("a", "b", 10)
    g.addArc("a", "d", 4)
    g.addArc("b", "t", 8)
    g.addArc("c", "b", 2)
    g.addArc("c", "d", 1)
    g.addArc("d", "b", 2)
    g.addArc("d", "t", 6)
    g.addArc("e", "b", 4)
    g.addArc("e", "t", 2)
    

    '''
    # Exercice 2 gauche
    g = graph.Graph(np.array(["s", "1", "2", "3", "4", "t"]))
    g.addArc("s", "1", 16)
    g.addArc("s", "2", 13)
    g.addArc("1", "2", 10)
    g.addArc("1", "3", 12)
    g.addArc("2", "1", 4)
    g.addArc("2", "4", 14)
    g.addArc("3", "2", 9)
    g.addArc("3", "t", 20)
    g.addArc("4", "3", 7)
    g.addArc("4", "t", 4)
    '''

    '''
    # Exercice 2 droite
    g = graph.Graph(np.array(["s", "A", "B", "C", "D", "E", "F", "t"]))
    g.addArc("s", "A", 10)
    g.addArc("s", "C", 12)
    g.addArc("s", "E", 15)
    g.addArc("A", "B", 9)
    g.addArc("A", "C", 4)
    g.addArc("A", "D", 15)
    g.addArc("B", "D", 15)
    g.addArc("B", "t", 10)
    g.addArc("C", "D", 8)
    g.addArc("C", "E", 4)
    g.addArc("D", "F", 15)
    g.addArc("D", "t", 10)
    g.addArc("E", "F", 16)
    g.addArc("F", "C", 6)
    g.addArc("F", "t", 10)
    '''
    
    return g

# Fonction appliquant l'algorithme de Ford-Fulkerson à un graphe
# Les noms des sommets sources est puits sont fournis en entrée
def fordFulkerson(g, sName, tName):

    """
    Marquage des sommets du graphe:
     - mark[j] est égal à +i si le sommet d'indice j peut être atteint en augmentant le flot sur l'arc ij
     - mark[j] est égal à  -i si le sommet d'indice j peut être atteint en diminuant le flot de l'arc ij
     - mark[j] est égal à sys.float_info.max si le sommet n'est pas marqué
    """
    mark = [0] * g.n
    
    # Récupérer l'indice de la source et du puits
    s = g.indexOf(sName)
    t = g.indexOf(tName)
    
    # Créer un nouveau graphe contenant les même sommets que g
    flow = graph.Graph(g.nodes)

    # Récupérer tous les arcs du graphe 
    arcs = g.getArcs()
    
    for i in arcs:
        flow.addArcByIndex(i.id1, i.id2, 0)

    # Ajouter votre code ici
    while True:
        mark = [sys.float_info.max] * g.n
        mark[s] = "+"
        i = 0 #index du sommet marqué
        endAlgorithm = False
        while (not endAlgorithm) and (mark[t] == sys.float_info.max):
            # Marquer des sommets
            endAlgorithm = True
            destinations = getDestinations(arcs, i)
            for j in destinations.keys():
                # if destinations[j] == True: +i
                if destinations[j]:
                    if (mark[j] == sys.float_info.max) and (flow.adjacency[i, j] != g.adjacency[i, j]):
                        mark[j] = i
                        endAlgorithm = False
                        break
                # if destinations[j] == False: -i
                else:
                    if (mark[j] == sys.float_info.max) and (flow.adjacency[j, i] != 0):
                        mark[j] = -i
                        endAlgorithm = False
                        break
            # Si aucun chemin n'est disponible, revenez au noeud précédent et voyez s'il existe un autre chemin à partir de ce noeud précédent
            if endAlgorithm:
                val = mark[i]
                mark[i] = -sys.float_info.max
                # S'il n'y a pas de chemin disponible à partir du noeud s, l'algorithme se termine
                if val != "+":
                    i = abs(int(val))
                    endAlgorithm = False
            else:
                i = j
        # L'algorithme se termine
        if endAlgorithm:
            break
        
        # Trouver la chaine ameliorante et sa valeur minimale
        newWeights = []
        for nodeId in range(len(mark)):
            if (mark[nodeId] != "+") and (mark[nodeId] != sys.float_info.max) and (mark[nodeId] != -sys.float_info.max):
                if mark[nodeId] >= 0:
                    newWeight = g.adjacency[mark[nodeId], nodeId] - flow.adjacency[mark[nodeId], nodeId]
                else:
                    newWeight = flow.adjacency[nodeId, -mark[nodeId]]
                newWeights.append(newWeight)
        minValue = min(newWeights)

        # Ajouter ou decrementer la valeur minimale
        for nodeId in range(len(mark)):
            if (mark[nodeId] != "+") and (mark[nodeId] != sys.float_info.max) and (mark[nodeId] != -sys.float_info.max):
                if mark[nodeId] >= 0:
                    flow.adjacency[mark[nodeId], nodeId] += minValue
                else:
                    flow.adjacency[nodeId, -mark[nodeId]] -= minValue
    
    return flow

# Obtenir les noeuds connectés au noeud dont l'identifiant est index
def getDestinations(arcs, index):
    destinations = {}
    for i in arcs:
        if i.id1 == index:
            destinations[i.id2] = True #if (+i), True
        elif i.id2 == index:
            destinations[i.id1] = False #if (-i), False
    
    # Trier par ordre alphabetique
    return dict(sorted(destinations.items()))

if __name__ == '__main__':
    main()
