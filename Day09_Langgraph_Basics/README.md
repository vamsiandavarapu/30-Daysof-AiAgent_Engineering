# Day 9: LangGraph Basics

These examples introduce LangGraph by building small stateful workflows, adding conditional routing, and connecting a graph node to a Groq chat model.

## Examples

- `01_basic_langgraph.py` — a sequential graph that adds two numbers and then doubles the result.
- `02_conditional_langgraph.py` — routes a number to an even or odd result.
- `03_langgraph_qna.py` — sends a question through a LangGraph node and prints the model's answer.

## Requirements

- Python 3.10 or later
- A Groq API key to run the Q&A example

Install the packages from a terminal:

```powershell
python -m pip install langgraph langchain-groq python-dotenv
```

## Run the examples

From this directory, run any example:

```powershell
python 01_basic_langgraph.py
python 02_conditional_langgraph.py
python 03_langgraph_qna.py
```

The first two examples run locally. The Q&A example needs `GROQ_API_KEY` set in the environment or in a `.env` file in this directory:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

The Q&A program accepts questions until you type `exit` or `quit`. Keep API keys private and do not commit `.env` files.
