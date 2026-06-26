# C3 Kickoff Brief: Exact Series & Ticker Master List

**Task ID:** C3  
**Priority:** 2 (Elevated per Arena v1.1 feedback)  
**Owner:** Bridge (Integration Dynamo)  
**Status:** In Progress  
**Activated:** June 26, 2026  
**Dependencies:** C1 v1.0, C2 v0.1 (both signed off)

---

## Objective

Create and maintain a complete, accurate master list of all Koyfin and Barchart series used by the Whinfell Transmission Map and BUILD Cousins fallback tools.

## Required Deliverable

One maintained Markdown file in this folder:

`Whinfell_Series_Ticker_Master_List.md`

Must include for each series:
- Component mapping (C1 score component)
- Display name
- Ticker / series identifier
- Platform (Koyfin / Barchart / FRED)
- Field type (price, return, OAS, yield, spread)
- Lookback windows used (1D, 5D, 20D/1M)
- Used in (Comet dashboard / C2 fallback / both)

## Success Criteria

- Complete coverage of all 8 C1 score components
- Resolves C1/C2 open dependency on exact OAS series codes
- Maintainable — single source of truth for data integration

## Review Gates

1. Self Review (Bridge)
2. Peer Review (Blueprint)
3. Arena Review (Integration Dynamo + Basis Avenger)
4. TempLibby Sign-off

---

**Start now. Cross-reference C1 Section 4 and C2 Market Inputs tab.**