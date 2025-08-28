# TFG
Repository of the TFG of Jesús Núñez de Arenas Llamas

# Structure of the project

## Schema

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

## tfg crew

In the tfg folder we will encounter the code of MetaCrew. This code will be used to create the new group of agents that will tackle the different benchmarks.

## Benchamrks

In it we will encounter the different benchmarks, with its own crews created from the outputs of MetaCrew.

### Crews

Crews created to pass the different benchmarks.

### Crews_creation

Output of MetaCrew to create each one of the crews. Each crew represents a different benchmark.