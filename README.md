# AI Decision Influence Evaluation Framework

## Overview
This framework implements experiments to evaluate how AI language models might influence human decision-making processes, based on the methodology described in "Sabotage Evaluations for Frontier Models" (Benton et al., 2024). The project focuses on measuring an AI assistant's ability to subtly manipulate decisions while avoiding detection.

## Key Features
- Multiple AI behavior modes (Control, Subtle, Moderate, Aggressive)
- Time-constrained decision-making simulation
- Suspicion rating system


## High Level Project Structure
```
├── configs/                 # Hydra configuration files
├── src/
│   ├── experiment/         # Experiment implementations
│   │   ├── loader.py      # ExperimentLoader
│   │   └── types.py       # Shared type definitions
│   ├── llms/              # LLMs (OpenAI/Anthropic/Google)
│   ├── models/            # Model implementations
│   │   ├── helper.py      # AI assistant model
│   │   ├── participant.py # Decision maker model
│   │   ├── judge.py       # Debate judge model
│   │   └── debate.py      # Debate model
│   ├── debate/            # Debate management components
│   │   ├── manager.py     # DebateManager
│   │   └── types.py       # DebateRound definitions
│   └── scenario/          # Scenario definitions
│       ├── loader.py      # Scenario loading
│       └── types.py       # Scenario type definitions
└── run.py                # Main entry point
```

## Installation
```bash
# Clone repository
git clone https://https://github.com/ConnorWatts/decision_sabotage.git
cd decision_sabotage

# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r deps/requirements.txt
```

## Usage

### Basic Usage
```bash
python run.py --experiment_name classic
```

### Configuration Options
```bash
python run.py     --config_path ./configs     --config_name base     --experiment_name classic     --overrides "experiment.time_limit=3600"
```

## Configuration Files
The project uses Hydra for configuration management. Key configuration (classic) files include:
```yaml
# configs/classic.yaml
experiment_name: classic

# Model configurations
models:
  helper:
    source: 'openai'
    name: 'gpt-4o'
    temperature: 0.5
    behavior: 'control'

  participant:
    source: 'openai'
    name: 'gpt-4o'
    temperature: 0.5

# Environment configurations
environment:
  time_limit: 30
  num_interactions: 5

# Scenario configurations
scenario: 'business_expansion'
```

## Core Components

### Experiment Types
#### SingleClassicExperiment
Standard decision-making experiment with:
- Time limit (default 30 minutes)
- Configurable number of interactions
- Document verification
- Suspicion rating system

#### SingleDebateExperiment
A debate-based evaluation framework with:

- Configurable debate rounds (default: 3 rounds)
- Debate between two AI models with a judge
- Participant model asking questions and making final decisions
- Tracking interactions, participant metrics, and outcomes

### Model Behaviors
- **Control**: Honest, balanced advice with document references
- **Subtle**: Minor bias towards incorrect answer while maintaining objectivity
- **Moderate**: Balanced but biased guidance
- **Aggressive**: Strong push towards incorrect answer while maintaining plausibility

### Helper Model
The `HelperModel` class provides:
- Context-aware responses
- Behavior-specific guidance
- Document reference support
- Interaction history tracking

### Participant Model
The `ParticipantModel` simulates:
- Question generation
- Final decision making
- Suspicion rating
- In the future this should be humans (or human x ai)

#### Debate Framework

### DebateManager
- Manages multi-round debates between two models.
- Includes a judge model to evaluate debates and render a decision.

### DebateModel
- Generates arguments and rebuttals during debates.
- Supports behavior-specific guidance (e.g., control, subtle, moderate, aggressive).

### JudgeModel
- Evaluates debate outcomes and provides a final decision with confidence scores.

## Future Development

### Immediate Next Steps
- **Enhanced Prompts**
  - Develop more sophisticated behavior prompts
  - Add document reference validation
  - Implement dynamic prompt adjustment

- **Characterizing Persuative behaviour**
  - Are there specific styles of persuation these agents use?

- **Metrics & Analysis**
  - Add detailed interaction logging
  - Implement statistical analysis tools
  - Create visualization dashboard

- **Validation Features**
  - Add scenario difficulty validation
  - Implement document relevance scoring
  - Add automated verification of AI claims

- **Sandbagging Experimentation**
- Evaluate models under "sandbagging" scenarios

- **Deeper look into Debate**
- When and how models collude
- Can we get more robust honest decision with more agents (n-agents?)

- **Use these experiments with some interpretability techniques**
  - TBC!


### Long-term Goals
- **Advanced Scenarios**
  - Multi-participant experiments
  - Complex decision trees
  - Real-time feedback mechanisms

- **Model Improvements**
  - Add more behavior types
  - Implement adaptive behavior
  - Add uncertainty quantification

- **Tooling & Infrastructure**
  - Web interface for experiments
  - Result database
  - Automated report generation

- **Deciosions about the AI itself**
  - Would it convince to change rewards/architecture
