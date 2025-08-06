#!/usr/bin/env python3
"""
Test script for the Graph Theory Visualizer
"""

import sys
import traceback

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import tkinter as tk
        print("✓ tkinter imported successfully")
    except ImportError as e:
        print(f"✗ tkinter import failed: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✓ matplotlib imported successfully")
    except ImportError as e:
        print(f"✗ matplotlib import failed: {e}")
        return False
    
    try:
        import networkx as nx
        print("✓ networkx imported successfully")
    except ImportError as e:
        print(f"✗ networkx import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ numpy imported successfully")
    except ImportError as e:
        print(f"✗ numpy import failed: {e}")
        return False
    
    return True

def test_wilson_algorithms():
    """Test the Wilson algorithms module"""
    print("\nTesting Wilson algorithms module...")
    
    try:
        from graph_algorithms import WilsonGraphAlgorithms
        print("✓ WilsonGraphAlgorithms imported successfully")
        
        # Test algorithm initialization
        algorithms = WilsonGraphAlgorithms()
        print("✓ WilsonGraphAlgorithms initialized successfully")
        
        # Test learning progression
        progression = algorithms.get_learning_progression()
        print(f"✓ Learning progression has {len(progression)} stages")
        
        return True
    except Exception as e:
        print(f"✗ Wilson algorithms test failed: {e}")
        traceback.print_exc()
        return False

def test_graph_creation():
    """Test basic graph creation and operations"""
    print("\nTesting graph creation...")
    
    try:
        import networkx as nx
        
        # Create a simple graph
        G = nx.Graph()
        G.add_nodes_from([0, 1, 2, 3])
        G.add_edges_from([(0, 1), (1, 2), (2, 3), (3, 0)])
        
        print(f"✓ Created graph with {len(G.nodes())} vertices and {len(G.edges())} edges")
        
        # Test basic properties
        print(f"✓ Graph is connected: {nx.is_connected(G)}")
        print(f"✓ Graph is a tree: {nx.is_tree(G)}")
        
        # Test Eulerian properties
        odd_vertices = [v for v in G.nodes() if G.degree(v) % 2 == 1]
        print(f"✓ Odd-degree vertices: {len(odd_vertices)}")
        
        return True
    except Exception as e:
        print(f"✗ Graph creation test failed: {e}")
        traceback.print_exc()
        return False

def test_visualizer_components():
    """Test if visualizer components can be created"""
    print("\nTesting visualizer components...")
    
    try:
        import tkinter as tk
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import matplotlib.pyplot as plt
        
        # Create a simple tkinter window
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(6, 4))
        canvas = FigureCanvasTkAgg(fig, root)
        
        print("✓ Tkinter window created successfully")
        print("✓ Matplotlib figure created successfully")
        print("✓ Canvas created successfully")
        
        # Clean up
        plt.close(fig)
        root.destroy()
        
        return True
    except Exception as e:
        print(f"✗ Visualizer components test failed: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("Graph Theory Visualizer - Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_wilson_algorithms,
        test_graph_creation,
        test_visualizer_components
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
        print("\nTo run the application:")
        print("  python main.py          # Basic version")
        print("  python enhanced_main.py # Enhanced version")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 