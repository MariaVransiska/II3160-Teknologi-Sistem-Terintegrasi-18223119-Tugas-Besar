![CI Status](https://github.com/MariaVransiska/II3160-Teknologi-Sistem-Terintegrasi-18223119-Tugas-Besar/actions/workflows/ci.yml/badge.svg)

# Tugas Besar II3160 Teknologi Sistem Terintegrasi
Nama  : Maria Vransiska Pingkhan
NIM   : 18223119 

## Game Tracker - Performance Analytics API
API FastAPI sederhana untuk mengelola performa pemain berdasarkan match record, dengan autentikasi JWT dasar dan beberapa router konteks (performance, profile, leaderboard, notification).

## Deskripsi Repository:
Implementasi API berbasis FastAPI untuk mencatat dan menganalisis performa pemain game. 
Fitur Utama: 
- Ingest data pertandingan (kills, deaths, assists, score, accuracy, timestamp).
- Perhitungan KDA, akurasi, rata-rata skor, dan tren performa.
- Endpoint untuk mengambil ringkasan performa per pemain.
- Struktur modular dengan pemisahan domain, service, schema, dan router.
- Autentikasi JWT dasar untuk proteksi endpoint performance dan token user.
- Membuat profil baru, update profil, delete profil.
- Menambahkan notifikasi, menghapus notifikasi. 
- Melihat leaderboard player.

## Struktur Repository:
```
app/
├── __init__.py
├── main.py
├── api/
│   ├── performance_router.py
│   ├── player_profile_router.py
│   ├── leaderboard_router.py
│   └── notification_router.py   
│
├── auth/
│   ├── auth_router.py
│   └── auth_service.py
│
├── domain/
│   ├── __init__.py
│   ├── events.py
│   ├── kda.py
│   ├── performance_summary.py
│   ├── performance_updated.py
│   ├── player_id.py
│   ├── player_performance.py
│   ├── match_record.py
│   ├── metric.py                    # TODO:  VO belum dipakai
│   ├── external_player_id.py        # TODO:  VO belum dipakai
│   └── external_game_account.py     # TODO:  VO belum dipakai
│
├── service/
│   └── performance_service.py
│
├── schema/
│   ├── performance_schemas.py
│   ├── leaderboard_schemas.py
│   └── profile_schemas.py
│
tests/
    └── test_api.py 
.coveragerc                       
pytest.ini
requirements.txt  
README.md                          
```

## Cara Setup dan Run
1. Install dependencies: pip3 install -r requirements.txt
2. Test: python3 -m pytest
3. Run server: python3 -m uvicorn app.main:app –reload
4. URL Swagger: http://localhost:8000/docs {local}
5. URL Deploy: https://gametracker-mar.vercel.app/docs 

## Checklist
- [x] CI (lint + test + docker build)
- [x] Coverage ≥95%
- [x] Deploy online (Vercel) → https://gametracker-mar.vercel.app/docs 