# ARB (Architecture Review Board) Review Rubric

## Expected Sections (checklist)

- [ ] Problem Statement / Business Context
- [ ] Current State Architecture
- [ ] Proposed Architecture
- [ ] Design Alternatives Considered
- [ ] Decision Records (ADR format preferred)
- [ ] Non-Functional Requirements (NFRs)
- [ ] Security Architecture
- [ ] Data Architecture & Flow
- [ ] Integration Points
- [ ] Scalability & Performance
- [ ] Cost Analysis (TCO)
- [ ] Risk Assessment
- [ ] Migration/Transition Plan
- [ ] Rollback Strategy
- [ ] Compliance & Regulatory
- [ ] Operational Readiness
- [ ] Stakeholder Sign-off

## Critical Questions

1. Does the proposal clearly state WHY this architecture change is needed?
2. Are alternatives evaluated with clear trade-off analysis?
3. Is security considered upfront (not as an afterthought)?
4. What happens when this fails? Is there a rollback plan?
5. Who operates this in production? Are they involved in the review?
6. What is the total cost of ownership over 3 years?
7. Does this create vendor lock-in? If so, is the trade-off justified?
8. Are data residency and compliance requirements addressed?