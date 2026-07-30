# MIYA25 Backend

A lightweight Flask + SQLite backend built to power the **MIYA25 V3.0** Next.js
frontend (citizen / government / admin portals). It is designed so every
button, form, upload and page in the frontend gets a real, stable response —
either from the database or from realistic sample data — with nothing left
half-built.

---

## 1. Tech stack

- **Flask 3** + **Flask-CORS** — REST API
- **SQLite** via **SQLAlchemy** — zero-config, file-based database (`database.db`)
- **PyJWT** — stateless JWT authentication (citizen / gov / admin roles)
- **Werkzeug** password hashing — no plaintext passwords, ever
- No Docker, no Redis, no Celery, no Kubernetes — just `python app.py`

---

## 2. Project structure

```
backend/
├── app.py                 # Entry point - creates the app, DB tables, seeds demo data
├── config.py               # All settings (env-var overridable)
├── requirements.txt
├── .env.example
├── database.db              # Created automatically on first run
├── routes/                  # One blueprint per feature area
├── models/                  # One SQLAlchemy model per table
├── services/
│   └── prediction_service.py  # Plant identification logic (swap-in point for a real ML model)
├── utils/
│   ├── decorators.py         # JWT middleware (token_required / role_required / optional_auth)
│   ├── response.py           # Standard {success, message, data} JSON envelope
│   └── file_upload.py         # Safe upload handling (jpg/jpeg/png/pdf, 10MB max)
├── data/
│   ├── plants.json            # 54 medicinal plants (name, scientificName, category, uses, precautions...)
│   └── bhavnagar.json         # Bhavnagar city reference data (hospitals, parks, NGOs, etc.)
├── uploads/                  # Uploaded files land here (served back at /uploads/...)
├── static/
├── seed.py                   # Populates SQLite with demo data the first time it runs
└── docs/
    ├── API_DOCUMENTATION.md
    └── MIYA25_Backend.postman_collection.json
```

---

## 3. Setup & run

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install -r requirements.txt
python app.py
```

The API will be live at **http://localhost:5000**.

On first run the app automatically:
1. Creates `database.db` and all tables.
2. Seeds demo users, trees, forests, rewards, Bhavnagar-area gov data, etc.
   (Re-running `python app.py` will **not** duplicate this data — it only
   seeds when the `users` table is empty.)

To wipe and reseed from scratch, just delete `database.db` and restart.

### Connecting your Next.js frontend

Point your frontend's API base URL at `http://localhost:5000`. Add to your
frontend's `.env.local`:

```
NEXT_PUBLIC_API_BASE_URL=http://localhost:5000
```

CORS is pre-configured for `http://localhost:3000`. To allow another origin,
edit `CORS_ORIGINS` in `.env` (comma-separated).

---

## 4. Demo accounts

| Role    | Email                 | Password     |
|---------|-----------------------|--------------|
| Citizen | citizen@miya25.test   | Citizen@123  |
| Gov     | gov@miya25.test       | Gov@123      |
| Admin   | admin@miya25.test     | Admin@123    |

A few extra citizen accounts (`kavya@miya25.test`, `rohan@miya25.test`,
`meera@miya25.test`) all use password `Citizen@123` and exist purely to
populate the leaderboard with realistic data.

---

## 5. Standard response shape

Every endpoint returns the same JSON envelope, so the frontend never has to
guess the shape of an error:

```json
// Success
{ "success": true, "message": "Trees fetched.", "data": [ ... ] }

// Error
{ "success": false, "message": "Authentication token is missing." }
```

HTTP status codes are used correctly alongside this (`200`, `201`, `401`,
`403`, `404`, `409`, `413`, `422`, `500`) but the frontend can always safely
check `response.data.success` first.

---

## 6. Authentication

- `POST /api/auth/register` — `{ name, email, password, role }` (`role` defaults to `citizen`)
- `POST /api/auth/login` — `{ email, password, role? }` → `{ token, user }`
- `GET /api/auth/me` — requires `Authorization: Bearer <token>`
- `POST /api/auth/logout` — stateless; frontend just discards the token

Send the JWT on every authenticated request as:

```
Authorization: Bearer <token>
```

Endpoints that are **useful without login** (e.g. viewing plants, forests,
Bhavnagar data, weather) do not require a token. Endpoints tied to "my data"
(profile, my pickups, my complaints, rewards wallet, adopt a tree, etc.) use
`optional_auth` or `token_required` — see `docs/API_DOCUMENTATION.md` for the
full per-endpoint list.

---

## 7. Plant Identification (`POST /api/predict`)

Accepts a multipart upload with field name `image` (or `file`), and returns:

```json
{
  "success": true,
  "message": "Plant identified successfully.",
  "data": {
    "name": "Tulsi",
    "scientificName": "Ocimum tenuiflorum",
    "category": "Herb",
    "medicinalUse": "Helps with cough, cold and sore throat.",
    "emergencyUse": "Chew washed leaves or prepare a warm infusion for mild cough.",
    "note": "Traditional medicinal use only.",
    "confidence": 96.4,
    "imageUrl": "/uploads/plant_images/xxxxx.jpg"
  }
}
```

**Today's logic** (see `services/prediction_service.py`): the uploaded
filename is checked against known plant-name keywords (e.g. a file named
`tulsi_leaf.jpg` returns Tulsi). No keyword match → a random plant from the
54-plant catalog is returned with a realistic confidence score (90–99%).

**Swapping in a real model later:** replace the body of `run_inference()`
in `services/prediction_service.py` with real TensorFlow/Keras inference.
Keep the same function signature and return shape and nothing else in the
app needs to change.

---

## 8. Bhavnagar city data

`data/bhavnagar.json` ships with realistic sample records for Bhavnagar,
Gujarat covering hospitals, primary health centres, government & municipal
offices, fire & police stations, parks & gardens, lakes, tourist places,
emergency contacts, nearby NGOs, waste collection centers, blood banks,
ambulance services, public toilets, tree plantation areas, environmental
projects, rainwater harvesting sites and smart city projects.

Browse it via:
- `GET /api/bhavnagar/sections` — list of available section names
- `GET /api/bhavnagar/<section>` — e.g. `/api/bhavnagar/hospitals`
- `GET /api/bhavnagar/all` — everything in one call
- `GET /api/hospitals` — convenience alias used by the frontend's `useHospitals()` hook

**Live data:** `GET /api/weather` and `GET /api/aqi` attempt a live lookup
for Bhavnagar (21.7645° N, 72.1519° E) from the free, no-key Open-Meteo API.
If the request fails or times out (e.g. no internet access on your machine),
they fall back to realistic dummy data automatically — the frontend never
sees an error.

---

## 9. Everything else

See `docs/API_DOCUMENTATION.md` for the complete endpoint reference (every
route, method, auth requirement, request body and response shape), and
import `docs/MIYA25_Backend.postman_collection.json` into Postman to try
every endpoint immediately.

---

## 10. Design notes

- **Never crashes**: every route body is wrapped so unexpected errors return
  a clean `{success:false, message:...}` JSON response (HTTP 500) instead of
  an unhandled stack trace.
- **Lightweight by design**: reference/catalog data (medicinal plants,
  Bhavnagar places) lives in JSON files, while user-generated and
  transactional data (users, trees, carbon logs, rewards, complaints, etc.)
  lives in SQLite via SQLAlchemy.
- **File uploads**: `jpg`, `jpeg`, `png`, `pdf` only, 10MB max, stored under
  `uploads/` with a randomized filename, served back at `/uploads/...`.
