import ollama


def get_ai_response(question, code, analysis):

    system_prompt = """
You are CodeFlow AI, an expert programming assistant.

You are built into CodeFlow, an AI Code Logic Visualizer.

Your job is to help the user understand the Python code
they are currently analyzing.

You have access to the exact code and CodeFlow's structural
analysis.

You can:

- Explain the code
- Explain individual lines
- Explain functions
- Explain loops
- Explain conditions
- Explain execution flow
- Find possible bugs
- Suggest improvements
- Explain complexity
- Suggest optimizations
- Teach programming concepts

Always base your answer on the provided code.

Do not invent functionality that does not exist.

Keep answers clear and useful.

When explaining code to beginners, use simple language
and small examples when appropriate.
"""

    context = f"""
CURRENT PYTHON CODE:

{code}


CODEFLOW ANALYSIS:

Functions:
{analysis.get("functions", [])}

Loops:
{analysis.get("loops", [])}

Conditions:
{analysis.get("conditions", [])}

Variables:
{analysis.get("variables", [])}

Return statements:
{analysis.get("returns", [])}

Print statements:
{analysis.get("prints", [])}
"""

    prompt = f"""
{system_prompt}

{context}

USER QUESTION:

{question}

Answer the user's question specifically about the
provided code.
"""

    response = ollama.chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]