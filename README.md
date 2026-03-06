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

## Mission System

Entertainment missions reward active play, event hosting, and community engagement.

| Mission | Description | XP | Unlock |
|---------|-------------|-----|--------|
| First Match | Host an Arena match with 2+ participants | 100 | Default |
| Tournament Run | Run a guild tournament with 8+ players | 400 | Entertainer rank |
| Campaign Arc | Complete a full RPG campaign arc (3+ sessions) | 500 | Entertainer rank |
| Studio Track | Produce a beat via the Beat Generator pipeline | 150 | Default |
| Event Host | Host a live guild event with 10+ attendees | 300 | Host rank |
| Lore Drop | Publish an Entertainment lore event post | 100 | Default |
| XP Champion | Award 1,000+ XP to guild members in a single event | 600 | Arena Champion rank |

**Daily missions (reset 00:00 UTC):**
- Emit a `citadel.ent.arena.match_completed` event — 30 XP
- Post an event announcement in the Guild House feed — 25 XP

Entertainment is the primary XP multiplier for the Brotherhood economy. Hosting events,
running campaigns, and producing content for other guilds earns bonus TP allocations.

---

## Guild Expectations

**Members:**
- Participate in at least 1 Arena match or RPG session per sprint
- Post event recaps in `#arena-results` within 24 hours of match completion
- Complete Entertainment onboarding (Arena + RPG primer) within 7 days of placement
- Engage in `#game-room` and `#events` lobby channels

**Contributors:**
- Arena matchmaking logic changes require load tests (50+ simulated matches)
- RPG session data must be anonymized before any external logging
- Studio Beat Generator changes need audio output samples in the PR
- Code review turnaround: 48 hours

**Guild Lead (Grand Arena Master):**
- Weekly event calendar posted to `#announcements`
- Coordinate tournament brackets with Discord event integrations
- Manage XP award approvals above the standard per-event cap

---

## Contributing

**Branch naming:**
```
feat/<srs-code>/<short-description>
fix/<srs-code>/<short-description>
arena/<srs-code>/<short-description>
```

**PR checklist:**
- [ ] SRS code referenced (e.g., `SRS: ENT-ARENA-004`)
- [ ] `npm test` passes — Arena matchmaking tests included
- [ ] Discord webhook payloads tested against staging channel
- [ ] XP award values reviewed against Brotherhood economy balance
- [ ] No player PII in match result logs

**Commit format:** `<type>(<srs-code>): <description>`
Example: `feat(ENT-ARENA-004): add CAPS-grade balancing to matchmaking`

**SAKE compliance:** New game engine modules require a `.sake` file stub.
See [guild-sdk](https://github.com/citadel-nexus/guild-sdk) for the format.

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
