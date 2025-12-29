# 👕 Sistem Rekomendasi Outfit Harian Berbasis Web

### Berdasarkan Cuaca dan Tren Fashion Menggunakan Machine Learning

## 👥 Struktur Tim

Proyek ini dikerjakan oleh **5 orang** dengan pembagian peran sebagai berikut:

| No  | Peran                         | Jumlah  |
| --- | ----------------------------- | ------- |
| 1   | Machine Learning Engineer     | 2 orang |
| 2   | Web Developer (Frontend)      | 2 orang |
| 3   | Backend Engineer / Integrator | 1 orang |

---

## 🧠 Jobdesk Machine Learning Engineer

### 👤 ML Engineer 1 — Dataset & Preprocessing

**Fokus:** Pengolahan dan kesiapan data

**Tugas:**

- Mengumpulkan dataset publik:
  - Dataset outfit (fashion product)
  - Dataset tren fashion
  - Dataset cuaca
- Melakukan data cleaning:
  - Menghapus data kosong dan duplikat
  - Menyeragamkan kategori outfit
- Feature engineering:
  - Penyesuaian suhu dengan jenis outfit
  - Integrasi skor tren fashion
- Menyusun dataset akhir dalam format CSV
- Mendokumentasikan struktur dan deskripsi fitur dataset

**Output:**

- `dataset_final.csv`
- Dokumentasi fitur dataset

---

### 👤 ML Engineer 2 — Modeling & Evaluation

**Fokus:** Pembuatan dan evaluasi model rekomendasi

**Tugas:**

- Menentukan metode Machine Learning:
  - Content-Based Filtering
  - KNN / Cosine Similarity
- Melatih model menggunakan dataset final
- Melakukan evaluasi model:
  - Accuracy
  - Precision
  - Recall
- Menyimpan model dalam format `.pkl` atau `.joblib`
- Menyusun laporan hasil evaluasi model

**Output:**

- Model ML terlatih (`model.pkl`)
- Notebook training dan evaluasi
- Laporan performa model

---

## 🌐 Jobdesk Web Developer

### 👤 Web Developer 1 — UI/UX & Layout

**Fokus:** Tampilan dan desain antarmuka

**Tugas:**

- Mendesain UI website (wireframe & layout)
- Membuat halaman:
  - Input cuaca
  - Preferensi gaya berpakaian
  - Hasil rekomendasi outfit
- Implementasi frontend:
  - HTML, CSS, JavaScript
  - Responsive design
- Menampilkan visual outfit dan ikon cuaca

**Output:**

- Tampilan web siap pakai
- UI yang responsif dan user-friendly

---

### 👤 Web Developer 2 — Frontend Logic & UX

**Fokus:** Interaksi pengguna dan pengalaman pengguna

**Tugas:**

- Implementasi logika frontend:
  - Validasi input
  - Dropdown dan slider
- Integrasi API backend:
  - Mengambil hasil rekomendasi
- Menambahkan fitur UX:
  - Loading state
  - Error handling
- Menyimpan riwayat rekomendasi (localStorage)

**Output:**

- Frontend interaktif
- Integrasi API berjalan dengan baik

---

## 🔗 Jobdesk Backend Engineer / Integrator

### 👤 Backend Engineer

**Fokus:** Penghubung antara frontend dan model Machine Learning

**Tugas:**

- Membangun REST API menggunakan Flask atau FastAPI
- Endpoint utama:
  - `/predict` untuk rekomendasi outfit
- Memuat model Machine Learning ke backend
- Menangani preprocessing input dari frontend
- Mengirim hasil rekomendasi ke frontend dalam format JSON
- Dokumentasi endpoint API

**Output:**

- Backend API
- Dokumentasi REST API

---

## 🗂️ Struktur Folder Proyek

outfit-recommendation/
│
├── frontend/
│ ├── index.html
│ ├── css/
│ └── js/
│
├── backend/
│ ├── app.py
│ ├── model.pkl
│ └── utils.py
│
├── ml/
│ ├── dataset/
│ ├── preprocessing.ipynb
│ └── training.ipynb
│
└── docs/
└── laporan.pdf
