#!/usr/bin/env python3
"""
Enhanced Eulerian/Hamiltonian Path Visualizer
Inspired by Robin J. Wilson's "Introduction to Graph Theory"

This enhanced version integrates the Wilson algorithms module and provides
a more comprehensive educational experience with detailed explanations.
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import numpy as np
from typing import List, Tuple, Optional, Dict
import json
import os

# Import our Wilson algorithms module
from graph_algorithms import WilsonGraphAlgorithms

class EnhancedGraphTheoryVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Graph Theory Visualizer - Wilson's Approach")
        self.root.geometry("1600x1000")
        self.root.configure(bg='#f0f0f0')
        
        # Initialize Wilson algorithms
        self.wilson_algorithms = WilsonGraphAlgorithms()
        
        # Graph data structure
        self.graph = nx.Graph()
        self.vertices = {}  # {vertex_id: (x, y)}
        self.edges = []     # [(vertex1, vertex2), ...]
        self.current_path = []
        self.selected_vertex = None
        self.drawing_edge = False
        self.edge_start = None
        
        # Educational state
        self.current_concept = "Graph Basics"
        self.learning_stage = 1
        
        self.setup_ui()
        self.create_example_graphs()
        
    def setup_ui(self):
        """Create the enhanced user interface with educational focus"""
        
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top panel - Learning progression
        top_panel = ttk.Frame(main_frame)
        top_panel.pack(fill=tk.X, pady=(0, 10))
        
        # Title
        title_label = ttk.Label(top_panel, text="Enhanced Graph Theory Visualizer", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = ttk.Label(top_panel, text="Following Wilson's Educational Approach", 
                                  font=('Arial', 12, 'italic'))
        subtitle_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Learning stage selector
        stage_label = ttk.Label(top_panel, text="Learning Stage:", font=('Arial', 10, 'bold'))
        stage_label.pack(side=tk.RIGHT, padx=(0, 10))
        
        self.stage_var = tk.StringVar(value="1")
        stage_combo = ttk.Combobox(top_panel, textvariable=self.stage_var, 
                                  values=["1", "2", "3", "4", "5", "6"], 
                                  width=5, state="readonly")
        stage_combo.pack(side=tk.RIGHT)
        stage_combo.bind('<<ComboboxSelected>>', self.on_stage_change)
        
        # Content frame
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left panel - Educational content and controls
        left_panel = ttk.Frame(content_frame, width=350)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Current concept display
        concept_frame = ttk.LabelFrame(left_panel, text="Current Learning Focus", padding=10)
        concept_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.concept_label = ttk.Label(concept_frame, text="Graph Basics", 
                                      font=('Arial', 12, 'bold'))
        self.concept_label.pack()
        
        self.concept_desc = ttk.Label(concept_frame, text="Learn about vertices, edges, and basic graph structure", 
                                     wraplength=330, justify=tk.LEFT)
        self.concept_desc.pack(pady=(5, 0))
        
        # Wilson's insights
        insights_frame = ttk.LabelFrame(left_panel, text="Wilson's Key Insights", padding=10)
        insights_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.insights_text = scrolledtext.ScrolledText(insights_frame, height=4, width=40, 
                                                      font=('Arial', 9), wrap=tk.WORD)
        self.insights_text.pack(fill=tk.BOTH, expand=True)
        
        # Graph creation controls
        creation_frame = ttk.LabelFrame(left_panel, text="Graph Creation", padding=10)
        creation_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(creation_frame, text="Add Vertex Mode", 
                  command=self.toggle_vertex_mode).pack(fill=tk.X, pady=2)
        ttk.Button(creation_frame, text="Add Edge Mode", 
                  command=self.toggle_edge_mode).pack(fill=tk.X, pady=2)
        ttk.Button(creation_frame, text="Clear Graph", 
                  command=self.clear_graph).pack(fill=tk.X, pady=2)
        
        # Analysis controls
        analysis_frame = ttk.LabelFrame(left_panel, text="Graph Analysis", padding=10)
        analysis_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(analysis_frame, text="Analyze Eulerian Properties", 
                  command=self.analyze_eulerian).pack(fill=tk.X, pady=2)
        ttk.Button(analysis_frame, text="Find Eulerian Path", 
                  command=self.find_eulerian_path).pack(fill=tk.X, pady=2)
        ttk.Button(analysis_frame, text="Analyze Hamiltonian Properties", 
                  command=self.analyze_hamiltonian).pack(fill=tk.X, pady=2)
        ttk.Button(analysis_frame, text="Find Hamiltonian Path", 
                  command=self.find_hamiltonian_path).pack(fill=tk.X, pady=2)
        ttk.Button(analysis_frame, text="Analyze Connectivity", 
                  command=self.analyze_connectivity).pack(fill=tk.X, pady=2)
        ttk.Button(analysis_frame, text="Analyze Tree Properties", 
                  command=self.analyze_tree).pack(fill=tk.X, pady=2)
        ttk.Button(analysis_frame, text="Clear Path", 
                  command=self.clear_path).pack(fill=tk.X, pady=2)
        
        # Example graphs
        example_frame = ttk.LabelFrame(left_panel, text="Educational Examples", padding=10)
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
        ttk.Button(example_frame, text="Disconnected Graph", 
                  command=lambda: self.load_example("disconnected")).pack(fill=tk.X, pady=2)
        
        # Graph properties
        properties_frame = ttk.LabelFrame(left_panel, text="Graph Properties", padding=10)
        properties_frame.pack(fill=tk.BOTH, expand=True)
        
        self.properties_text = scrolledtext.ScrolledText(properties_frame, height=8, width=40, 
                                                        font=('Courier', 9), wrap=tk.WORD)
        self.properties_text.pack(fill=tk.BOTH, expand=True)
        
        # Right panel - Graph visualization
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Graph canvas
        self.fig, self.ax = plt.subplots(figsize=(12, 9))
        self.canvas = FigureCanvasTkAgg(self.fig, right_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Bind mouse events
        self.canvas.mpl_connect('button_press_event', self.on_canvas_click)
        self.canvas.mpl_connect('motion_notify_event', self.on_canvas_motion)
        self.canvas.mpl_connect('button_release_event', self.on_canvas_release)
        
        # Initialize display
        self.update_display()
        self.update_properties()
        self.update_insights("Welcome to Enhanced Graph Theory! This tool follows Robin J. Wilson's educational approach, emphasizing visual learning and intuitive understanding.")
        
    def create_example_graphs(self):
        """Create pre-built example graphs for learning"""
        self.examples = {
            "simple_cycle": {
                "name": "Simple Cycle",
                "description": "A basic cycle graph - every vertex has degree 2",
                "vertices": [(0, 0), (1, 1), (2, 0), (1, -1)],
                "edges": [(0, 1), (1, 2), (2, 3), (3, 0)],
                "insight": "This is a simple cycle - notice how every vertex has exactly 2 edges. This is a fundamental structure in graph theory.",
                "stage": 1
            },
            "eulerian": {
                "name": "Eulerian Graph",
                "description": "A graph with an Eulerian cycle - all vertices have even degree",
                "vertices": [(0, 0), (1, 1), (2, 0), (1, -1), (0.5, 0.5)],
                "edges": [(0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (1, 4), (2, 4), (3, 4)],
                "insight": "This graph has an Eulerian cycle because every vertex has even degree. You can trace every edge exactly once and return to the start.",
                "stage": 4
            },
            "hamiltonian": {
                "name": "Hamiltonian Graph", 
                "description": "A graph with a Hamiltonian cycle - visits every vertex exactly once",
                "vertices": [(0, 0), (1, 1), (2, 0), (1, -1)],
                "edges": [(0, 1), (1, 2), (2, 3), (3, 0), (0, 2), (1, 3)],
                "insight": "This graph has a Hamiltonian cycle - you can visit every vertex exactly once and return to the start. Notice the additional edges that make this possible.",
                "stage": 5
            },
            "tree": {
                "name": "Tree",
                "description": "A connected acyclic graph - no cycles, connected",
                "vertices": [(0, 0), (1, 1), (1, -1), (2, 0.5), (2, -0.5)],
                "edges": [(0, 1), (0, 2), (1, 3), (2, 4)],
                "insight": "This is a tree - it's connected (you can reach any vertex from any other) but has no cycles. Trees are fundamental structures in computer science.",
                "stage": 3
            },
            "k5": {
                "name": "Complete Graph K5",
                "description": "A non-planar graph - cannot be drawn without edge crossings",
                "vertices": [(0, 0), (1, 1), (2, 0), (1, -1), (0.5, 0)],
                "edges": [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)],
                "insight": "This is K5, the complete graph on 5 vertices. It's non-planar - you cannot draw it without edges crossing. This is a key result in graph theory.",
                "stage": 6
            },
            "disconnected": {
                "name": "Disconnected Graph",
                "description": "A graph with multiple components",
                "vertices": [(0, 0), (1, 1), (2, 0), (3, 1), (4, 0)],
                "edges": [(0, 1), (1, 2), (3, 4)],
                "insight": "This graph has two separate components. You cannot reach vertices 3 and 4 from vertices 0, 1, and 2. This demonstrates the concept of connectivity.",
                "stage": 2
            }
        }
        
    def on_stage_change(self, event=None):
        """Handle learning stage changes"""
        stage = int(self.stage_var.get())
        self.learning_stage = stage
        
        # Get learning progression
        progression = self.wilson_algorithms.get_learning_progression()
        if stage <= len(progression):
            current_stage = progression[stage - 1]
            self.concept_label.config(text=current_stage["title"])
            self.concept_desc.config(text=current_stage["description"])
            
            # Update insights based on stage
            stage_insights = {
                1: "Start with the basics: vertices (points) and edges (lines connecting points). This is the foundation of all graph theory.",
                2: "Connectivity is crucial - can you reach every vertex from every other vertex? This determines many properties of the graph.",
                3: "Trees are special: connected graphs with no cycles. They're like the 'skeleton' of connected graphs.",
                4: "Eulerian paths traverse every edge exactly once. The key insight is counting the number of edges at each vertex.",
                5: "Hamiltonian paths visit every vertex exactly once. This is much harder than Eulerian paths - no simple condition exists!",
                6: "Advanced concepts like planarity, coloring, and matching build on the fundamentals you've learned."
            }
            
            if stage in stage_insights:
                self.update_insights(stage_insights[stage])
            
    def toggle_vertex_mode(self):
        """Toggle vertex creation mode"""
        messagebox.showinfo("Vertex Mode", "Click anywhere on the canvas to add vertices!\n\nWilson's Insight: Vertices are the fundamental building blocks of graphs. Think of them as locations or objects.")
        
    def toggle_edge_mode(self):
        """Toggle edge creation mode"""
        messagebox.showinfo("Edge Mode", "Click and drag between vertices to create edges!\n\nWilson's Insight: Edges represent relationships or connections between vertices. They define the structure of the graph.")
        
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
        self.update_insights("Graph cleared. Start building a new graph to explore graph theory concepts!")
        
    def clear_path(self):
        """Clear the current path display"""
        self.current_path = []
        self.update_display()
        
    def analyze_eulerian(self):
        """Analyze Eulerian properties using Wilson's approach"""
        if len(self.graph.nodes()) == 0:
            messagebox.showwarning("No Graph", "Please create a graph first!")
            return
            
        analysis = self.wilson_algorithms.analyze_eulerian_properties(self.graph)
        
        # Display detailed analysis
        analysis_text = f"EULERIAN ANALYSIS\n{'='*50}\n\n"
        analysis_text += f"Has Eulerian Path: {analysis['has_eulerian_path']}\n"
        analysis_text += f"Has Eulerian Cycle: {analysis['has_eulerian_cycle']}\n\n"
        analysis_text += f"Reason: {analysis['reason']}\n\n"
        analysis_text += f"Explanation: {analysis['explanation']}\n\n"
        analysis_text += f"Wilson's Insight: {analysis['wilson_insight']}\n\n"
        
        if 'degrees' in analysis:
            analysis_text += "Vertex Degrees:\n"
            for vertex, degree in analysis['degrees'].items():
                analysis_text += f"  Vertex {vertex}: {degree}\n"
        
        self.update_insights(analysis_text)
        
    def find_eulerian_path(self):
        """Find Eulerian path using Wilson's algorithm"""
        if len(self.graph.nodes()) == 0:
            messagebox.showwarning("No Graph", "Please create a graph first!")
            return
            
        path = self.wilson_algorithms.find_eulerian_path(self.graph)
        
        if path:
            self.current_path = path
            self.update_display()
            self.update_insights("Eulerian path found and highlighted! This path traverses every edge exactly once.")
        else:
            analysis = self.wilson_algorithms.analyze_eulerian_properties(self.graph)
            self.update_insights(f"No Eulerian path exists.\n\nReason: {analysis['reason']}\n\nExplanation: {analysis['explanation']}")
            
    def analyze_hamiltonian(self):
        """Analyze Hamiltonian properties using Wilson's approach"""
        if len(self.graph.nodes()) == 0:
            messagebox.showwarning("No Graph", "Please create a graph first!")
            return
            
        analysis = self.wilson_algorithms.analyze_hamiltonian_properties(self.graph)
        
        # Display detailed analysis
        analysis_text = f"HAMILTONIAN ANALYSIS\n{'='*50}\n\n"
        analysis_text += f"Wilson's Insight: {analysis['wilson_insight']}\n\n"
        analysis_text += f"Difficulty: {analysis['difficulty']}\n\n"
        
        if 'dirac_condition' in analysis:
            analysis_text += f"Dirac's Theorem: {analysis['dirac_explanation']}\n\n"
        
        if 'ore_condition' in analysis:
            analysis_text += f"Ore's Theorem: {analysis['ore_explanation']}\n\n"
        
        self.update_insights(analysis_text)
        
    def find_hamiltonian_path(self):
        """Find Hamiltonian path using Wilson's algorithm"""
        if len(self.graph.nodes()) == 0:
            messagebox.showwarning("No Graph", "Please create a graph first!")
            return
            
        path = self.wilson_algorithms.find_hamiltonian_path_simple(self.graph)
        
        if path:
            self.current_path = path
            self.update_display()
            self.update_insights("Hamiltonian path found and highlighted! This path visits every vertex exactly once.")
        else:
            self.update_insights("No Hamiltonian path found. This is a complex problem - no efficient algorithm exists for all graphs. Try a different graph structure!")
            
    def analyze_connectivity(self):
        """Analyze connectivity using Wilson's approach"""
        if len(self.graph.nodes()) == 0:
            messagebox.showwarning("No Graph", "Please create a graph first!")
            return
            
        analysis = self.wilson_algorithms.analyze_connectivity(self.graph)
        
        # Display detailed analysis
        analysis_text = f"CONNECTIVITY ANALYSIS\n{'='*50}\n\n"
        analysis_text += f"Is Connected: {analysis['is_connected']}\n\n"
        analysis_text += f"Explanation: {analysis['explanation']}\n\n"
        analysis_text += f"Wilson's Insight: {analysis['wilson_insight']}\n\n"
        
        if not analysis['is_connected'] and 'components' in analysis:
            analysis_text += f"Components: {analysis['component_count']}\n"
            for i, component in enumerate(analysis['components']):
                analysis_text += f"  Component {i+1}: {list(component)}\n"
        elif analysis['is_connected'] and 'articulation_points' in analysis:
            if analysis['has_articulation_points']:
                analysis_text += f"Articulation Points: {analysis['articulation_points']}\n"
                analysis_text += f"Explanation: {analysis['articulation_explanation']}\n"
            else:
                analysis_text += f"Explanation: {analysis['articulation_explanation']}\n"
        
        self.update_insights(analysis_text)
        
    def analyze_tree(self):
        """Analyze tree properties using Wilson's approach"""
        if len(self.graph.nodes()) == 0:
            messagebox.showwarning("No Graph", "Please create a graph first!")
            return
            
        analysis = self.wilson_algorithms.analyze_tree_properties(self.graph)
        
        # Display detailed analysis
        analysis_text = f"TREE ANALYSIS\n{'='*50}\n\n"
        analysis_text += f"Is Tree: {analysis['is_tree']}\n\n"
        analysis_text += f"Wilson's Insight: {analysis['wilson_insight']}\n\n"
        
        if analysis['is_tree']:
            analysis_text += f"Explanation: {analysis['explanation']}\n\n"
            analysis_text += f"Tree Property: {analysis['tree_property']}\n"
            analysis_text += f"Explanation: {analysis['tree_property_explanation']}\n\n"
            analysis_text += f"Leaves: {analysis['leaves']}\n"
            analysis_text += f"Leaf Count: {analysis['leaf_count']}\n"
            analysis_text += f"Explanation: {analysis['leaf_explanation']}\n"
        else:
            analysis_text += f"Reason: {analysis['reason']}\n"
            analysis_text += f"Explanation: {analysis['explanation']}\n"
        
        self.update_insights(analysis_text)
        
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
            
        # Update stage if example has a specific stage
        if "stage" in example:
            self.stage_var.set(str(example["stage"]))
            self.on_stage_change()
            
        self.update_display()
        self.update_properties()
        self.update_insights(example["insight"])
        
    def update_display(self):
        """Update the graph visualization"""
        self.ax.clear()
        
        # Set up the plot
        self.ax.set_xlim(-0.5, 4.5)
        self.ax.set_ylim(-1.5, 1.5)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title("Interactive Graph Visualization - Wilson's Approach", 
                         fontsize=14, fontweight='bold')
        
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
        
        self.properties_text.insert(tk.END, f"BASIC PROPERTIES\n{'='*30}\n")
        self.properties_text.insert(tk.END, f"Vertices: {n_vertices}\n")
        self.properties_text.insert(tk.END, f"Edges: {n_edges}\n")
        self.properties_text.insert(tk.END, f"Connected: {nx.is_connected(self.graph)}\n\n")
        
        # Degree information
        degrees = [self.graph.degree(v) for v in self.graph.nodes()]
        self.properties_text.insert(tk.END, f"DEGREE ANALYSIS\n{'='*30}\n")
        self.properties_text.insert(tk.END, f"Min degree: {min(degrees)}\n")
        self.properties_text.insert(tk.END, f"Max degree: {max(degrees)}\n")
        self.properties_text.insert(tk.END, f"Average degree: {sum(degrees)/len(degrees):.2f}\n\n")
        
        # Eulerian properties
        odd_vertices = [v for v in self.graph.nodes() if self.graph.degree(v) % 2 == 1]
        self.properties_text.insert(tk.END, f"EULERIAN ANALYSIS\n{'='*30}\n")
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
    app = EnhancedGraphTheoryVisualizer(root)
    root.mainloop()

if __name__ == "__main__":
    main() 