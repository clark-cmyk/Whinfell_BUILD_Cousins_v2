# C3 Kickoff Brief: Exact Series & Ticker Master List

**Task ID:** C3  
**Priority:** Medium (after C2 sign-off)  
**Owner:** Bridge  
**Status:** In Progress  
**Target:** 2 days  
**Activated:** June 26, 2026 (Facilitated by Track 1)  
**Dependencies:** C1 v1.0, C2 v0.1 (both signed off)

---

## Objective

Create a single source of truth for every ticker/series used in the Whinfell Transmission Map (Koyfin + Barchart + FRED proxies).

## Deliverable

A clean Markdown table in `07_Reference_Materials/Whinfell_Series_Ticker_Master_List.md` with columns:

| Column | Description |
|--------|-------------|
| Component | e.g., HY Spread, Equity Breadth, Basis Edge, Futures Leadership |
| Primary Ticker/Series | Authoritative series identifier |
| Fallback / Proxy | Next-best when primary unavailable |
| Time Window | 5D, 20D, 1Y, etc. |
| Koyfin / Barchart Source | Platform lookup path |
| Maintenance Note | Update triggers, proxy rules, open items |

## Success Criteria

- Complete coverage of all **8 Whinfell Score components** + **Basis** + **Futures Leadership**
- Clear proxy hierarchy (e.g., when OAS is not available)
- Easy to update and share with the desk

## Review Gates

1. Self Review (Bridge)
2. Peer Review (Blueprint)
3. Arena Review (Integration Dynamo + Macro Guardian)
4. TempLibby Sign-off

---

**C3 officially kicked off. Bridge to deliver master list within 2-day target.**