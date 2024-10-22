from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import random
from random_color import random_color
from pyclustering.gcolor.dsatur import dsatur
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Ajout du middleware CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vous pouvez spécifier les origines autorisées
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Node(BaseModel):
    id: int
    name: str
    color: str

class Link(BaseModel):
    source: int
    target: int
    weight: int

class Graph(BaseModel):
    name: str
    nodes: List[Node]
    links: List[Link]

@app.get("/random", response_model=Graph)
def generate_random_graph(number_of_nodes: int, probability_connection: float):
    nodes = []
    for i in range(number_of_nodes):
        node = Node(
            id=i,
            name=f"Node {i}",
            color=random_color()
        )
        nodes.append(node)
    
    links = []
    for i in range(number_of_nodes):
        for j in range(i + 1, number_of_nodes):
            if random.random() < probability_connection:
                link = Link(
                    source=i,
                    target=j,
                    weight=random.randint(1, 10)
                )
                links.append(link)
    
    graph = Graph(
        name="Random Graph",
        nodes=nodes,
        links=links
    )
    return graph

@app.post("/graph/color/dsatur", response_model=Graph)
def color_graph(graph: Graph):
    # Création de la matrice d'adjacence
    num_nodes = len(graph.nodes)
    adjacency_matrix = [[0]*num_nodes for _ in range(num_nodes)]
    for link in graph.links:
        adjacency_matrix[link.source][link.target] = 1
        adjacency_matrix[link.target][link.source] = 1  # Graphe non orienté

    # Application de l'algorithme DSATUR
    dsatur_instance = dsatur(adjacency_matrix)
    dsatur_instance.process()
    node_colors = dsatur_instance.get_colors()

    # Mise à jour des couleurs des noeuds
    color_map = {}
    for idx, color_idx in enumerate(node_colors):
        if color_idx not in color_map:
            color_map[color_idx] = random_color()
        graph.nodes[idx].color = color_map[color_idx]

    return graph
