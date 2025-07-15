# 🗺️ GPS Navigator - Madrid Street Map

This project implements a graph-based GPS navigator that calculates the optimal route between two addresses in Madrid's street map using classic graph theory algorithms like **Dijkstra**.

---

## 👨‍💻 Authors

- **Jorge Ibinarriaga Robles**  
- **Miguel Ángel Huamani Salinas**  

---

## 📂 Project Structure

```
.
├── main.py              # Main console execution script
├── api.py               # FastAPI server for HTTP route queries
├── gps.py               # Navigation logic and routes
├── grafo.py             # Graph implementation and traversal algorithms
├── callejero.py         # Street data processing and graph construction
├── dgt_main.py          # Auxiliary functions for data cleaning and parsing
├── data/
│   ├── cruces.csv       # Street intersections dataset
│   └── direcciones.csv  # Addresses dataset
```

---

## 🧠 General Description

This program allows you to:

- Load a graph of Madrid's street map from real datasets of **intersections and addresses**.
- Calculate the **minimum route** between two points, based on distance or estimated time.
- Get step-by-step directions (GPS-style), including:
  - Turn right/left
  - Continue straight
  - Exit roundabouts
- Graphically visualize the graph and route using `NetworkX`.
- Query routes through a `REST API` (see below).

---

## 🔍 Main Features

### 📍 Module `gps.py`
- `distancia_entre_nodos`: Euclidean distance between two coordinates.
- `crear_grafo_distancia` and `crear_grafo_tiempo`: Construction of weighted graphs.
- `dibujar_grafo`, `dibujar_ruta`: Graph and route visualization.
- `encontrar_ruta_minima`: Minimum path calculation with Dijkstra.
- `dirigir_ruta`: Navigation instructions generation.

### 🧱 Module `grafo.py`
Contains the `Grafo` class with:
- Methods to add vertices/edges and query the structure.
- Algorithm implementations: `dijkstra`, `camino_minimo`, `prim`, `kruskal`.

### 🏙️ Module `callejero.py`
- Real dataset processing to unify nearby intersections.
- Entity modeling: `Cruce` and `Calle`.
- Graph creation from processed data.

---

## 🌐 REST API (FastAPI)

An HTTP API is also exposed to query routes programmatically.

### 🚀 Server execution:

```bash
python -m uvicorn api:app --port 8080 --log-level debug
```

### 📮 Endpoint `/ruta`

```
POST /ruta
```

**Body parameters (JSON):**

```json
{
  "origen": "Calle Del Príncipe de Vergara 291",
  "destino": "Calle Del Padre Damián 18",
  "modo": "S"  // or "T"
}
```

**Response:**

```json
{
  "ruta": [
    "Calle Del Príncipe de Vergara 291",
    "Avenida de América",
    "Calle Del Padre Damián 18"
  ]
}
```

---

## 📦 Requirements

- Python 3.11+
- pandas
- networkx
- matplotlib
- inquirer
- difflib (Python standard module)
- fastapi
- uvicorn

Quick installation:

```bash
pip install pandas networkx matplotlib inquirer fastapi uvicorn
```

---

## ▶️ Execution (console mode)

```bash
python main.py
```

The program will ask you to select origin and destination through the console with an autocomplete system like a navigator.

---

## 🧪 Example

- **Origin:** Calle de Alberto Aguilera 25
- **Destination:** Calle Del Padre Damián 18  

The optimal route will be displayed in the console with detailed step-by-step instructions.

---

## ⚠️ Considerations

- It is recommended to clean the datasets before execution (`dgt_main.py` handles part of the preprocessing).
- The `.csv` files contain special characters, make sure to use the correct encoding (`windows-1252` or `utf-8` depending on the case).
- Geometric approximations were used to unify nearby intersections like roundabouts.

---

## 📚 Bibliography

- **Graph theory:** Metro maps and neural networks, Claudi Alsina, 2012.
- **Introduction to Algorithms:** Cormen, Leiserson, Rivest, MIT Press, 1990.
- **Data Structures and Algorithms:** Aho, Hopcroft & Ullman, Pearson, 1998.
