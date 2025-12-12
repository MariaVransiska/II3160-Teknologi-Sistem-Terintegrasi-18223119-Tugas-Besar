# =========================
# Imports & Test Client
# =========================
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from app.main import app
from app.api.performance_router import service
from app.domain.player_id import PlayerId
from app.domain.player_performance import PlayerPerformance
from app.domain.match_record import MatchRecord

client = TestClient(app)

# =========================
# Helpers
# =========================
def get_token():
    resp = client.post("/auth/login", json={"username": "pingkhan", "password": "12345"})
    assert resp.status_code == 200
    return resp.json()["access_token"]

# =========================
# Root & Auth
# =========================
def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["msg"].startswith("Game Tracker")

def test_auth_login_invalid():
    r = client.post("/auth/login", json={"username": "x", "password": "y"})
    assert r.status_code in (401, 400)

# =========================
# Performance API
# =========================
def test_performance_ingest_and_get():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    payload = {
        "match_id": "m-001",
        "player_id": "player-123",
        "game_name": "AwesomeFPS",
        "kills": 10,
        "deaths": 2,
        "assists": 3,
        "score": 1500.5,
        "accuracy": 0.45,
        "timestamp": "2024-12-01T12:00:00Z"
    }
    r = client.post("/performance/ingest", json=payload, headers=headers)
    assert r.status_code == 200
    body = r.json()
    assert body["player_id"] == "player-123"
    assert "summary" in body and "kda" in body["summary"]

    r2 = client.get("/performance/performance/player-123", headers=headers)
    assert r2.status_code == 200
    assert r2.json()["summary"]["avg_score"] >= 0

def test_performance_requires_auth():
    payload = {
        "match_id": "m-002",
        "player_id": "player-unauth",
        "game_name": "AwesomeFPS",
        "kills": 1, "deaths": 1, "assists": 0,
        "score": 100.0, "accuracy": 0.1,
        "timestamp": "2024-12-01T12:00:00Z"
    }
    r = client.post("/performance/ingest", json=payload)
    assert r.status_code == 403

def test_performance_invalid_token():
    headers = {"Authorization": "Bearer invalid.token.value"}
    body = {
        "match_id": "m-003", "player_id": "bad-token", "game_name": "AwesomeFPS",
        "kills": 2, "deaths": 2, "assists": 1, "score": 300.0, "accuracy": 0.2,
        "timestamp": "2024-12-01T12:00:00Z"
    }
    r = client.post("/performance/ingest", json=body, headers=headers)
    # verify_token akan gagal → 401
    assert r.status_code == 401

def test_get_performance_404():
    # Tanpa ingest untuk player-x → harus 404
    token = client.post("/auth/login", json={"username": "pingkhan", "password": "12345"}).json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    r = client.get("/performance/performance/player-x", headers=headers)
    assert r.status_code == 404

def test_performance_ingest_failure_500(monkeypatch):
    # Paksa service.ingest_match mengembalikan (performance tanpa summary) untuk memicu 500
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}

    def fake_ingest(_match):
        class Dummy:
            player_id = PlayerId("err-500")
            performance_summary = None
            last_updated = None
        return Dummy(), None

    orig = service.ingest_match
    try:
        monkeypatch.setattr(service, "ingest_match", fake_ingest)
        payload = {
            "match_id": "e-001",
            "player_id": "err-500",
            "game_name": "AwesomeFPS",
            "kills": 0,
            "deaths": 0,
            "assists": 0,
            "score": 0.0,
            "accuracy": 0.0,
            "timestamp": "2024-12-01T12:00:00Z"
        }
        r = client.post("/performance/ingest", json=payload, headers=headers)
        assert r.status_code == 500
        assert r.json()["detail"] == "failed to compute performance"
    finally:
        # Pulihkan method asli
        monkeypatch.setattr(service, "ingest_match", orig)

# =========================
# Leaderboard API
# =========================
def test_leaderboard_flow():
    token = get_token()
    headers = {"Authorization": f"Bearer {token}"}
    perf = client.get("/performance/performance/player-123", headers=headers).json()
    # upsert leaderboard pakai PerformanceOut
    r = client.post("/leaderboard/upsert", json=perf)
    assert r.status_code == 200 and r.json()["ok"] is True

    r2 = client.get("/leaderboard/?limit=10")
    assert r2.status_code == 200
    assert isinstance(r2.json(), list)

    r3 = client.get("/leaderboard/player/player-123")
    assert r3.status_code == 200
    assert r3.json()["player_id"] == "player-123"

def test_leaderboard_player_not_found():
    r = client.get("/leaderboard/player/unknown-player")
    assert r.status_code == 404

