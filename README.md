# TFG

Repository for the **Final Degree Project** of **Jesús Núñez de Arenas Llamas**.  

This project explores **MetaCrew**, a system for generating and coordinating groups of AI agents that are evaluated on a variety of benchmarks.  

---

##  📂 Project Structure

```
TFG/
├── tfg/ # MetaCrew code and agent implementations
│   ├── src/
│   ├── output/
│   ├── storage/
│   └── README.md
├── Benchmarks/ # Benchmark definitions and crew outputs
│   ├── Crews/ # Benchmark crews
│   │   ├── codenames_crew/
│   │   ├── logic_crew/
│   │   ├── mmmu_crew/
│   │   ├── scienceworld_crew/
│   │   ├── travel_crew/
│   │   └── writing_crew/
│   └── Crews_creation/ # Files used to create the benchmark crews 
│   │   ├── output_codenames/
│   │   ├── output_logic/
│   │   ├── output_mmmu/
│   │   ├── output_scienceworld/
│   │   ├── output_travel/
│   │   └── output_writing/
└── README.md
```

---

## 🔹 Main Components  

### **tfg/**  
Contains the implementation of **MetaCrew**, the system responsible for generating new groups of agents. These agents are later evaluated against different benchmarks.  

### **Benchmarks/**  
Defines the evaluation tasks and holds the results of different crews when tackling them.  

- **Crews/** → Collections of agents specifically designed to solve each benchmark.  
- **Crews_creation/** → Raw outputs from MetaCrew used to construct each crew. Each folder corresponds to a different benchmark.  

---

## 🚀 How It Works  

1. **MetaCrew (`tfg/`)** generates agents with different skills and strategies.  
2. These agents are grouped into **crews** tailored to specific benchmarks.  
3. The crews are evaluated on the selected benchmarks in `Benchmarks/Crews/`.  

---

## 📌 Benchmarks Included  

- **Codenames Crew** – Word association and reasoning tasks.  
- **Logic Crew** – Symbolic and logical reasoning challenges.  
- **MMMU Crew** – Multi-modal understanding and reasoning.  
- **ScienceWorld Crew** – Scientific reasoning and problem solving.  
- **Travel Crew** – Planning and decision-making in travel scenarios.  
- **Writing Crew** – Creative and structured text generation.  

---

## ⚙️ Installation  

Clone the repository:  

```bash
git clone https://github.com/Jesus-Nunez-de-Arenas/MetaCrew.git
```

We are using Poetry to manage dependencies. You will need to install them separately in both the tfg/ folder (MetaCrew core) and each benchmark folder:

```bash
cd tfg
poetry install

cd ../Benchmarks/Crews/<Benchmark>
poetry install
```


## ▶️ Usage

### Run MetaCrew to generate agents:
```bash
cd tfg
poetry run run_crew
```

### Evaluate a crew on a benchmark:

```bash
cd Benchmarks/Crew/<benchmark>_crew
poetry run run_crew
```

### View results:

The outputs for each benchmark can be found in the output_\<benchmark\>.

# 📜 License

This project is licensed under the MIT License. See the LICENSE file for details.

