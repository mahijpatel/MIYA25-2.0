# MIYA25 2.0 — AI Powered Smart Miyawaki Forest Platform

**Prototype build.** Fully working Next.js 15 app with mock data and
localStorage-based auth — no database or backend server required to run it.

## What's inside

- `frontend/` — **the actual app.** Next.js 15 + React 18 + TypeScript +
  Tailwind CSS + Leaflet + Recharts + React Hook Form + Zod. Verified with
  `npm install` (439 packages, clean) and `npm run build` (63 routes, zero
  TypeScript/ESLint errors).
- `backend/` — a partial Express/Prisma scaffold from an earlier direction.
  **Not required** — the frontend doesn't call it. See `backend/README.md`.
- `docs/`, `powerbi/`, `ai-service/` — placeholders from earlier scope, not
  part of the current prototype.

## Run it on your laptop

```bash
cd frontend
npm install
npm run dev
```

Open **http://localhost:3000**. Click any of the three portal buttons on the
landing page (Citizen / Government / Admin) — any email/password works, this
is mock authentication stored in your browser's localStorage.

## See it on your phone (same WiFi network)

1. Find your laptop's local IP:
   - Windows: `ipconfig` → look for "IPv4 Address" (e.g. `192.168.1.42`)
   - Mac/Linux: `ifconfig` or `ip addr` → look for `inet 192.168.x.x`
2. Run the dev server bound to your network instead of just localhost:
   ```bash
   cd frontend
   npm run dev -- -H 0.0.0.0
   ```
3. On your phone (connected to the **same WiFi**), open a browser and go to
   `http://192.168.x.x:3000` (use your actual IP from step 1).
4. Make sure your laptop's firewall allows incoming connections on port 3000
   (Windows will usually prompt you the first time — allow it).

The citizen portal is mobile-first (bottom nav, card layout) so it's the
best one to check on your phone; the Government/Admin portals use a
collapsible sidebar that turns into a hamburger menu below the `lg`
breakpoint.

## Login

There's no real backend, so any email + any password logs you in — just
pick which role tab (Citizen / Government / Admin) you want to preview.
Sessions persist in your browser's localStorage until you hit **Logout**.

## What's actually complete

- **Citizen portal** (19 pages): Home, Nearby Forests, Forest Detail, Adopt
  Tree, Carbon Calculator, Volunteer, Compost, Rewards, Achievements,
  Profile, Notifications, Settings, Learning Center, Green First Responder
  (SOS/first aid/nearby volunteers & hospitals), Report Issue, Weather, AQI,
  Tree Tracking, Activity History, Leaderboard, QR Scanner (simulated).
- **Government portal** (29 pages): Dashboard, Forest Monitoring/Management,
  Tree Plantation/Health, Biodiversity, Urban Heat, GIS Heat Maps, Net Zero,
  Carbon Dashboard/Credits, Smart Compost, IoT/Sensor Dashboard, Drone
  Monitoring, Emergency Dashboard, Fire/Flood/Illegal-Cutting Monitoring,
  Volunteer Management, Citizen Complaints, CSR, NGO, Funding, Reports &
  Power BI, Analytics, Departments, Users, Notifications, Settings.
- **Admin portal** (8 pages): Dashboard, User Management, Roles,
  Permissions, Analytics, Audit Logs, Notifications, Settings.
- No dead links, no 404s (unknown routes auto-redirect to your dashboard),
  every page has back navigation, dark/light mode, responsive layout.

## Known gaps (being upfront)

- No real backend, database, or authentication — this is a mock-data
  prototype by design, per the project brief.
- Power BI `.pbix` files aren't included — that's a proprietary binary
  format that can't be authored outside Power BI Desktop.
- The `backend/`, `ai-service/`, `docs/`, `powerbi/` folders are leftovers
  from an earlier scope and aren't wired into the running app.
