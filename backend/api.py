from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List
import random
from randomcolor import RandomColor
from pyclustering.gcolor.dsatur import dsatur
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configurer le logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

# Ajout du middleware CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Définition des modèles
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

# Fonction pour calculer la matrice d'adjacence
def compute_adj_mat(graph: Graph):
    res = []
    for n in graph.nodes:
        tmp = []
        for m in graph.nodes:
            ii = len([l for l in graph.links if l.source == n.id and l.target == m.id])
            oo = len([l for l in graph.links if l.target == n.id and l.source == m.id])
            tmp.append(ii + oo)
        res.append(tmp)
    return res

# Route pour générer un graphe aléatoire
@app.get("/random", response_model=Graph)
def generate_random_graph(
    number_of_nodes: int = Query(..., gt=0),
    probability_connection: float = Query(..., ge=0.0, le=1.0)
):
    rand_color = RandomColor()
    nodes = []
    for i in range(number_of_nodes):
        node = Node(
            id=i,
            name=f"Node {i}",
            color=rand_color.generate()[0]  # Génère une couleur aléatoire
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

# Route pour colorer un graphe en utilisant l'algorithme DSATUR
@app.post("/graph/color/dsatur", response_model=Graph)
def color_graph(graph: Graph) -> Graph:
    logger.info("Coloration du graphe en cours...")

    # Calcul de la matrice d'adjacence
    adj_mat = compute_adj_mat(graph)

    # Application de l'algorithme DSATUR
    d = dsatur(adj_mat)
    d.process()
    colors = d.get_colors()

    # Générer un nombre limité de couleurs en fonction du nombre de classes de couleurs
    num_colors = max(colors) + 1
    rand_color = RandomColor()
    colors_array = rand_color.generate(count=num_colors)

    # Mise à jour des couleurs des nœuds avec les classes de couleurs
    for n in graph.nodes:
        n.color = colors_array[colors[n.id]]

    return graph
