# Guild: Entertainment

> *"The arena never closes. The crowd never sleeps."*

The Entertainment Guild is where Citadel members come to play. RPG campaigns,
competitive events, the Arena, lore progression, and gamification. Entertainment
drives Brotherhood XP through structured play — quests, tournaments, and
the spectacle of the Guild House.

---

## Identity

| | |
|---|---|
| **Sigil** | The Crossed Swords on Stage |
| **Vibe** | Electric. Loud. The roar of the crowd when the final boss drops. |
| **Color** | Crimson `#C0392B` |
| **NATS Prefix** | `citadel.ent.*` |
| **Port** | `8400` |
| **Parent Guild** | Entertainment (root) |
| **Sub-guilds** | Creator, Writers, Music |

---

## Purpose

- Host **RPG campaigns** and track session progression
- Run the **Arena** — PvP events, tournaments, leaderboard management
- Award **XP and TP** through gameplay events (missions, battles, achievements)
- Compile **session lore** into canonical narrative (via Creator/Writers guilds)
- Drive **Guild House social engagement** — events, announcements, match results
- Coordinate **music scoring** for events via Music Studio sub-guild

---

## Domains of Operation

### Arena System
- PvP matchmaking with CAPS-grade balancing
- Tournament brackets with XP prizes
- Real-time match results via NATS + Discord webhooks

### RPG Campaign Engine
- Session tracking in `rpg_sessions` (Supabase)
- Quest/mission progression tied to Brotherhood rank
- Lore extraction pipeline → `lore_entries` → book pipeline

### XP Economy
| Action | XP Award |
|--------|----------|
| Mission completed | 100 XP |
| Arena win | 150 XP |
| Lore contribution | 200 XP |
| Tournament top-3 | 500 XP |
| Rank milestone | 1000 XP |

---

## Services & Integrations

| Service | Role |
|---------|------|
| **Supabase** | `rpg_sessions`, `lore_entries`, `oad_missions`, `character_sheets` |
| **Discord** | Event announcements, match results, lore drops |
| **NATS** | `citadel.ent.*` event bus |
| **PostHog** | `guild_house_mission_*`, `guild_house_rank_up` events |
| **Datadog** | Arena latency + error rate monitors |

---

## NATS Event Subjects

```
citadel.ent.arena.match_started     — PvP match initiated
citadel.ent.arena.match_completed   — Result + XP awarded
citadel.ent.rpg.session_started     — Campaign session opened
citadel.ent.rpg.session_ended       — Session data persisted
citadel.ent.tournament.bracket_set  — New tournament created
citadel.ent.xp.awarded              — XP event emitted
```

---

## Getting Started

```bash
npm install
cp .env.example .env
npm run dev
```

## Environment Variables

```
NATS_URL=nats://<your-nats-host>:4222
SUPABASE_SERVICE_ROLE_KEY=<key>
DISCORD_BOT_TOKEN=<token>
DISCORD_WEBHOOK_URL=<url>
GUILD_PORT=8400
```
