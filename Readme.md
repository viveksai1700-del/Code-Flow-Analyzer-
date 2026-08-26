# CodeFlow AI

AI-powered Python code logic visualizer that analyzes source code, converts its structure into a visual execution flow, and provides an integrated AI assistant for understanding and improving code.

## Overview

CodeFlow AI helps developers and students understand how Python programs work without manually tracing every line.

It combines Python AST-based code analysis, visual logic flow generation, structural code insights, and a local AI assistant into one interactive Streamlit application.

## Features

### Code Analyzer

Automatically analyzes Python source code and detects:

- Functions
- Variables
- Conditions
- Loops
- Return statements
- Function calls
- Output statements

### Logic Flow Visualizer

Converts the structure of Python code into a visual execution flow, making complex logic easier to understand.

### AI Assistant

The integrated AI assistant can:

- Explain code
- Find potential bugs
- Trace execution logic
- Suggest optimizations
- Answer questions about the analyzed code

The assistant is designed to work with a locally running Qwen3 model.

### Code Insights

Provides structural metrics including:

- Lines of code
- Number of functions
- Number of loops
- Number of conditions
- Number of variables
- Complexity estimate
- Maintainability estimate
- Return statements
- Output statements

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web interface |
| Python AST | Code structure analysis |
| Qwen3 | Local AI assistant |
| HTML/CSS | UI and styling |

## Project Structure

codeflow-ai/
├── app.py
├── analyzer.py
├── ai_assistant.py
├── style.css
├── requirements.txt
└── README.md

## How It Works

Python Source Code
        ↓
   AST Parser
        ↓
Code Structure Analysis
        ↓
 ┌──────┴──────┐
 ↓             ↓
Logic Flow   Code Metrics
 ↓
AI Assistant
 ↓
Code Explanation

## Installation

### 1. Clone the repository

git clone https://github.com/YOUR-USERNAME/codeflow-ai.git

cd codeflow-ai

### 2. Create a virtual environment

python -m venv venv

### 3. Activate the virtual environment

Windows:

venv\Scripts\activate

### 4. Install dependencies

pip install -r requirements.txt

### 5. Set up the local AI model

CodeFlow's AI assistant uses a locally running Qwen3 model.

Make sure your local model service is running and that `ai_assistant.py` is configured to communicate with it.

### 6. Run the application

python -m streamlit run app.py

The application will open in your browser.

## Example

Given the following Python code:

def calculate_total(price, tax):
    total = price + (price * tax)

    if total > 100:
        print("Expensive")

    return total

CodeFlow can identify the function, variable assignment, condition, output statement, and return statement and represent the program logic visually.

## Why CodeFlow?

Understanding code is often harder than writing it.

CodeFlow bridges that gap by combining traditional program analysis with AI assistance in one interactive interface.

Instead of only showing the source code, CodeFlow helps answer:

"What is this program actually doing?"

## Future Improvements

- Support for additional programming languages
- Interactive flowchart nodes
- Step-by-step code execution
- Complexity visualization
- Code optimization suggestions
- AI-generated documentation
- Exportable flowcharts
- Improved AST analysis
- Syntax highlighting
- Code comparison

## Author

Built as a portfolio project exploring Python code analysis, visualization, and local AI integration.

## License

This project is available for educational and portfolio use.