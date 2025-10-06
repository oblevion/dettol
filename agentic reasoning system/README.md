# Agentic Reasoning System

This project implements a modular, agentic architecture for logic question answering:
- Decomposes complex logic questions
- Selects appropriate solving tools
- Executes and verifies subtasks
- Outputs transparent step-by-step reasoning
- Does NOT use advanced reasoning-heavy LLMs, per competition rules

## Setup

1. Install dependencies:  
   `pip install -r requirements.txt`

2. Run on sample question:  
   `python main.py`

## Structure

See `modules/` for code.  
See `datasets/logic_qa.json` for example questions.

## Extend

To expand reasoning, add new decomposition and verification modules, and build detailed symbolic logic parsing.
