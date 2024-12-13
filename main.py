from llama_cpp import Llama

llm = Llama(
      model_path="llama-2-7b.Q3_K_L.gguf",
)
output = llm(
      "Q: What is 2+3? A: ", # Prompt
      max_tokens=32, # Generate up to 32 tokens, set to None to generate up to the end of the context window
      stop=["Q:", "\n"], # Stop generating just before the model would generate a new question
      echo=True # Echo the prompt back in the output
)
print(output)