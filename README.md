# Tugas Besar II3160 Teknologi Sistem Terintegrasi
## Game Tracker - Performance Analytics API
API FastAPI sederhana untuk mengelola performa pemain berdasarkan match record, dengan autentikasi JWT dasar dan beberapa router konteks (performance, profile, leaderboard, notification).

## Daftar Isi 


## Deskripsi Repository:
Implementasi API berbasis FastAPI untuk mencatat dan menganalisis performa pemain game. 
Fitur Utama: 
- Ingest data pertandingan (kills, deaths, assists, score, accuracy, timestamp).
- Perhitungan KDA, akurasi, rata-rata skor, dan tren performa.
- Endpoint untuk mengambil ringkasan performa per pemain.
- Struktur modular dengan pemisahan domain, service, schema, dan router.
- Autentikasi JWT dasar untuk proteksi endpoint.

## Struktur Repository:
app/
│── main.py
│
├── api/
│   ├── performance_router.py
│   ├── player_profile_router.py
│   ├── leaderboard_router.py
│   ├── notification_router.py
│
├── auth/
│   ├── auth_router.py
│   ├── auth_service.py
│
├── domain/
│   ├── events.py
│   ├── kda.py
│   ├── performance_summary.py
│   ├── performance_updated.py
│   ├── player_id.py
│   ├── player_performance.py
│   ├── match_record.py
│   ├── metric.py
│
├── service/
│   ├── performance_service.py
│
└── schema/
    ├── performance_schemas.py

## Cara Setup dan Run
(nanti dibuat)

Dokumen Laporan : 
