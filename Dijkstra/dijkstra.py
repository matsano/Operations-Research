import graph
import sys

def main():
    
    # Exercice 4.2
    cities = []
    cities.append("Paris")
    cities.append("Hambourg")
    cities.append("Londres")
    cities.append("Amsterdam")
    cities.append("Edimbourg")
    cities.append("Berlin")
    cities.append("Stockholm")
    cities.append("Rana")
    cities.append("Oslo")

    g = graph.Graph(cities)
    
    g.addArc("Paris", "Hambourg", 7)
    g.addArc("Paris",  "Londres", 4)
    g.addArc("Paris",  "Amsterdam", 3)
    g.addArc("Hambourg",  "Stockholm", 1)
    g.addArc("Hambourg",  "Berlin", 1)
    g.addArc("Londres",  "Edimbourg", 2)
    g.addArc("Amsterdam",  "Hambourg", 2)
    g.addArc("Amsterdam",  "Oslo", 8)
    g.addArc("Stockholm",  "Oslo", 2)
    g.addArc("Stockholm",  "Rana", 5)
    g.addArc("Berlin",  "Amsterdam", 2)
    g.addArc("Berlin",  "Stockholm", 1)
    g.addArc("Berlin",  "Oslo", 3)
    g.addArc("Edimbourg",  "Oslo", 7)
    g.addArc("Edimbourg",  "Amsterdam", 3)
    g.addArc("Edimbourg",  "Rana", 6)
    g.addArc("Oslo",  "Rana", 2)
    

    '''
    # Exercice 4.3
    nods = []
    nods.append("r")
    nods.append("a")
    nods.append("b")
    nods.append("c")
    nods.append("d")
    nods.append("e")
    nods.append("f")
    nods.append("g")
    g = graph.Graph(nods)
    g.addArc("r", "a", 5)
    g.addArc("r", "b", 4)
    g.addArc("a", "c", 3)
    g.addArc("b", "a", 5)
    g.addArc("b", "c", 3)
    g.addArc("b", "g", 9)
    g.addArc("c", "d", 2)
    g.addArc("c", "f", 6)
    g.addArc("c", "g", 8)
    g.addArc("d", "a", 8)
    g.addArc("d", "e", 2)
    g.addArc("e", "c", 4)
    g.addArc("g", "f", 5)
    '''

    '''
    # Exercice 4.3
    nods = []
    nods.append("r")
    nods.append("A")
    nods.append("B")
    nods.append("C")
    nods.append("D")
    nods.append("E")
    nods.append("F")
    nods.append("G")
    g = graph.Graph(nods)
    g.addArc("r", "A", 2)
    g.addArc("r", "G", 3)
    g.addArc("A", "B", 3)
    g.addArc("A", "F", 1)
    g.addArc("B", "C", 2)
    g.addArc("D", "C", 2)
    g.addArc("E", "D", 3)
    g.addArc("E", "F", 2)
    g.addArc("F", "D", 4)
    g.addArc("F", "G", 3)
    g.addArc("G", "E", 2)
    '''

    
    # Applique l'algorithme de Dijkstra pour obtenir une arborescence
    # Pour l'exercice 4.2:
    tree = dijkstra(g, "Paris")
    # Pour l'exercice 4.3:
    #tree = dijkstra(g, "r")

    print(tree)



def dijkstra(g, origin):
    # Get the index of the origin 
    r = g.indexOf(origin)

    # Next node considered 
    pivot = r
    
    # Liste qui contiendra les sommets ayant été considérés comme pivot
    v2 = []
    v2.append(r)
    
    pred = [0] * g.n
    
    # Les distances entre r et les autres sommets sont initialement infinies
    pi = [sys.float_info.max] * g.n
    pi[r] = 0
    
    # Ajouter votre code ici
    tree = graph.Graph(g.nodes)

    for i in range(1, g.n):
        for node in g.nodes:
            j = g.indexOf(node)
            destinations = getDestinations(g.getArcs(), pivot)
            if (j in destinations) and (j not in v2):
                if (pi[pivot] + g.adjacency[pivot, j]) < pi[j]:
                    pi[j] = pi[pivot] + g.adjacency[pivot, j]
                    pred[j] = pivot
        
        pivot = getNewPivot(v2, pi)
        v2.append(pivot)
        tree.addArcByIndex(pred[pivot], pivot, g.adjacency[pred[pivot]][pivot])
    
    return tree


# Obtenir les noeuds dont le precedent est le pivot
def getDestinations(arcs, index1):
    destinations = []
    for i in arcs:
        if i.id1 == index1:
            destinations.append(i.id2)
    return destinations

# Determiner le nouveau pivot, celui avec le plus petit pi et qui n'a été pas encore un pivot
def getNewPivot(v2, pi):
    minPi = sys.float_info.max
    for i in range (len(pi)):
        if (i not in v2) and (pi[i] < minPi):
            minPi = pi[i]
            newPivot = i
    return newPivot
   
if __name__ == '__main__':
    main()
