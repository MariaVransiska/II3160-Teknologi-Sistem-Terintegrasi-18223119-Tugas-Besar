# Tugas Besar II3160 Teknologi Sistem Terintegrasi
## Game Tracker - Performance Analytics API
API FastAPI sederhana untuk mengelola performa pemain berdasarkan match record, dengan autentikasi JWT dasar dan beberapa router konteks (performance, profile, leaderboard, notification).

## Deskripsi Repository:
Implementasi API berbasis FastAPI untuk mencatat dan menganalisis performa pemain game. 
Fitur Utama: 
- Ingest data pertandingan (kills, deaths, assists, score, accuracy, timestamp).
- Perhitungan KDA, akurasi, rata-rata skor, dan tren performa.
- Endpoint untuk mengambil ringkasan performa per pemain.
- Struktur modular dengan pemisahan domain, service, schema, dan router.
- Autentikasi JWT dasar untuk proteksi endpoint.

## Struktur Repository:
```
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
```

## Endpoint dan Deskripsi
- GET `/` (Root)
  - Menyediakan status API. Response: `{ "msg": "Game Tracker Performance Analytics API" }`
  - Sumber: `app/main.py`

- POST `/performance/ingest`
  - Input: `MatchIn` (match_id, player_id, game_name, kills, deaths, assists, score, accuracy, timestamp).
  - Proses: membuat/menemukan `PlayerPerformance`, menambah riwayat match, menghitung ulang `PerformanceSummary` (KDA, accuracy, avg_score, trend, win_rate), dan mengembalikan agregat terbaru.
  - Output: `PerformanceOut` berisi `player_id`, `summary` (mapping dari `PerformanceSummary` dan `KDA`), `last_updated`.
  - Sumber: `app/api/performance_router.py` -> `ingest_match`, `app/service/performance_service.py`.

- GET `/performance/performance/{player_id}`
  - Mengambil `PlayerPerformance` yang sudah teragregasi untuk `player_id` tertentu.
  - Output: `PerformanceOut` sama seperti di endpoint ingest.
  - Sumber: `app/api/performance_router.py` -> `get_performance`.

- GET `/profile/`
  - Stub untuk data profil pemain. Sumber: `app/api/player_profile_router.py`.

- GET `/leaderboard/`
  - Stub leaderboard. Sumber: `app/api/leaderboard_router.py`.

- GET `/notification/`
  - Stub notifikasi. Sumber: `app/api/notification_router.py`.

- POST `/auth/login`
  - Menghasilkan JWT untuk akses endpoint terlindungi.
  - Sumber: `app/auth/auth_router.py`, `app/auth/auth_service.py`.

## Cara Setup dan Run
(nanti dibuat)

Dokumen Laporan : 
