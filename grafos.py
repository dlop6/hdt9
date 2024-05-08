import networkx as nx
import pandas as pd

import matplotlib.pyplot as plt

G = nx.Graph()

# Definición de los nombres de los nodos
nodos = {1: "Pueblo Paleta", 2: "Aldea Azalea", 
         3:"Ciudad Safiro", 4:"Ciudad Lavanda", 
         5: "Aldea Fuego"}

# Función para crear el grafo a partir de un archivo CSV
def crear_grafos():
    df = pd.read_csv('rutas.csv', sep=',', header=0)
    
    destinos = set()  # Conjunto de nodos de destino
    
    for _, row in df.iterrows():
        origen = row['estacion']
        destino = row['destino']
        costo = row['costo']
        
        # Verificar si el nodo de destino ya existe en el grafo
        if destino in destinos:
            # Si existe, agregar solo la arista desde el nodo de origen al nodo de destino
            G.add_edge(origen, destino, weight=costo)
        else:
            # Si no existe, agregar el nodo de destino y luego la arista
            G.add_node(destino)
            G.add_edge(origen, destino, weight=costo)
            destinos.add(destino)

# Función para encontrar los nodos vecinos de un nodo dado
def find_neighbors(nodo:int):
    nodos_vecinos = list(G.neighbors(nodos[nodo]))
    return nodos_vecinos

# Algoritmo de Dijkstra para encontrar la ruta más corta entre dos nodos
def dijkstra(G: nx, origen, destino):
    # Inicializar las distancias desde el nodo origen a todos los demás nodos como infinito
    distancias = {nodo: float('inf') for nodo in G.nodes()}
    # La distancia desde el nodo origen a sí mismo es 0
    distancias[origen] = 0
    # Conjunto de nodos visitados
    visitados = set()
    
    while len(visitados) < len(G.nodes()):
        # Encontrar el nodo no visitado más cercano
        nodo_actual = min((nodo for nodo in distancias.items() if nodo[0] not in visitados), key=lambda x: x[1])[0]
        visitados.add(nodo_actual)
        
        # Actualizar las distancias de los nodos vecinos del nodo actual
        for vecino in G.neighbors(nodo_actual):
            # Calcular la nueva distancia
            nueva_distancia = distancias[nodo_actual] + G[nodo_actual][vecino]['weight']
            # Actualizar la distancia si es menor que la actual
            if nueva_distancia < distancias[vecino]:
                distancias[vecino] = nueva_distancia
    
    return distancias[destino]

# Función para visualizar el grafo
def visualizacion():
    pos = nx.circular_layout(G)
    labels = nx.draw(G, pos, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

# Función para encontrar la ruta más eficiente entre dos estaciones
def ruta_eficiente(estacion: int, destino: int):
    try: 
        est = nodos[estacion]
        dest = nodos[destino]
        
        if est not in G.nodes or dest not in G.nodes:
            raise nx.NodeNotFound(f"Nodo {est} o {dest} no están en el grafo.")
        
        distancia = dijkstra(G, est, dest)
        
        return f"La distancia de {est} a {dest} es de {distancia}."
    
    except Exception as e:
        return f"Error: {str(e)}"

# Función principal del programa
def main():
    crear_grafos()
    
    while True: 
        opcion = int(input("\nBIENVENIDO A TU SISTEMA DE RUTAS FAVORITO!\nEscoge una opción:\n1. Visualizar posibles rutas\n2. Encontrar ruta más corta\n3. Salir\n"))
        
        if opcion == 1: 
            visualizacion()
        elif opcion == 2: 
            estacion = int(input("Escoja su estación: \n1. Pueblo Paleta \n2. Aldea Azalea\n3. Ciudad Safiro\n4. Ciudad Lavanda \n5. Aldea Fuego\n"))
            destino = int(input("Escoja su destino: \n1. Pueblo Paleta \n2. Aldea Azalea\n3. Ciudad Safiro\n4. Ciudad Lavanda \n5. Aldea Fuego\n"))
            print(ruta_eficiente(estacion, destino)) # Imprimimos el resultado de la función
        elif opcion == 3: 
            break

# Llamada a la función principal
main()
