<div align="center">

  <h1>🤖 Robot Multi-Floor Pathfinding Simulator</h1>
  
  <p>
    <b>An Advanced Multi-Floor Pathfinding Visualization using A* Algorithm</b>
  </p>

  <p>
    <a href="https://www.python.org/">
      <img src="https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    </a>
    <a href="https://www.pygame.org/news">
      <img src="https://img.shields.io/badge/Pygame-CE-blueviolet?style=for-the-badge&logo=python&logoColor=white" alt="Pygame">
    </a>
    <a href="#">
      <img src="https://img.shields.io/badge/Status-Active-success?style=for-the-badge" alt="Status">
    </a>
    <a href="#">
      <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License">
    </a>
  </p>
  
  <br />
</div>

---

## 📖 About The Project

**Robot Pathfinding Simulator** is a sophisticated educational tool designed to visualize complex pathfinding algorithms in a multi-floor environment. Unlike traditional 2D grid solvers, this simulator introduces verticality with **Elevators** and **Stairs**, adding a layer of strategic cost analysis to the pathfinding process.

The "Robot" (Yellow agent) intelligently calculates the most efficient route from Point A to Point B, dynamically choosing between taking the fast elevator (which can skip floors) or the slower stairs (which must be traversed sequentially), all while avoiding user-defined obstacles.

### 🌟 Key Innovations

- **Vertical Navigation**: Seamless transitions between floors.
- **Cost-Aware Routing**: Smart decision making between Elevator vs. Stairs.
- **Dynamic UI**: Real-time interactions, animations, and visual feedback.

---

## 🚀 Key Features

- **🏢 Multi-Floor System**: Support for 2 to 6 floors, dynamically adjustable.
- **🧠 A\* Algorithm Engine**: Visualizes the node scanning process in real-time.
- **🎨 Interactive Canvas**:
  - **🧱 Walls**: Draw barriers to block paths.
  - **🟢 Start / 🔴 End**: draggable start and target points.
  - **🧽 Eraser**: Remove specific elements.
- **↕️ Strategic Movement**:
  - **Elevator (Central)**: Rapid vertical transport (Cost: 8).
  - **Stairs (Edges)**: Slower, floor-by-floor traversal (Cost: 12).
- **✨ Modern UI/UX**:
  - Dark theme with consistent color palettes.
  - Animated robot movement with trails.
  - Visual indicators for open/closed sets.

---

## 🛠️ Technology Stack

- **Language**: Python 3.x
- **Library**: `pygame` (rendering engine)
- **Concepts**: Graph Theory, A\* Search Algorithm, Object-Oriented Programming (OOP)

---

## 💻 Installation & Getting Started

### Prerequisites

Ensure you have Python installed on your system.

```bash
python --version
```

### Installation

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/sudostealth/Robot_MultiFloor_PathFinding_Simulator.git
    cd Robot_MultiFloor_PathFinding_Simulator
    ```

2.  **Install Dependencies**

    ```bash
    pip install pygame
    ```

3.  **Run the Simulator**
    ```bash
    python robot2.py
    ```

---

## 🎮 Usage Guide

1.  **Select a Tool**: Use the bottom control panel to select **Wall**, **Start**, or **End**.
2.  **Draw Elements**: Click on the grid.
    - Left-click to place Walls, Start, or End points.
    - Right-click to erase.
    - You can change the number of floors using the **+ / -** buttons.
3.  **Run Simulation**: Click the **▶️ Run** button.
4.  **Watch**: Observe the A\* algorithm scanning nodes (Orange/Turquoise) and finding the shortest path (Purple).
5.  **Reset**: Use **🗑️ Clear** to start over.

| Icon | Tool      | Description                         |
| :--: | :-------- | :---------------------------------- |
|  🧱  | **Wall**  | Creates impassable barriers.        |
|  🟢  | **Start** | Sets the robot's starting position. |
|  🔴  | **End**   | Sets the destination target.        |
|  🧽  | **Erase** | Removes walls or points.            |
|  ▶️  | **Run**   | Executes the pathfinding algorithm. |

---

## 🧩 Project Structure

The project is modularized for better maintainability:

```
📂 Project Root
├── 📄 robot2.py          # Main entry point. Handles game loop and event logic.
├── 📄 pathfinding.py     # Contains A* algorithm, Node class, and Heuristic logic.
├── 📄 ui_components.py   # UI elements: Buttons, Robot class, and Drawing functions.
└── 📄 config.py          # Configuration constants, Colors, and Dimensions.
```

---

## 🤓 Algorithm Details

### The A\* (A-Star) Approach

The robot uses the **A\* Search Algorithm**, which combines:

1.  **g(n)**: The cost from the start node to current node `n`.
2.  **h(n)**: The heuristic estimated cost from `n` to the target.

**Formula**: `f(n) = g(n) + h(n)`

### Heuristics & Costs

To create realistic behavior, different movement types have different "weights":

- **Horizontal/Vertical Move**: Cost **1**.
- **Elevator**: Cost **8** + `(floors_traveled * specialized_multiplier)`.
- **Stairs**: Cost **12** (Expensive! Robot avoids stairs unless necessary).

The Heuristic function (`h_score`) also adds a penalty for floor differences (Manhattan Distance + Floor Penalty), encouraging the robot to change floors only when efficient.

---

## 🔮 Future Improvements

- [ ] Dijkstra and BFS algorithm toggles.
- [ ] Diagonal movement support.
- [ ] Save/Load map configurations.
- [ ] 3D Visualization mode.

---

## 🤝 Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1.  Fork the Project
2.  Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the Branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

<div align="center">
  <p>Made with ❤️ by <b>Sazib</b></p>
</div>
