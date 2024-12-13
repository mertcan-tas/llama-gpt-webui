from llama_cpp import Llama

llm = Llama(
    model_path="llama-2-7b.Q3_K_L.gguf",
    n_gpu_layers=-1,
    ctx_size=4096,
    temperature=0.01,
    top_p=0.9,
    max_tokens=128,
    stop=["\n", "Q:"],
    echo=False,
    verbose=False,
    seed=1234,
    model_kwargs={"use_fp16": True},
    generate_kwargs={"temperature": 0.01, "top_k": 50}
)
output = llm(
    "Q: Nigga? A: ",
    max_tokens=32
)
response_text = output['choices'][0]['text'].strip()

print(response_text)