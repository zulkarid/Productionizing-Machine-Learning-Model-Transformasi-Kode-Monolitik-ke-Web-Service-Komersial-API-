## Anggota Kelompok

Kelompok 19 — DS-04-02

| Nama | NIM |
|------|-----|
| Rayhan Akbar Zulkarnaen | 103102400069 |
| Dhana Zeta Pangestu | 103102400064 |

# Olympic Medals Prediction API

API untuk memprediksi jumlah medali Olimpiade suatu negara, dibangun pakai FastAPI. Proyek ini awalnya cuma notebook biasa, terus di-refactor jadi web service yang bisa dipanggil dari aplikasi lain.

---

## Struktur File

```
├── main.py                 # server FastAPI, endpoint /predict ada di sini
├── predictor.py            # logic ML-nya, dipisah biar rapi
├── model.pkl               # hasil export model dari notebook
├── machine_learning.ipynb  # notebook asli buat eksplorasi & training
├── teams.csv               # dataset yang dipakai
└── README.md
```

---

## Dataset

`teams.csv` berisi data historis tim Olimpiade. Total **2144 baris** setelah data null di-drop.

Kolom yang tersedia: `team`, `country`, `year`, `events`, `athletes`, `age`, `height`, `weight`, `medals`, `prev_medals`, `prev_3_medals`

Yang dipakai buat prediksi cuma dua kolom karena korelasinya paling tinggi terhadap `medals`:

```
athletes       0.84
prev_medals    0.92
```

---

## Proses Training (machine_learning.ipynb)

Data dibagi berdasarkan tahun:
- Train: tahun < 2012 → 1609 baris
- Test: tahun ≥ 2012 → 405 baris

Model yang dipakai Linear Regression dari scikit-learn dengan fitur `athletes` dan `prev_medals`.

**MAE hasil evaluasi: 3.30 medali**

Beberapa contoh prediksi di test set:

| Negara | Atlet | Prev Medals | Aktual | Prediksi |
|--------|-------|-------------|--------|----------|
| USA 2012 | 689 | 317 | 248 | 285.21 |
| USA 2016 | 719 | 248 | 264 | 235.57 |
| IND 2012 | 95 | 3 | 6 | 6.92 |
| IND 2016 | 130 | 6 | 2 | 11.68 |

Setelah training, model di-export ke `model.pkl` pakai pickle:

```python
import pickle
with open('model.pkl', 'wb') as file:
    pickle.dump(reg, file)
```

---

## Instalasi

```bash
pip install fastapi uvicorn numpy scikit-learn
```

## Jalankan Server

```bash
uvicorn main:app --reload
```

Akses di `http://127.0.0.1:8000` — Swagger UI ada di `http://127.0.0.1:8000/docs`

---

## Endpoint

### POST `/predict`

Kirim dua parameter ini:

| Field | Tipe | Keterangan |
|-------|------|------------|
| `athletes` | number | jumlah atlet yang dikirim ke Olimpiade |
| `prev_medals` | number | medali yang didapat di Olimpiade sebelumnya |

**Request:**
```json
{
  "athletes": 250,
  "prev_medals": 30
}
```

**Response sukses:**
```json
{
  "status": "success",
  "predicted_medals": 28
}
```

**Response kalau parameter kurang:**
```json
{
  "status": "error",
  "message": "Data tidak lengkap! Parameter berikut wajib diisi: 'athletes'"
}
```

**Response kalau tipe data salah (ngirim teks ke kolom angka):**
```json
{
  "status": "error",
  "message": "Tipe data salah! Input 'athletes' dan 'prev_medals' harus berupa angka."
}
```

---

## Catatan Teknis

- Tipe input di `OlympicInput` sengaja dibuat `float | str` (bukan float doang) supaya request yang ngirim teks tidak langsung ditolak Pydantic — biar error handling di `predictor.py` yang nangani sendiri dengan pesan yang lebih informatif.
- Hasil prediksi yang negatif otomatis di-clamp ke 0, karena jumlah medali tidak mungkin minus.
- Instance `OlympicPredictor` dibuat sekali waktu server start, bukan tiap request, jadi model tidak perlu di-load ulang terus.