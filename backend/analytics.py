import networkx as nx

from graph import build_graph


def calculate_metrics():
    graph = build_graph()

    if graph.number_of_nodes() == 0:
        return {
            "nodes": 0,
            "edges": 0,
            "density": 0,
            "communities": 0
        }

    degree = dict(graph.degree())

    betweenness = nx.betweenness_centrality(
        graph,
        normalized=True
    )

    pagerank = nx.pagerank(graph)

    for node in graph.nodes:
        graph.nodes[node]["degree"] = degree[node]
        graph.nodes[node]["betweenness"] = round(
            betweenness[node],
            4
        )
        graph.nodes[node]["pagerank"] = round(
            pagerank[node],
            4
        )

    communities = list(
        nx.community.greedy_modularity_communities(graph)
    )

    suspicious_nodes = []

    for node, data in graph.nodes(data=True):
        score = (
            degree[node] * 0.4
            + betweenness[node] * 10 * 0.35
            + pagerank[node] * 10 * 0.25
        )

        suspicious_nodes.append({
            "id": node,
            "name": graph.nodes[node].get("name"),
            "score": round(score, 3),
            "degree": degree[node],
            "betweenness": round(
                betweenness[node],
                3
            ),
            "pagerank": round(
                pagerank[node],
                3
            )
        })

    suspicious_nodes.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "density": round(
            nx.density(graph),
            4
        ),
        "communities": len(communities),
        "top_entities": suspicious_nodes[:10]
    }

