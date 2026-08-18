# Data Analysis Agent with LangChain, Ollama & Streamlit

A beginner-friendly Data Analysis Agent that lets users upload a CSV file, explore data visually, and ask questions in natural language.

This project uses a free local Ollama model instead of a paid API. No OpenAI, Gemini, or Claude API key is required.

## Features

- Upload CSV datasets through a Streamlit web interface
- Preview uploaded data in an interactive table
- View dataset rows, columns, missing values, and data types
- Create bar charts, line charts, and histograms
- Ask questions about the uploaded dataset
- Use a LangChain agent with safe Python data-analysis tools
- Run a free local AI model using Ollama (`llama3.2:3b`)

## How It Works

```text
CSV File Upload
      ↓
Streamlit Dashboard
      ↓
Data Preview and Visualizations
      ↓
LangChain Agent
      ↓
Local Ollama Model
      ↓
Data Analysis Tools
      ↓
Final Answer
```

## Technologies Used

- Python 3.12
- Streamlit
- Pandas
- LangChain
- LangChain Ollama
- Ollama
- Llama 3.2 3B

## Project Structure

```text
data-analysis-agent/
├── .venv/              # Local virtual environment
├── .gitignore          # Files ignored by Git
├── app.py              # Streamlit dashboard and agent code
├── requirements.txt    # Required Python libraries
└── README.md           # Project documentation
```

## Installation

Create and activate a virtual environment:

```cmd
py -3.12 -m venv .venv
.venv\Scripts\activate
```

Install required Python libraries:

```cmd
python -m pip install -r requirements.txt
```

## Requirements

```text
streamlit
pandas
langchain
langchain-ollama
```

## Ollama Setup

Install Ollama from:

https://ollama.com/download/windows

Download the local model:

```cmd
ollama pull llama3.2:3b
```

Verify installed models:

```cmd
ollama list
```

## Run the Application

```cmd
python -m streamlit run app.py
```

Open the local Streamlit URL shown in the terminal, usually:

```text
http://localhost:8501
```

## Example Questions

```text
What is the total Sales for each Category?
```

```text
Show numeric statistics for this dataset.
```

```text
What are the top values in the Country column?
```

## Note

The agent uses predefined Python tools to analyze the uploaded CSV. It does not run arbitrary code, and answers should always be verified using the visible data table and charts.
