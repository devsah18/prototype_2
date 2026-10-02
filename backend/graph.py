import networkx as nx

from database import get_entities, get_relationships


def build_graph():
    graph = nx.Graph()

    entities = get_entities()
    relationships = get_relationships()

    for entity in entities:
        graph.add_node(
            entity["id"],
            name=entity["name"],
            type=entity["type"]
        )

    for relationship in relationships:
        graph.add_edge(
            relationship["source"],
            relationship["target"],
            type=relationship["type"],
            weight=relationship["weight"]
        )

    return graph


def graph_for_frontend():
    graph = build_graph()

    nodes = []

    for node_id, data in graph.nodes(data=True):
        nodes.append({
            "data": {
                "id": node_id,
                "label": data["name"],
                "type": data["type"]
            }
        })

    edges = []

    for index, (source, target, data) in enumerate(
        graph.edges(data=True)
    ):
        edges.append({
            "data": {
                "id": f"edge-{index}",
                "source": source,
                "target": target,
                "relationship": data.get("type", "CONNECTED"),
                "weight": data.get("weight", 1)
            }
        })

    return {
        "nodes": nodes,
        "edges": edges
    }
