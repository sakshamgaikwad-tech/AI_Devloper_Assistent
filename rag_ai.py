from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="microsoft/phi-2",
    max_length=200
)

def generate_answer(question, context):

    prompt = f"""
You are an expert Python coding assistant.

Use the provided code context to answer the user's question.

Code Context:
{context}

User Question:
{question}

Provide a short and clear answer.
"""

    result = generator(prompt)

    output = result[:10]["generated_text"]

    if "Provide a short and clear answer." in output:
        output = output.split("Provide a short and clear answer.")[-1]

    return output.strip()