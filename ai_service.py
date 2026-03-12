from transformers import pipeline

# Load lightweight AI model
generator = pipeline("text-generation", model="distilgpt2")

def explain_code(code: str):
    prompt = f"Explain the following Python code in simple terms:\n{code}\nExplanation:"

    result = generator(prompt, max_length=200, num_return_sequences=1)

    return result[0]["generated_text"]