import os
from celery import shared_task
from llama_cpp import Llama

@shared_task
def chatMessage(prompt):
    try:
        # Şu anki dosyanın bulunduğu dizin
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Modelin tam yolu
        model_path = os.path.join(current_dir, "llama-2-7b.Q3_K_L.gguf")
        
        # Llama modelini yükle
        llm = Llama(
            model_path=model_path,  # Tam model yolu
            n_gpu_layers=10,
            ctx_size=4096,
            temperature=0.7,
            top_p=0.9,
            max_tokens=128,
            stop=["\n", "Q:"],
            echo=False,
            verbose=False,
            seed=1234,
            model_kwargs={"use_fp16": True},
            generate_kwargs={"temperature": 0.7, "top_k": 50}
        )

        # Prompt ile yanıt üret
        output = llm(f"Q: {prompt} A:", max_tokens=32)
        return output['choices'][0]['text'].strip()

    except Exception as e:
        # Hata durumunda loglama
        return f"Error while generating response: {str(e)}"