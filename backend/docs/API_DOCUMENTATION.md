# MIYA25 Backend — API Documentation

Base URL (local): `http://localhost:5000`

Every response follows this envelope:

```json
// success
{ "success": true, "message": "...", "data": {} }
// error
{ "success": false, "message": "..." }
```

Auth header (for protected routes): `Authorization: Bearer <jwt_token>`

Legend: 🔓 public · 🔑 optional auth (works either way, personalizes if logged in) · 🔒 login required · 🛡️ role-restricted

---

## Auth

| Method | Endpoint | Access | Body | Notes |
|---|---|---|---|---|
| POST | `/api/auth/register` | 🔓 | `{name, email, password, role?}` | `role` ∈ citizen\|gov\|admin, defaults to citizen |
| POST | `/api/auth/login` | 🔓 | `{email, password, role?}` | Returns `{token, user}` |
| GET | `/api/auth/me` | 🔒 | — | Current user profile |
| POST | `/api/auth/logout` | 🔒 | — | Stateless; frontend discards token |

**Demo accounts:** `citizen@miya25.test` / `Citizen@123`, `gov@miya25.test` / `Gov@123`, `admin@miya25.test` / `Admin@123`

---

## Plant Identification

| Method | Endpoint | Access | Body |
|---|---|---|---|
| POST | `/api/predict` | 🔓 | multipart, field `image` (or `file`) |
| GET | `/api/plants` | 🔓 | query: `search`, `category` |
| GET | `/api/plants/<name>` | 🔓 | — |

`/api/predict` response `data`: `name, scientificName, category, medicinalUse, emergencyUse, note, confidence, imageUrl`.

---

## Trees & Forests

| Method | Endpoint | Access |
|---|---|---|
| GET | `/api/trees` (query: `forest_site_id`, `health_status`) | 🔓 |
| GET | `/api/trees/<id>` | 🔓 |
| POST | `/api/trees` | 🔑 |
| POST | `/api/trees/<id>/adopt` | 🔒 |
| GET | `/api/forests` | 🔓 |
| GET | `/api/forests/<id>` | 🔓 |

---

## Carbon & Emissions

| Method | Endpoint | Access | Body |
|---|---|---|---|
| GET | `/api/carbon-logs` | 🔑 | — |
| POST | `/api/carbon-logs` | 🔑 | `{transport_kg, electricity_kg, diet_kg, waste_kg, diet_type}` |
| GET | `/api/carbon-credits` | 🔓 | — (gov carbon dashboard) |

---

## Emergency, Complaints & Feedback

| Method | Endpoint | Access | Body |
|---|---|---|---|
| GET | `/api/emergency-reports` (query: `status`, `category`) | 🔑 | — |
| POST | `/api/emergency-reports` | 🔑 | JSON or multipart(`attachment`): `{title, category, description, severity, location_name, latitude, longitude}` |
| POST | `/api/complaint` | 🔑 | JSON or multipart(`attachment`): `{title, category, description, location_name}` |
| GET | `/api/complaint/status/<id>` | 🔑 | — |
| GET | `/api/complaint/mine` | 🔑 | — |
| GET | `/api/complaint/all` | 🔑 | gov/admin complaint dashboard |
| POST | `/api/feedback` | 🔑 | `{subject, message, rating}` |
| GET | `/api/feedback` | 🔑 | Citizens see only their own; gov/admin see all |

---

## Waste, Compost & Volunteering

| Method | Endpoint | Access | Body |
|---|---|---|---|
| GET | `/api/pickups/mine` | 🔑 | — |
| POST | `/api/pickups` | 🔑 | `{waste_type, quantity_kg, address, scheduled_date}` |
| GET | `/api/compost-units` | 🔓 | — |
| GET | `/api/volunteers` | 🔓 | — |
| POST | `/api/volunteer-signups` | 🔑 | `{volunteer_id, full_name, phone}` |
| GET | `/api/volunteer-signups/mine` | 🔑 | — |

---

## Rewards Module

