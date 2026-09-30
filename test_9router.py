from openai import OpenAI

# Inisialisasi client ke 9Router lokal
client = OpenAI(
    base_url="http://localhost:20128/v1",
    api_key="sk-7ac57b36ea47ff09-0tgtoq-b50eac8c" 
)

def test_models():
    print("Mencari daftar model di 9Router...")
    try:
        # Menarik daftar semua model yang aktif di 9Router
        models = client.models.list()
        model_ids = [model.id for model in models.data]
        
        print(f"Total model ditemukan: {len(model_ids)}")
        print(f"Contoh model: {model_ids[:5]}\n")
        
        # Eksekusi test ping ke model pertama dalam daftar
        if len(model_ids) > 0:
            target_model = model_ids[0]
            print(f"--- Memulai test chat pada model: {target_model} ---")
            
            response = client.chat.completions.create(
                model=target_model,
                messages=[
                    {"role": "user", "content": "Halo! Tolong balas dengan kata 'Test Berhasil'."}
                ],
                max_tokens=20
            )
            
            print("\nBalasan:")
            print(response.choices[0].message.content)
            
    except Exception as e:
        print(f"Terjadi error: {e}")

if __name__ == "__main__":
    test_models()
