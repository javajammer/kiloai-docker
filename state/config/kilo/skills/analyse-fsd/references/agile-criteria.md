# Agile/Scrum Methodology Compliance Criteria (A1-A8)

Use this checklist when the detected methodology is Agile/Scrum.
Evaluate each criterion and assign PASS / PARTIAL / FAIL status.

---

## A1: Sprint Time-Boxing

| Field | Content |
|-------|---------|
| **ID** | A1 |
| **Area** | Sprint Planning |
| **Check** | Are sprints time-boxed (fixed duration, 1-4 weeks) with clear sprint goals? |
| **Evidence to Look For** | Sprint duration defined, sprint goal format, sprint calendar, consistent cadence |
| **Severity if Missing** | HIGH |
| **PASS Criteria** | Sprints are consistently time-boxed (same duration each). Each sprint has a clear, single sprint goal. Sprint start/end dates are fixed and respected. |
| **PARTIAL Criteria** | Sprint duration varies, or sprint goals are vague/missing, or deadlines are extended mid-sprint. |
| **FAIL Criteria** | No fixed sprint duration, sprints extend indefinitely, or no sprint goals defined. |

---

## A2: Backlog Health

| Field | Content |
|-------|---------|
| **ID** | A2 |
| **Area** | Backlog |
| **Check** | Is the product backlog prioritized, estimated, and refined regularly? |
| **Evidence to Look For** | Backlog prioritization (ranking/ordering), estimation (story points/t-shirt), refinement cadence, ready items |
| **Severity if Missing** | HIGH |
| **PASS Criteria** | Backlog is ordered by priority/value. Top items estimated. Regular refinement sessions scheduled. "Ready" criteria defined for items entering sprint. Backlog visible to all stakeholders. |
| **PARTIAL Criteria** | Backlog exists but not prioritized, or estimation is inconsistent, or refinement is irregular. |
| **FAIL Criteria** | No single backlog, items added without prioritization, no estimation, or backlog is a dumping ground. |

---

## A3: User Story Quality (INVEST)

| Field | Content |
|-------|---------|
| **ID** | A3 |
| **Area** | User Stories |
| **Check** | Do user stories follow INVEST criteria (Independent, Negotiable, Valuable, Estimable, Small, Testable)? |
| **Evidence to Look For** | Story format ("As a... I want... So that..."), acceptance criteria, story splitting, INVEST compliance |
| **Severity if Missing** | MEDIUM |
| **PASS Criteria** | Stories follow standard format. Each has acceptance criteria. Stories are small enough to complete in one sprint. Stories are independently deployable where possible. |
| **PARTIAL Criteria** | Stories exist but lack acceptance criteria, or are too large (epics masquerading as stories). |
| **FAIL Criteria** | No user stories, or stories are requirements in disguise with no business value framing. |

---

## A4: Definition of Done (DoD)

| Field | Content |
|-------|---------|
| **ID** | A4 |
| **Area** | Definition of Done |
| **Check** | Is there an explicit, shared Definition of Done that the team commits to? |
| **Evidence to Look For** | DoD document/checklist, team agreement, includes quality criteria (code review, testing, documentation) |
| **Severity if Missing** | HIGH |
| **PASS Criteria** | DoD is documented and agreed by the team. Includes: code complete, unit tests passing, code reviewed, integration tests, documentation updated, deployable increment. DoD is reviewed and improved periodically. |
| **PARTIAL Criteria** | DoD exists but is too basic (e.g., just "code complete") or not consistently followed. |
| **FAIL Criteria** | No Definition of Done. "Done" means different things to different people. |

---

## A5: Technical Debt Management

| Field | Content |
|-------|---------|
| **ID** | A5 |
| **Area** | Technical Debt |
| **Check** | Is there a deliberate budget/strategy for managing technical debt per sprint? |
| **Evidence to Look For** | Tech debt backlog items, allocated capacity (% per sprint), refactoring stories, debt tracking |
| **Severity if Missing** | MEDIUM |
| **PASS Criteria** | Technical debt items are visible in backlog. Team allocates capacity (e.g., 15-20% per sprint) for debt reduction. Debt items have business value justification. |
| **PARTIAL Criteria** | Tech debt acknowledged but no systematic approach to address it. |
| **FAIL Criteria** | Technical debt not tracked, or team is pressured to take shortcuts without plan to address them. |

---

## A6: Retrospectives & Continuous Improvement

| Field | Content |
|-------|---------|
| **ID** | A6 |
| **Area** | Retrospectives |
| **Check** | Are sprint retrospectives conducted regularly with actionable outcomes that are tracked? |
| **Evidence to Look For** | Retro meeting records, action items, improvement tracking, team velocity trend |
| **Severity if Missing** | MEDIUM |
| **PASS Criteria** | Retrospectives held every sprint. Action items are assigned with owners and due dates. Previous action items reviewed at start of next retro. Team shows measurable improvement over time. |
| **PARTIAL Criteria** | Retrospectives held but action items not tracked, or same issues raised repeatedly. |
| **FAIL Criteria** | No retrospectives, or retrospectives are skipped under deadline pressure. |

---

## A7: Velocity Tracking & Forecasting

| Field | Content |
|-------|---------|
| **ID** | A7 |
| **Area** | Velocity |
| **Check** | Is velocity tracked and used for realistic forecasting and commitment? |
| **Evidence to Look For** | Velocity chart/trend, sprint commitment based on velocity, release forecasting |
| **Severity if Missing** | LOW |
| **PASS Criteria** | Velocity tracked over multiple sprints. Sprint commitments based on historical velocity. Release forecasts use velocity trends. Team velocity is stable or improving. |
| **PARTIAL Criteria** | Velocity tracked but not used for forecasting, or commitments consistently exceed capacity. |
| **FAIL Criteria** | No velocity tracking, or velocity is used to pressure team rather than plan. |

---

## A8: Cross-Functional Team

| Field | Content |
|-------|---------|
| **ID** | A8 |
| **Area** | Team Composition |
| **Check** | Does the team have all skills needed to deliver end-to-end (dev, test, UX, DB, ops)? |
| **Evidence to Look For** | Team roster, skill matrix, T-shaped skills, pair programming, knowledge sharing |
| **Severity if Missing** | HIGH |
| **PASS Criteria** | Team has all necessary skills. Members are T-shaped (deep in one area, broad in others). Knowledge sharing practices in place. No single point of failure for any skill. |
| **PARTIAL Criteria** | Most skills present but with gaps (e.g., no dedicated tester, no UX, no DBA). |
| **FAIL Criteria** | Team relies heavily on external dependencies for core activities. Single points of failure for critical skills. |

---

## Scoring Guide

| Score | Criteria |
|-------|----------|
| **8/8 PASS** | Fully compliant — Agile/Scrum process is mature and well-executed |
| **6-7 PASS** | Mostly compliant — Minor gaps, acceptable with noted conditions |
| **4-5 PASS** | Partially compliant — Significant gaps, requires coaching/remediation |
| **<4 PASS** | Non-compliant — "Agile" in name only, process not genuinely followed |
