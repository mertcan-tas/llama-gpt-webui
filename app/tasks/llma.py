from celery import shared_task
from django.conf import settings
from llama_cpp import Llama

@shared_task
def chatMessage(prompt):
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
        "Q: {} A: ".format(prompt),
        max_tokens=32
    )
    return output['choices'][0]['text'].strip()
