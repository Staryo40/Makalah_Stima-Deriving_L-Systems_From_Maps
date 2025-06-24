# Tugas Makalah Stima - Deriving L-System Grammar from Real City Street Networks Using Pathfinding Algorithms   
Abstract: City street networks are inherently complex due to their organic and often unstructured development, influenced by geographic, historical, and planning factors. Modeling these networks accurately poses a significant challenge, both in terms of analytical complexity and computational cost. This paper explores am approach that combines uninformed pathfinding algorithms with Lindenmayer systems (L-systems) to simplify and compress complex urban networks into generative rule sets. Using blind search methods such as Breadth-First Search (BFS) and Depth-First Search (DFS), traversal patterns can be analyzed from real-world street layouts. These patterns are then encoded into compact, recursive L-system rules capable of regenerating the original network or extending it while preserving its underlying spatial logic. This technique offers data compression and enables lightweight generation of complex structures, making it ideal for applications in procedural content generation, simulation, and urban planning.

<p align="center">
<img src="https://github.com/user-attachments/assets/5fe3e8fa-ee8d-49df-8e65-b3d19ae52f38" alt="Example image comparison of original graph (left) and L-System generated graph (right)" width="700"/>
</p>
<p align="center">Comparison of original graph (left) and L-System generated graph (right) of Jakarta, Indonesia</p>

## Program Requirements
1. Python 
2. Conda (Miniconda or Anaconda)
## Environment Setup
Create a conda environment
```bash
conda env create -f environment.yml
conda activate geoenv
```
## Running the Program
After setup, be sure to activate the environment  
Run the following command to run the program
```bash
python src/main.py
```
## About The Creator
Nama: Aryo Wisanggeni  
NIM: 13523100  
Kelas: K02
