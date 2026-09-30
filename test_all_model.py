import time
import concurrent.futures
from openai import OpenAI

# Konfigurasi warna untuk terminal
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'

# Inisialisasi client OpenAI ke 9Router lokal
client = OpenAI(
    base_url="BASE URL 9ROUTER DIHALAMAN ENDPOINT & KEY BAGIAN Local",
    api_key="API KEY 9ROUTER DIHALAMAN ENDPOINT & KEY BAGIAN APIKEYS"
)

# Fungsi untuk menguji satu model (akan dijalankan oleh masing-masing thread)
def test_single_model(idx, total, model_id):
    start_time = time.time()
    status_text = ""
    status_color = ""
    detail_text = ""
    detail_color = ""
    
    try:
        response = client.chat.completions.create(
            model=model_id,
            messages=[{"role": "user", "content": "Hi"}],
            max_tokens=5,
            timeout=120
        )
        
        elapsed = time.time() - start_time
        content = response.choices[0].message.content
        
        if not content or content.strip() == "":
            status_text, status_color = "EMPTY", YELLOW
            detail_text, detail_color = "balasan kosong", YELLOW
        else:
            status_text, status_color = "OK", GREEN
            if elapsed <= 15:
                speed = "FAST"
            elif elapsed <= 45:
                speed = "NORMAL"
            else:
                speed = "SLOW"
            detail_text, detail_color = f"{speed} {elapsed:.1f}s", GREEN
            
    except Exception as e:
        err_msg = str(e).lower()
        status_text, status_color = "BLOCKED", RED
        
        if "timeout" in err_msg:
            detail_text = "TIMEOUT"
        elif "credit" in err_msg or "quota" in err_msg or "balance" in err_msg:
            detail_text = "no_credit"
        elif "auth" in err_msg or "key" in err_msg or "unauthorized" in err_msg:
            detail_text = "auth"
        elif "invalid" in err_msg or "not found" in err_msg:
            detail_text = "invalid_model"
        else:
            detail_text = "error_api"
        
        detail_color = RED

    # Formatting string output
    prefix = f"{idx}/{total}] {model_id}"
    formatted_status = f"{status_color}{status_text.ljust(11)}{RESET}"
    formatted_detail = f"{detail_color}{detail_text}{RESET}"
    
    return f"{prefix.ljust(50)} {formatted_status} {formatted_detail}"

def main():
    try:
        models_response = client.models.list()
        model_ids = [m.id for m in models_response.data]
    except Exception as e:
        print(f"Gagal mengambil daftar model dari 9Router: {e}")
        return

    total = len(model_ids)
    
    print(f"Model di daftar: {total} | sudah tercatat: 0 | akan diuji sekarang: {total} (8 paralel)")
    print("Batas waktu: FAST <= 15 dtk, NORMAL <= 45 dtk, SLOW di atasnya, > 120 dtk = TIMEOUT\n")

    # Menggunakan ThreadPoolExecutor untuk menjalankan 8 proses sekaligus
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        # Submit semua tugas ke executor
        futures = {
            executor.submit(test_single_model, idx, total, model_id): model_id 
            for idx, model_id in enumerate(model_ids, 1)
        }
        
        # Cetak hasil secara real-time setiap kali ada satu thread yang selesai
        for future in concurrent.futures.as_completed(futures):
            print(future.result())

if __name__ == "__main__":
    main()
