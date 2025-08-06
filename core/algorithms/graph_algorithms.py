"""
Graph Algorithms Module
Inspired by Robin J. Wilson's "Introduction to Graph Theory"

This module implements the core algorithms and concepts from Wilson's book,
emphasizing visual understanding and intuitive learning.
"""

import networkx as nx
from typing import List, Tuple, Optional, Dict, Set
import itertools

class WilsonGraphAlgorithms:
    """
    Educational implementation of graph algorithms following Wilson's approach.
    Focuses on understanding rather than optimization.
    """
    
    def __init__(self):
        self.algorithm_explanations = {
            "eulerian": {
                "name": "Eulerian Path/Cycle",
                "description": "A path that traverses every edge exactly once",
                "conditions": {
                    "cycle": "All vertices have even degree",
                    "path": "Exactly two vertices have odd degree"
                },
                "wilson_insight": "Euler solved the Königsberg bridge problem by realizing that the key is the number of edges meeting at each landmass."
            },
            "hamiltonian": {
                "name": "Hamiltonian Path/Cycle", 
                "description": "A path that visits every vertex exactly once",
                "conditions": {
                    "cycle": "Visits all vertices and returns to start",
                    "path": "Visits all vertices exactly once"
                },
                "wilson_insight": "Unlike Eulerian paths, there's no simple condition to determine if a Hamiltonian path exists. This is a much harder problem!"
            },
            "connectivity": {
                "name": "Connectivity",
                "description": "How well-connected a graph is",
                "conditions": {
                    "connected": "Every vertex can reach every other vertex",
                    "disconnected": "Some vertices cannot be reached from others"
                },
                "wilson_insight": "Connectivity is fundamental - it tells us whether a graph is 'in one piece' or has separate components."
            },
            "trees": {
                "name": "Trees",
                "description": "Connected graphs with no cycles",
                "conditions": {
                    "tree": "Connected and acyclic",
                    "forest": "Collection of trees"
                },
                "wilson_insight": "Trees are the 'skeleton' of connected graphs - remove edges from any connected graph and you get a tree."
            }
        }
    
    def analyze_eulerian_properties(self, graph: nx.Graph) -> Dict:
        """
        Analyze Eulerian properties following Wilson's educational approach.
        Returns detailed analysis with explanations.
        """
        if not nx.is_connected(graph):
            return {
                "has_eulerian_path": False,
                "has_eulerian_cycle": False,
                "reason": "Graph is not connected",
                "explanation": "Eulerian paths require the graph to be connected - you must be able to reach every edge from every other edge."
            }
        
        # Count degrees
        degrees = dict(graph.degree())
        odd_degree_vertices = [v for v, d in degrees.items() if d % 2 == 1]
        
        analysis = {
            "degrees": degrees,
            "odd_degree_count": len(odd_degree_vertices),
            "odd_degree_vertices": odd_degree_vertices,
            "wilson_insight": self.algorithm_explanations["eulerian"]["wilson_insight"]
        }
        
        if len(odd_degree_vertices) == 0:
            analysis.update({
                "has_eulerian_path": True,
                "has_eulerian_cycle": True,
                "reason": "All vertices have even degree",
                "explanation": "Since every vertex has an even number of edges, you can enter and leave each vertex an equal number of times, allowing you to return to your starting point."
            })
        elif len(odd_degree_vertices) == 2:
            analysis.update({
                "has_eulerian_path": True,
                "has_eulerian_cycle": False,
                "reason": f"Exactly two vertices ({odd_degree_vertices}) have odd degree",
                "explanation": "You must start at one odd-degree vertex and end at the other. The path cannot return to the start because that would require an even number of edges at each vertex."
            })
        else:
            analysis.update({
                "has_eulerian_path": False,
                "has_eulerian_cycle": False,
                "reason": f"Found {len(odd_degree_vertices)} vertices with odd degree",
                "explanation": "You cannot have an Eulerian path with more than 2 odd-degree vertices. Think about it: you need to enter and leave most vertices an equal number of times."
            })
        
        return analysis
    
    def find_eulerian_path(self, graph: nx.Graph) -> Optional[List]:
        """
        Find an Eulerian path using Hierholzer's algorithm.
        Educational implementation with step-by-step explanation.
        """
        analysis = self.analyze_eulerian_properties(graph)
        
        if not analysis["has_eulerian_path"]:
            return None
        
        # Hierholzer's algorithm
        if analysis["has_eulerian_cycle"]:
            # Start anywhere for a cycle
            start_vertex = next(iter(graph.nodes()))
        else:
            # Start at an odd-degree vertex for a path
            start_vertex = analysis["odd_degree_vertices"][0]
        
        # Create a copy of the graph to modify
        temp_graph = graph.copy()
        path = []
        current_vertex = start_vertex
        
        while temp_graph.edges():
            # Find a cycle starting from current vertex
            cycle = [current_vertex]
            next_vertex = current_vertex
            
            while True:
                # Find an edge from current vertex
                neighbors = list(temp_graph.neighbors(next_vertex))
                if not neighbors:
                    break
                
                # Take the first available edge
                next_vertex = neighbors[0]
                temp_graph.remove_edge(current_vertex, next_vertex)
                cycle.append(next_vertex)
                current_vertex = next_vertex
                
                # If we're back to start, we've completed a cycle
                if next_vertex == start_vertex and len(cycle) > 1:
                    break
            
            # Insert this cycle into the main path
            if not path:
                path = cycle
            else:
                # Find where to insert the cycle
                for i, vertex in enumerate(path):
                    if vertex == start_vertex:
                        path = path[:i] + cycle + path[i+1:]
                        break
            
            # Find next vertex with remaining edges
            for vertex in path:
                if temp_graph.degree(vertex) > 0:
                    current_vertex = vertex
                    start_vertex = vertex
                    break
        
        return path
    
    def analyze_hamiltonian_properties(self, graph: nx.Graph) -> Dict:
        """
        Analyze Hamiltonian properties. Note: This is NP-complete, so we use heuristics.
        """
        n = len(graph.nodes())
        
        analysis = {
            "wilson_insight": self.algorithm_explanations["hamiltonian"]["wilson_insight"],
            "difficulty": "NP-complete problem - no efficient general solution exists"
        }
        
        # Some necessary conditions
        if n >= 3:
            # Dirac's theorem: if every vertex has degree ≥ n/2, then Hamiltonian cycle exists
            min_degree = min(graph.degree(v) for v in graph.nodes())
            if min_degree >= n / 2:
                analysis["dirac_condition"] = True
                analysis["dirac_explanation"] = f"Every vertex has degree ≥ {n/2}, so a Hamiltonian cycle exists (Dirac's theorem)"
            else:
                analysis["dirac_condition"] = False
                analysis["dirac_explanation"] = f"Minimum degree {min_degree} < {n/2}, so Dirac's theorem doesn't apply"
        
        # Ore's theorem: if for every pair of non-adjacent vertices, sum of degrees ≥ n
        ore_condition = True
        for u, v in itertools.combinations(graph.nodes(), 2):
            if not graph.has_edge(u, v):
                if graph.degree(u) + graph.degree(v) < n:
                    ore_condition = False
                    break
        
        analysis["ore_condition"] = ore_condition
        if ore_condition:
            analysis["ore_explanation"] = "For every pair of non-adjacent vertices, sum of degrees ≥ n, so Hamiltonian cycle exists (Ore's theorem)"
        else:
            analysis["ore_explanation"] = "Ore's theorem doesn't apply - some non-adjacent vertices have degree sum < n"
        
        return analysis
    
    def find_hamiltonian_path_simple(self, graph: nx.Graph) -> Optional[List]:
        """
        Simple Hamiltonian path finder for small graphs (≤ 8 vertices).
        Uses exhaustive search for educational purposes.
        """
        n = len(graph.nodes())
        
        if n > 8:
            return None  # Too large for exhaustive search
        
        if n == 0:
            return []
        
        # Try all possible permutations
        vertices = list(graph.nodes())
        
        # Try Hamiltonian cycles first
        for perm in itertools.permutations(vertices):
            # Check if this permutation forms a cycle
            is_cycle = True
            for i in range(len(perm)):
                if not graph.has_edge(perm[i], perm[(i + 1) % len(perm)]):
                    is_cycle = False
                    break
            
            if is_cycle:
                return list(perm) + [perm[0]]  # Return as cycle
        
        # Try Hamiltonian paths
        for perm in itertools.permutations(vertices):
            # Check if this permutation forms a path
            is_path = True
            for i in range(len(perm) - 1):
                if not graph.has_edge(perm[i], perm[i + 1]):
                    is_path = False
                    break
            
            if is_path:
                return list(perm)
        
        return None
    
    def analyze_connectivity(self, graph: nx.Graph) -> Dict:
        """
        Analyze graph connectivity following Wilson's approach.
        """
        analysis = {
            "is_connected": nx.is_connected(graph),
            "wilson_insight": self.algorithm_explanations["connectivity"]["wilson_insight"]
        }
        
        if analysis["is_connected"]:
            analysis["explanation"] = "The graph is connected - you can reach any vertex from any other vertex by following edges."
        else:
            components = list(nx.connected_components(graph))
            analysis["components"] = components
            analysis["component_count"] = len(components)
            analysis["explanation"] = f"The graph has {len(components)} separate components. You cannot reach all vertices from all other vertices."
        
        # Analyze connectivity further
        if analysis["is_connected"]:
            # Find articulation points (cut vertices)
            articulation_points = list(nx.articulation_points(graph))
            analysis["articulation_points"] = articulation_points
            analysis["has_articulation_points"] = len(articulation_points) > 0
            
            if articulation_points:
                analysis["articulation_explanation"] = f"Vertices {articulation_points} are articulation points - removing any of them would disconnect the graph."
            else:
                analysis["articulation_explanation"] = "The graph has no articulation points - it remains connected when any single vertex is removed."
        
        return analysis
    
    def analyze_tree_properties(self, graph: nx.Graph) -> Dict:
        """
        Analyze tree properties following Wilson's approach.
        """
        analysis = {
            "is_tree": nx.is_tree(graph),
            "wilson_insight": self.algorithm_explanations["trees"]["wilson_insight"]
        }
        
        if analysis["is_tree"]:
            analysis["explanation"] = "This is a tree - it's connected and has no cycles. Trees are fundamental structures in graph theory."
            
            # Tree properties
            n = len(graph.nodes())
            m = len(graph.edges())
            analysis["vertex_count"] = n
            analysis["edge_count"] = m
            analysis["tree_property"] = f"n = {n}, m = {m}, so m = n-1 = {n-1}"
            analysis["tree_property_explanation"] = "In any tree, the number of edges is always one less than the number of vertices."
            
            # Find leaves (vertices of degree 1)
            leaves = [v for v in graph.nodes() if graph.degree(v) == 1]
            analysis["leaves"] = leaves
            analysis["leaf_count"] = len(leaves)
            analysis["leaf_explanation"] = f"Vertices {leaves} are leaves (degree 1). Every tree has at least 2 leaves."
            
        else:
            if not nx.is_connected(graph):
                analysis["reason"] = "Graph is not connected"
                analysis["explanation"] = "Trees must be connected - you must be able to reach any vertex from any other vertex."
            else:
                cycles = list(nx.simple_cycles(graph))
                analysis["reason"] = "Graph contains cycles"
                analysis["cycles"] = cycles
                analysis["explanation"] = f"Trees cannot have cycles. This graph contains {len(cycles)} cycle(s)."
        
        return analysis
    
    def get_educational_content(self, concept: str) -> Dict:
        """
        Get educational content for a specific concept.
        """
        if concept in self.algorithm_explanations:
            return self.algorithm_explanations[concept]
        else:
            return {
                "name": "Unknown Concept",
                "description": "This concept is not yet implemented.",
                "wilson_insight": "Check back later for more educational content!"
            }
    
    def get_learning_progression(self) -> List[Dict]:
        """
        Get the recommended learning progression based on Wilson's book.
        """
        return [
            {
                "stage": 1,
                "title": "Graph Basics",
                "concepts": ["vertices", "edges", "degree", "adjacency"],
                "description": "Start with the fundamental building blocks of graphs."
            },
            {
                "stage": 2, 
                "title": "Connectivity",
                "concepts": ["connected", "components", "articulation_points"],
                "description": "Understand how graphs can be connected or disconnected."
            },
            {
                "stage": 3,
                "title": "Special Structures", 
                "concepts": ["trees", "cycles", "paths"],
                "description": "Explore fundamental graph structures like trees and cycles."
            },
            {
                "stage": 4,
                "title": "Eulerian Paths",
                "concepts": ["eulerian_path", "eulerian_cycle", "degree_conditions"],
                "description": "Learn about paths that traverse every edge exactly once."
            },
            {
                "stage": 5,
                "title": "Hamiltonian Paths",
                "concepts": ["hamiltonian_path", "hamiltonian_cycle", "np_complete"],
                "description": "Explore the more complex problem of visiting every vertex exactly once."
            },
            {
                "stage": 6,
                "title": "Advanced Concepts",
                "concepts": ["planarity", "coloring", "matching"],
                "description": "Dive into more advanced graph theory concepts."
            }
        ] 