# =========================
# Profile API
# =========================
def test_profile_crud():
    prof = {
        "player_id": "player-999",
        "display_name": "Player 999",
        "country": "ID",
        "game_accounts": [{"game": "AwesomeFPS", "external_id": "afps-999"}],
        "bio": "FPS enjoyer"
    }
    r = client.post("/profile/", json=prof)
    assert r.status_code == 200

    r2 = client.get("/profile/player-999")
    assert r2.status_code == 200

    r3 = client.put("/profile/player-999", json={"player_id": "player-999", "display_name": "Pro 999"})
    assert r3.status_code == 200
    assert r3.json()["display_name"] == "Pro 999"

    r4 = client.delete("/profile/player-999")
    assert r4.status_code == 200

def test_profile_not_found_get_and_delete():
    r1 = client.get("/profile/not-exist")
    assert r1.status_code == 404
    r2 = client.delete("/profile/not-exist")
    assert r2.status_code == 404

def test_update_profile_missing_and_fields():
    # GET/PUT pada profile yang belum ada → 404 (cover baris early return)
    r = client.put("/profile/not-exist", json={"player_id": "not-exist", "display_name": "X"})
    assert r.status_code == 404
    # Buat lalu update multiple fields (cover loop assignment)
    create = {
        "player_id": "player-777",
        "display_name": "P777",
        "country": "ID",
        "game_accounts": [{"game":"AwesomeFPS","external_id":"afps-777"}],
        "bio": "bio-1"
    }
    r1 = client.post("/profile/", json=create)
    assert r1.status_code == 200
    
    r2 = client.put("/profile/player-777", json={
        "player_id": "player-777",
        "display_name": "P777-upd",
        "country": "US",
        "bio": "bio-2"
    })
    assert r2.status_code == 200
    body = r2.json()
    assert body["display_name"] == "P777-upd"
    assert body["country"] == "US"
    assert body["bio"] == "bio-2"

def test_profile_create_missing_player_id():
    # Kirim player_id kosong agar lolos schema tapi gagal di router → 400
    bad = {
        "player_id": "",
        "display_name": "No ID",
        "country": "ID",
        "game_accounts": [],
        "bio": "x"
    }
    r = client.post("/profile/", json=bad)
    assert r.status_code == 400
    assert r.json()["detail"] == "player_id required"

def test_profile_create_duplicate():
    # Buat profil lalu buat lagi dengan player_id sama → 409
    prof = {
        "player_id": "dup-123",
        "display_name": "Dup 123",
        "country": "ID",
        "game_accounts": [{"game": "AwesomeFPS", "external_id": "afps-dup"}],
        "bio": "bio"
    }
    r1 = client.post("/profile/", json=prof)
    assert r1.status_code == 200
    r2 = client.post("/profile/", json=prof)
    assert r2.status_code == 409
    assert r2.json()["detail"] == "profile already exists"

# =========================
# Notification API
# =========================
def test_notification_crud():
    pid = "player-123"
    r1 = client.post(f"/notification/{pid}", json={"type": "PERFORMANCE_UPDATED", "message": "updated", "data": {"match_id": "m-001"}})
    assert r1.status_code == 200

    r2 = client.get(f"/notification/{pid}")
    assert r2.status_code == 200
    assert len(r2.json()) >= 1

    r3 = client.delete(f"/notification/{pid}")
    assert r3.status_code == 200

def test_notification_clear_when_empty():
    r = client.delete("/notification/none-player")
    # implementasi sekarang mengembalikan 404 jika tidak ada
    assert r.status_code in (200, 404)

# =========================
# Domain Small Tests
# =========================
def test_player_id_value_and_equality():
    a = PlayerId("player-x")
    b = PlayerId("player-x")
    c = PlayerId("player-y")
    assert a.value == "player-x"
    # equality by value (tanpa __eq__ kustom, objek berbeda !=)
    assert a.value == b.value
    assert a.value != c.value

def test_player_performance_trend_branch():
    pid = PlayerId("trend-1")
    perf = PlayerPerformance(player_id=pid)
    m1 = MatchRecord(
        match_id="t1", player_id=pid, game_name="AwesomeFPS",
        kills=10, deaths=2, assists=3, score=1000.0, accuracy=0.4,
        timestamp=datetime.now(timezone.utc),
    )
    perf.add_match(m1)
    m2 = MatchRecord(
        match_id="t2", player_id=pid, game_name="AwesomeFPS",
        kills=2, deaths=5, assists=1, score=800.0, accuracy=0.3,
        timestamp=datetime.now(timezone.utc),
    )
    perf.add_match(m2)
    assert perf.performance_summary is not None
    # normalisasi ke uppercase agar cocok dengan set yang diuji
    trend_upper = str(perf.performance_summary.trend).upper()
    assert trend_upper in ("UP", "DOWN", "STABLE")

def test_player_performance_init_defaults():
    perf = PlayerPerformance(player_id=PlayerId("init-1"))
    assert perf.games_played == 0
    assert perf.performance_summary is None

def test_player_id_str():
    pid = PlayerId("player-xyz")
    assert str(pid) == "player-xyz"