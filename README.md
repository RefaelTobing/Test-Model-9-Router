# Test-Model-9-Router

Aplikasi untuk menguji kesehatan dan performa semua model AI yang tersedia di 9Router lokal.

## Deskripsi

Project ini berisi dua script Python untuk monitoring dan testing model AI:

- **test_9router.py** — Test dasar koneksi ke 9Router dan ping model pertama
- **test_all_model.py** — Test komprehensif semua model secara paralel (8 worker thread)

## Prerequisites

- Python 3.7+
- Library: `openai` (OpenAI Python client)

Instalasi:
```bash
pip install openai
```

## Konfigurasi

### 1. Ubah Base URL dan API Key

Edit `test_all_model.py` baris 12-15:

```python
client = OpenAI(
    base_url="http://localhost:20128/v1",  # Ubah port jika berbeda
    api_key="your-api-key-here"             # Ganti dengan API key Anda
)
```

**Catatan:**
- **base_url** — Sesuaikan dengan URL dan port 9Router Anda (default: `http://localhost:20128/v1`)
- **api_key** — Dapatkan dari dashboard 9Router atau setting provider Anda

Lakukan hal yang sama di `test_9router.py` baris 4-6.

## Cara Menjalankan

### Test Dasar (Single Model)
```bash
python test_9router.py
```
Output: Menampilkan daftar model dan test chat completion pada model pertama.

### Test Komprehensif (Semua Model)
```bash
python test_all_model.py
```

Output format:
```
Model di daftar: 5 | sudah tercatat: 0 | akan diuji sekarang: 5 (8 paralel)
Batas waktu: FAST <= 15 dtk, NORMAL <= 45 dtk, SLOW di atasnya, > 120 dtk = TIMEOUT

1/5] model-1                                OK           FAST 2.3s
2/5] model-2                                OK           NORMAL 28.5s
3/5] model-3                                BLOCKED      TIMEOUT
4/5] model-4                                EMPTY        balasan kosong
5/5] model-5                                OK           SLOW 65.2s
```

## Interpretasi Hasil

### Status
- **OK** — Model berhasil merespons
- **BLOCKED** — Model tidak bisa diakses (lihat detail)
- **EMPTY** — Model merespons tapi balasan kosong

### Detail (untuk status OK)
- **FAST** — Response dalam ≤15 detik
- **NORMAL** — Response dalam 15-45 detik
- **SLOW** — Response dalam >45 detik

### Detail (untuk status BLOCKED)
- **TIMEOUT** — Request timeout (>120 detik)
- **no_credit** — Quota atau balance habis
- **auth** — Masalah autentikasi/API key
- **invalid_model** — Model tidak ditemukan
- **error_api** — Error API lainnya

## Tips

1. **Jalankan test_9router.py dulu** untuk verifikasi koneksi sebelum test semua model
2. **Parallel execution** — test_all_model.py menggunakan 8 thread, sesuaikan di kode jika perlu
3. **Timeout** — Default 120 detik per request, ubah di parameter `timeout=120`
4. **Max tokens** — Setiap request set `max_tokens=5` untuk test cepat, sesuaikan jika perlu respons lebih panjang

## Troubleshooting

**Koneksi ditolak**
- Cek URL dan port 9Router sudah benar
- Verifikasi 9Router service berjalan

**Auth error**
- Cek API key sudah benar dan tidak expired
- Verifikasi key di dashboard 9Router

**Timeout pada semua model**
- Cek kecepatan jaringan ke 9Router
- Tingkatkan timeout jika jaringan lambat