| Method | Endpoint | Access | Body |
|---|---|---|---|
| GET | `/api/rewards` | 🔓 | Redeemable catalog |
| GET | `/api/badges` | 🔑 | Flags `earned: true/false` if logged in |
| GET | `/api/wallet` | 🔒 | Points balance |
| GET | `/api/history` | 🔒 | Redemption history |
| POST | `/api/redeem` | 🔒 | `{reward_id}` |

---

## Dashboard, Leaderboard, Achievements

| Method | Endpoint | Access |
|---|---|---|
| GET | `/api/dashboard/summary` | 🔑 |
| GET | `/api/dashboard/recent-activity` | 🔑 |
| GET | `/api/dashboard/statistics` | 🔓 |
| GET | `/api/leaderboard` (query: `limit`) | 🔓 |
| GET | `/api/achievements` | 🔑 |

---

## Profile & Notifications

| Method | Endpoint | Access | Body |
|---|---|---|---|
| GET | `/api/profile` | 🔒 | — |
| PUT | `/api/profile` | 🔒 | `{name, phone, city}` |
| POST | `/api/profile/photo` | 🔒 | multipart, field `photo` |
| GET | `/api/notifications` | 🔑 | — |
| POST | `/api/notifications/<id>/read` | 🔑 | — |
| POST | `/api/notifications/read-all` | 🔑 | — |

---

## Government / Admin Monitoring

| Method | Endpoint | Access |
|---|---|---|
| GET | `/api/departments` | 🔓 |
| GET | `/api/drone-missions` | 🔓 |
| GET | `/api/flood-zones` | 🔓 |
| GET | `/api/heat-zones` | 🔓 |
| GET | `/api/sensor-readings` (query: `sensor_type`) | 🔓 |
| GET | `/api/learning-articles` (query: `category`) | 🔓 |
| GET | `/api/audit-logs` (query: `limit`) | 🛡️ admin, gov |
| GET | `/api/users` (query: `role`) | 🛡️ admin, gov |
| GET | `/api/users/<id>` | 🛡️ admin, gov |
| PUT | `/api/users/<id>` | 🛡️ admin |

---

## Bhavnagar City Data & Weather

| Method | Endpoint | Access |
|---|---|---|
| GET | `/api/bhavnagar/sections` | 🔓 |
| GET | `/api/bhavnagar/<section>` | 🔓 |
| GET | `/api/bhavnagar/all` | 🔓 |
| GET | `/api/hospitals` | 🔓 |
| GET | `/api/weather` | 🔓 |
| GET | `/api/aqi` | 🔓 |

Valid `<section>` values: `hospitals`, `primary_health_centres`, `government_offices`,
`municipal_offices`, `fire_stations`, `police_stations`, `parks_and_gardens`,
`lakes_and_water_bodies`, `tourist_places`, `emergency_contacts`, `nearby_ngos`,
`waste_collection_centers`, `blood_banks`, `ambulance_services`, `public_toilets`,
`tree_plantation_areas`, `environmental_projects`, `rainwater_harvesting_sites`,
`smart_city_projects`.

`/api/weather` and `/api/aqi` try a live Open-Meteo lookup for Bhavnagar first and
fall back to realistic dummy data if the request fails — the frontend always
gets a `200` with usable data either way (check `data.source`: `"open-meteo"` or `"fallback"`).

---

## Misc

| Method | Endpoint | Access |
|---|---|---|
| GET | `/api/health` | 🔓 | Health check |
| GET | `/uploads/<path>` | 🔓 | Serves uploaded files (photos, plant images, attachments) |

---

## Error codes used

| Code | Meaning |
|---|---|
| 400 | Bad request (e.g. insufficient points to redeem) |
| 401 | Missing/invalid/expired token, or bad login credentials |
| 403 | Authenticated but not permitted (wrong role) |
| 404 | Resource not found |
| 409 | Conflict (e.g. tree already adopted, reward out of stock, email taken) |
| 413 | Uploaded file exceeds 10MB |
| 422 | Validation error (missing required field) |
| 500 | Unexpected server error — always returned as clean JSON, never a crash |
