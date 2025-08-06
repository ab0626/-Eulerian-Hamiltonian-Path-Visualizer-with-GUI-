#!/usr/bin/env python3
"""
Eulerian/Hamiltonian Path Visualizer
Inspired by Robin J. Wilson's "Introduction to Graph Theory"

A comprehensive graph theory visualization tool that emphasizes:
- Visual learning and intuition
- Interactive exploration
- Progressive complexity building
- Conceptual understanding over formalism
"""

import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import FancyBboxPatch
import networkx as nx
import numpy as np
from typing import List, Tuple, Optional, Dict
import json
import os

class GraphTheoryVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Graph Theory Visualizer - Wilson's Approach")
        self.root.geometry("1400x900")
        self.root.configure(bg='#f0f0f0')
        
        # Graph data structure
        self.graph = nx.Graph()
        self.vertices = {}  # {vertex_id: (x, y)}
        self.edges = []     # [(vertex1, vertex2), ...]
        self.current_path = []
        self.selected_vertex = None
        self.drawing_edge = False
        self.edge_start = None
        
        # Educational content based on Wilson's book
        self.learning_stages = {
            "Stage 1": {
                "title": "Gentle Introduction - Conceptual & Visual Thinking",
                "concepts": [
                    "Graph Basics and Isomorphism",
                    "Eulerian and Hamiltonian Graphs", 
                    "Trees and Connectivity",
                    "Planarity",
                    "Graph Coloring",
                    "Matching and Network Flow"
                ]
            }
        }
        
        self.setup_ui()
        self.create_example_graphs()
        
    def setup_ui(self):
        """Create the main user interface with educational focus"""
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Educational content and controls
        left_panel = ttk.Frame(main_frame, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Title and learning stage
        title_label = ttk.Label(left_panel, text="Graph Theory Visualizer", 
                               font=('Arial', 16, 'bold'))
        title_label.pack(pady=(0, 10))
        
        stage_label = ttk.Label(left_panel, text="Based on Wilson's 'Introduction to Graph Theory'",
                               font=('Arial', 10, 'italic'))
        stage_label.pack(pady=(0, 20))
        
        # Learning stage selector
        stage_frame = ttk.LabelFrame(left_panel, text="Learning Stage", padding=10)
        stage_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.stage_var = tk.StringVar(value="Stage 1")
        stage_combo = ttk.Combobox(stage_frame, textvariable=self.stage_var, 
                                  values=list(self.learning_stages.keys()), state="readonly")
        stage_combo.pack(fill=tk.X)
        stage_combo.bind('<<ComboboxSelected>>', self.on_stage_change)
        
        # Current concept display
        concept_frame = ttk.LabelFrame(left_panel, text="Current Concept", padding=10)
        concept_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.concept_label = ttk.Label(concept_frame, text="Graph Basics", 
                                      font=('Arial', 11, 'bold'))
        self.concept_label.pack()
        
        self.concept_desc = ttk.Label(concept_frame, text="Learn about vertices, edges, and basic graph structure", 
                                     wraplength=280, justify=tk.LEFT)
        self.concept_desc.pack(pady=(5, 0))
        
        # Graph creation controls
        creation_frame = ttk.LabelFrame(left_panel, text="Graph Creation", padding=10)
        creation_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(creation_frame, text="Add Vertex Mode", 
                  command=self.toggle_vertex_mode).pack(fill=tk.X, pady=2)
        ttk.Button(creation_frame, text="Add Edge Mode", 
                  command=self.toggle_edge_mode).pack(fill=tk.X, pady=2)
        ttk.Button(creation_frame, text="Clear Graph", 
                  command=self.clear_graph).pack(fill=tk.X, pady=2)
        
        # Path finding controls
        path_frame = ttk.LabelFrame(left_panel, text="Path Analysis", padding=10)
        path_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(path_frame, text="Find Eulerian Path", 
                  command=self.find_eulerian_path).pack(fill=tk.X, pady=2)
        ttk.Button(path_frame, text="Find Hamiltonian Path", 
                  command=self.find_hamiltonian_path).pack(fill=tk.X, pady=2)
        ttk.Button(path_frame, text="Clear Path", 
                  command=self.clear_path).pack(fill=tk.X, pady=2)
        
        # Example graphs
        example_frame = ttk.LabelFrame(left_panel, text="Example Graphs", padding=10)
        example_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(example_frame, text="Simple Cycle", 
                  command=lambda: self.load_example("simple_cycle")).pack(fill=tk.X, pady=2)
        ttk.Button(example_frame, text="Eulerian Graph", 
                  command=lambda: self.load_example("eulerian")).pack(fill=tk.X, pady=2)
        ttk.Button(example_frame, text="Hamiltonian Graph", 
                  command=lambda: self.load_example("hamiltonian")).pack(fill=tk.X, pady=2)
        ttk.Button(example_frame, text="Tree", 
                  command=lambda: self.load_example("tree")).pack(fill=tk.X, pady=2)
        ttk.Button(example_frame, text="Non-planar (K5)", 
                  command=lambda: self.load_example("k5")).pack(fill=tk.X, pady=2)
        
        # Graph properties
        properties_frame = ttk.LabelFrame(left_panel, text="Graph Properties", padding=10)
        properties_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.properties_text = tk.Text(properties_frame, height=8, width=35, 
                                      font=('Courier', 9), wrap=tk.WORD)
        self.properties_text.pack(fill=tk.BOTH, expand=True)
        
        # Educational insights
        insights_frame = ttk.LabelFrame(left_panel, text="Wilson's Insights", padding=10)
        insights_frame.pack(fill=tk.BOTH, expand=True)
        
        self.insights_text = tk.Text(insights_frame, height=6, width=35, 
                                    font=('Arial', 9), wrap=tk.WORD)
        self.insights_text.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Graph visualization
        right_panel = ttk.Frame(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Graph canvas
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Bind mouse events
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)
        self.canvas.mpl_connect('motion_notify_event', self.on_canvas_motion)
        self.canvas.mpl_connect('button_release_event', self.on_canvas_release)
        
        # Initialize display
        self.update_display()
        self.update_properties()
        self.update_insights("Welcome to Graph Theory! Start by creating a simple graph or loading an example.")
        
    def create_example_graphs(self):
        """Create pre-built example graphs for learning"""
        self.examples = {
            "simple_cycle": {
                "name": "Simple Cycle",
                "description": "A basic cycle graph - every vertex has degree 2",
                "vertices": [(0, 0), (1, 1), (2, 0), (1, -1)],
                "edges": [(0, 1), (1, 2), (2, 3), (3, 0)],
                "insight": "This is a simple cycle - notice how every vertex has exactly 2 edges. This is a fundamental structure in graph theory."
            },
            "eulerian": {
                "name": "Eulerian Graph",
                "description": "A graph with an Eulerian cycle - all vertices have even degree",
                "vertices": [(0, 0), (1, 1), (2, 0), (1, -1), (0.5, 0.5)],
                "edges": [(0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (1, 4), (2, 4), (3, 4)],
                "insight": "This graph has an Eulerian cycle because every vertex has even degree. You can trace every edge exactly once and return to the start."
            },
            "hamiltonian": {
                "name": "Hamiltonian Graph", 
                "description": "A graph with a Hamiltonian cycle - visits every vertex exactly once",
                "vertices": [(0, 0), (1, 1), (2, 0), (1, -1)],
                "edges": [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)],
                "insight": "This graph has a Hamiltonian cycle - you can visit every vertex exactly once and return to the start. Notice the additional edges that make this possible."
            },
            "tree": {
                "name": "Tree",
                "description": "A connected acyclic graph - no cycles, connected",
                "vertices": [(0, 0), (1, 1), (1, -1), (2, 0.5), (2, -0.5)],
                "edges": [(0, 1), (0, 2), (1, 3), (2, 4)],
                "insight": "This is a tree - it's connected (you can reach any vertex from any other) but has no cycles. Trees are fundamental structures in computer science."
            },
            "k5": {
                "name": "Complete Graph K5",
                "description": "A non-planar graph - cannot be drawn without edge crossings",
                "vertices": [(0, 0), (1, 1), (2, 0), (1, -1), (0.5, 0)],
                "edges": [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)],
                "insight": "This is K5, the complete graph on 5 vertices. It's non-planar - you cannot draw it without edges crossing. This is a key result in graph theory."
            }
        }
        
    def on_stage_change(self, event=None):
        """Handle learning stage changes"""
        stage = self.stage_var.get()
        if stage in self.learning_stages:
            concepts = self.learning_stages[stage]["concepts"]
            self.concept_label.config(text=concepts[0])
            self.concept_desc.config(text=f"Exploring: {concepts[0]}")
            
    def toggle_vertex_mode(self):
        """Toggle vertex creation mode"""
        messagebox.showinfo("Vertex Mode", "Click anywhere on the canvas to add vertices!")
        
    def toggle_edge_mode(self):
        """Toggle edge creation mode"""
        messagebox.showinfo("Edge Mode", "Click and drag between vertices to create edges!")
        
    def on_canvas_click(self, event):
        """Handle canvas click events"""
        if event.inaxes != self.ax:
            return
            
        x, y = event.xdata, event.ydata
        if x is None or y is None:
            return
            
        # Check if clicking near existing vertex
        vertex_id = self.find_nearby_vertex(x, y)
        
        if vertex_id is not None:
            # Start drawing edge
            self.drawing_edge = True
            self.edge_start = vertex_id
        else:
            # Add new vertex
            vertex_id = len(self.vertices)
            self.vertices[vertex_id] = (x, y)
            self.graph.add_node(vertex_id)
            self.update_display()
            self.update_properties()
            
    def on_canvas_motion(self, event):
        """Handle canvas mouse motion"""
        if event.inaxes != self.ax:
            return
            
        if self.drawing_edge and self.edge_start is not None:
            # Update temporary edge display
            self.update_display()
            
    def on_canvas_release(self, event):
        """Handle canvas mouse release"""
        if event.inaxes != self.ax:
            return
            
        if self.drawing_edge and self.edge_start is not None:
            x, y = event.xdata, event.ydata
            if x is not None and y is not None:
                end_vertex = self.find_nearby_vertex(x, y)
                if end_vertex is not None and end_vertex != self.edge_start:
                    # Add edge
                    self.graph.add_edge(self.edge_start, end_vertex)
                    self.edges.append((self.edge_start, end_vertex))
                    
            self.drawing_edge = False
            self.edge_start = None
            self.update_display()
            self.update_properties()
            
    def find_nearby_vertex(self, x, y, threshold=0.1):
        """Find vertex near given coordinates"""
        for vertex_id, (vx, vy) in self.vertices.items():
            if abs(x - vx) < threshold and abs(y - vy) < threshold:
                return vertex_id
        return None
        
    def clear_graph(self):
        """Clear the entire graph"""
        self.graph.clear()
        self.vertices.clear()
        self.edges.clear()
        self.current_path = []
        self.update_display()
        self.update_properties()
        self.update_insights("Graph cleared. Start building a new graph!")
        
    def clear_path(self):
        """Clear the current path display"""
        self.current_path = []
        self.update_display()
        
    def find_eulerian_path(self):
        """Find Eulerian path if it exists"""
        if len(self.graph.nodes()) == 0:
            messagebox.showwarning("No Graph", "Please create a graph first!")
            return
            
        # Check if graph is connected
        if not nx.is_connected(self.graph):
            self.update_insights("Graph is not connected. Eulerian paths require connected graphs.")
            return
            
        # Count odd degree vertices
        odd_vertices = [v for v in self.graph.nodes() if self.graph.degree(v) % 2 == 1]
        
        if len(odd_vertices) == 0:
            # Eulerian cycle exists
            try:
                path = list(nx.eulerian_circuit(self.graph))
                self.current_path = [edge[0] for edge in path] + [path[-1][1]]
                self.update_display()
                self.update_insights("Eulerian cycle found! Every vertex has even degree, so you can traverse every edge exactly once and return to start.")
            except nx.NetworkXError:
                self.update_insights("No Eulerian cycle found. The graph must be connected with all vertices having even degree.")
        elif len(odd_vertices) == 2:
            # Eulerian path exists
            try:
                path = list(nx.eulerian_path(self.graph))
                self.current_path = [edge[0] for edge in path] + [path[-1][1]]
                self.update_display()
                self.update_insights("Eulerian path found! Exactly two vertices have odd degree, so you can traverse every edge exactly once.")
            except nx.NetworkXError:
                self.update_insights("No Eulerian path found. The graph must be connected with exactly two vertices having odd degree.")
        else:
            self.update_insights(f"No Eulerian path exists. Found {len(odd_vertices)} vertices with odd degree. Eulerian paths require exactly 0 or 2 odd-degree vertices.")
            
    def find_hamiltonian_path(self):
        """Find Hamiltonian path if it exists"""
        if len(self.graph.nodes()) == 0:
            messagebox.showwarning("No Graph", "Please create a graph first!")
            return
            
        # For small graphs, try to find Hamiltonian path
        if len(self.graph.nodes()) <= 8:
            try:
                # Try to find Hamiltonian cycle first
                path = list(nx.find_cycle(self.graph, len(self.graph.nodes())))
                if len(path) == len(self.graph.nodes()):
                    self.current_path = [edge[0] for edge in path] + [path[-1][1]]
                    self.update_display()
                    self.update_insights("Hamiltonian cycle found! You can visit every vertex exactly once and return to start.")
                    return
            except nx.NetworkXNoCycle:
                pass
                
            # Try to find Hamiltonian path
            for start in self.graph.nodes():
                for end in self.graph.nodes():
                    if start != end:
                        try:
                            path = nx.shortest_path(self.graph, start, end)
                            if len(path) == len(self.graph.nodes()):
                                self.current_path = path
                                self.update_display()
                                self.update_insights("Hamiltonian path found! You can visit every vertex exactly once.")
                                return
                        except nx.NetworkXNoPath:
                            continue
                            
            self.update_insights("No Hamiltonian path found. This is a complex problem - no efficient algorithm exists for all graphs.")
        else:
            self.update_insights("Graph too large for exhaustive search. Hamiltonian path detection is NP-complete.")
            
    def load_example(self, example_name):
        """Load a pre-built example graph"""
        if example_name not in self.examples:
            return
            
        example = self.examples[example_name]
        
        # Clear current graph
        self.graph.clear()
        self.vertices.clear()
        self.edges.clear()
        self.current_path = []
        
        # Load example
        for i, (x, y) in enumerate(example["vertices"]):
            self.vertices[i] = (x, y)
            self.graph.add_node(i)
            
        for edge in example["edges"]:
            self.graph.add_edge(edge[0], edge[1])
            self.edges.append(edge)
            
        self.update_display()
        self.update_properties()
        self.update_insights(example["insight"])
        
    def update_display(self):
        """Update the graph visualization"""
        self.ax.clear()
        
        # Set up the plot
        self.ax.set_xlim(-0.5, 2.5)
        self.ax.set_ylim(-1.5, 1.5)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title("Interactive Graph Visualization", fontsize=14, fontweight='bold')
        
        # Draw edges
        for edge in self.edges:
            v1, v2 = edge
            x1, y1 = self.vertices[v1]
            x2, y2 = self.vertices[v2]
            self.ax.plot([x1, x2], [y1, y2], 'k-', linewidth=2, alpha=0.7)
            
        # Draw vertices
        for vertex_id, (x, y) in self.vertices.items():
            color = 'lightblue'
            if vertex_id in self.current_path:
                color = 'red'
            elif self.drawing_edge and vertex_id == self.edge_start:
                color = 'green'
                
            circle = plt.Circle((x, y), 0.1, color=color, ec='black', linewidth=2)
            self.ax.add_patch(circle)
            self.ax.text(x, y, str(vertex_id), ha='center', va='center', 
                        fontweight='bold', fontsize=12)
            
        # Draw current path
        if len(self.current_path) > 1:
            for i in range(len(self.current_path) - 1):
                v1, v2 = self.current_path[i], self.current_path[i + 1]
                if self.graph.has_edge(v1, v2):
                    x1, y1 = self.vertices[v1]
                    x2, y2 = self.vertices[v2]
                    self.ax.plot([x1, x2], [y1, y2], 'r-', linewidth=4, alpha=0.8)
                    
        # Draw temporary edge while drawing
        if self.drawing_edge and self.edge_start is not None:
            x1, y1 = self.vertices[self.edge_start]
            self.ax.plot([x1, x1], [y1, y1], 'g--', linewidth=2, alpha=0.5)
            
        self.canvas.draw()
        
    def update_properties(self):
        """Update the graph properties display"""
        self.properties_text.delete(1.0, tk.END)
        
        if len(self.graph.nodes()) == 0:
            self.properties_text.insert(tk.END, "No graph created yet.\n")
            return
            
        # Basic properties
        n_vertices = len(self.graph.nodes())
        n_edges = len(self.graph.edges())
        
        self.properties_text.insert(tk.END, f"Vertices: {n_vertices}\n")
        self.properties_text.insert(tk.END, f"Edges: {n_edges}\n")
        self.properties_text.insert(tk.END, f"Connected: {nx.is_connected(self.graph)}\n")
        
        # Degree information
        degrees = [self.graph.degree(v) for v in self.graph.nodes()]
        self.properties_text.insert(tk.END, f"Min degree: {min(degrees)}\n")
        self.properties_text.insert(tk.END, f"Max degree: {max(degrees)}\n")
        
        # Eulerian properties
        odd_vertices = [v for v in self.graph.nodes() if self.graph.degree(v) % 2 == 1]
        self.properties_text.insert(tk.END, f"Odd-degree vertices: {len(odd_vertices)}\n")
        
        if len(odd_vertices) == 0:
            self.properties_text.insert(tk.END, "→ Eulerian cycle possible\n")
        elif len(odd_vertices) == 2:
            self.properties_text.insert(tk.END, "→ Eulerian path possible\n")
        else:
            self.properties_text.insert(tk.END, "→ No Eulerian path/cycle\n")
            
        # Tree properties
        if nx.is_tree(self.graph):
            self.properties_text.insert(tk.END, "→ This is a tree\n")
            
        # Planarity check (simplified)
        if n_vertices >= 5 and n_edges > 3 * n_vertices - 6:
            self.properties_text.insert(tk.END, "→ Likely non-planar\n")
        else:
            self.properties_text.insert(tk.END, "→ May be planar\n")
            
    def update_insights(self, message):
        """Update the educational insights display"""
        self.insights_text.delete(1.0, tk.END)
        self.insights_text.insert(tk.END, message)

def main():
    """Main application entry point"""
    root = tk.Tk()
    app = GraphTheoryVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main() 