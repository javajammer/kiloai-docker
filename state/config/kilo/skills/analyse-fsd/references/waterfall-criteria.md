# Waterfall Methodology Compliance Criteria (W1-W8)

Use this checklist when the detected methodology is Waterfall.
Evaluate each criterion and assign PASS / PARTIAL / FAIL status.

---

## W1: Requirements Baselining

| Field | Content |
|-------|---------|
| **ID** | W1 |
| **Area** | Requirements Phase |
| **Check** | Are requirements formally baselined, versioned, and signed off before design begins? |
| **Evidence to Look For** | Signed requirements document, version history, baseline date, approval signatures |
| **Severity if Missing** | CRITICAL |
| **PASS Criteria** | Requirements document exists with version number, baseline date, and stakeholder sign-off. Changes tracked via formal process. |
| **PARTIAL Criteria** | Requirements exist but lack formal sign-off, versioning, or baseline date. |
| **FAIL Criteria** | No formal requirements document, or requirements are still being modified during design/implementation. |

---

## W2: Design Review Gate

| Field | Content |
|-------|---------|
| **ID** | W2 |
| **Area** | Design Phase |
| **Check** | Is the design formally reviewed and approved before implementation begins? |
| **Evidence to Look For** | Design review meeting minutes, approval record, reviewer names, review date |
| **Severity if Missing** | CRITICAL |
| **PASS Criteria** | Design document reviewed by designated reviewers with documented feedback and formal approval before coding starts. |
| **PARTIAL Criteria** | Design reviewed informally (email/chat) but no formal review record or approval. |
| **FAIL Criteria** | No design review conducted, or implementation started before design approval. |

---

## W3: Requirements Traceability Matrix (RTM)

| Field | Content |
|-------|---------|
| **ID** | W3 |
| **Area** | Traceability |
| **Check** | Is there a Requirements Traceability Matrix linking requirements → design → code → test cases? |
| **Evidence to Look For** | RTM document, bidirectional traceability, coverage analysis |
| **Severity if Missing** | HIGH |
| **PASS Criteria** | RTM exists with bidirectional traceability. Every requirement maps to design elements, code modules, and test cases. Coverage analysis shows 100% traceability. |
| **PARTIAL Criteria** | RTM exists but incomplete (some requirements not traced, or only forward tracing). |
| **FAIL Criteria** | No RTM exists. No way to verify all requirements are implemented and tested. |

---

## W4: Change Control Process

| Field | Content |
|-------|---------|
| **ID** | W4 |
| **Area** | Change Control |
| **Check** | Is there a formal Change Request (CR) process with approval workflow? |
| **Evidence to Look For** | CR form template, approval workflow diagram, change log, impact assessment process |
| **Severity if Missing** | HIGH |
| **PASS Criteria** | Formal CR process documented. Includes: request form, impact analysis, approval authority, implementation tracking, and audit trail. All scope changes go through this process. |
| **PARTIAL Criteria** | CR process exists but not consistently followed, or lacks impact analysis or audit trail. |
| **FAIL Criteria** | No formal change control process. Scope changes are made ad-hoc without approval. |

---

## W5: Phase Gate Criteria

| Field | Content |
|-------|---------|
| **ID** | W5 |
| **Area** | Phase Gates |
| **Check** | Are phase gate entry/exit criteria explicitly defined for each phase transition? |
| **Evidence to Look For** | Gate checklist, go/no-go criteria, approval authority per gate, gate review meeting records |
| **Severity if Missing** | HIGH |
| **PASS Criteria** | Each phase transition has defined entry and exit criteria. Gate reviews conducted with documented decisions. Clear go/no-go authority. |
| **PARTIAL Criteria** | Phase gates exist but criteria are vague or not consistently applied. |
| **FAIL Criteria** | No phase gates defined, or phases overlap without formal transition. |

---

## W6: V-Model Verification Mapping

| Field | Content |
|-------|---------|
| **ID** | W6 |
| **Area** | V-Model |
| **Check** | Are verification and validation steps mapped to corresponding requirements (left side → right side of V)? |
| **Evidence to Look For** | V-model diagram, verification matrix, test-to-requirement mapping |
| **Severity if Missing** | MEDIUM |
| **PASS Criteria** | V-model diagram present showing relationships between development phases and corresponding verification activities. Each requirement maps to specific test level (unit/integration/system/acceptance). |
| **PARTIAL Criteria** | V-model mentioned but mapping is incomplete or generic. |
| **FAIL Criteria** | No V-model consideration. Testing is disconnected from requirements. |

---

## W7: Testing Strategy Per Phase

| Field | Content |
|-------|---------|
| **ID** | W7 |
| **Area** | Testing Plan |
| **Check** | Is testing planned per phase with clear types (unit → integration → system → UAT → regression)? |
| **Evidence to Look For** | Test plan document, test strategy matrix, entry/exit criteria per test phase, resource allocation |
| **Severity if Missing** | HIGH |
| **PASS Criteria** | Comprehensive test plan with: test types per phase, entry/exit criteria, test data strategy, environment requirements, resource allocation, and defect management process. |
| **PARTIAL Criteria** | Test plan exists but lacks specificity (e.g., no entry/exit criteria, no resource plan). |
| **FAIL Criteria** | No test plan, or testing is an afterthought with no structured approach. |

---

## W8: Phase Deliverables Documentation

| Field | Content |
|-------|---------|
| **ID** | W8 |
| **Area** | Documentation |
| **Check** | Are deliverables per phase documented and archived (requirements doc, design doc, test reports, deployment records)? |
| **Evidence to Look For** | Deliverable list per phase, document repository, version control, archive policy |
| **Severity if Missing** | MEDIUM |
| **PASS Criteria** | Clear list of deliverables per phase. All deliverables stored in version-controlled repository. Document retention policy defined. |
| **PARTIAL Criteria** | Some deliverables documented but not consistently stored or versioned. |
| **FAIL Criteria** | No documentation plan. Deliverables are ad-hoc or lost. |

---

## Scoring Guide

| Score | Criteria |
|-------|----------|
| **8/8 PASS** | Fully compliant — Waterfall process is mature and well-executed |
| **6-7 PASS** | Mostly compliant — Minor gaps, acceptable with noted conditions |
| **4-5 PASS** | Partially compliant — Significant gaps, requires remediation plan |
| **<4 PASS** | Non-compliant — Waterfall process is not being followed effectively |
