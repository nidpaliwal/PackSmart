# Software Requirements Specification

## PackSmart – AI-Based Intelligent Food Packaging Material Recommendation System

**Problem Statement:** SIH26236 (Ministry of Food Processing Industries, Software, Theme: Agriculture, FoodTech & Rural Development)

**Version:** 1.0 (draft) | **Date:** 21 September 2026

---

## 1. Introduction

### 1.1 Purpose

This document specifies the requirements for PackSmart, a web application that recommends the most suitable packaging material for a food commodity. It is written for the development team, mentors and evaluators.

### 1.2 Problem Background

Choosing food packaging is mostly done by experience. A wrong choice causes spoilage, moisture gain, rancidity, higher cost, non-compliance with food-contact rules, or plastic waste. Small food processors (MSMEs, FPOs, women self-help groups) rarely have a packaging expert.

### 1.3 Scope

**In scope:**
- Recommend and rank packaging materials and structures for a given food commodity and conditions.
- Estimate shelf life for each option.
- Estimate cost and sustainability for each option.
- Show regulatory and food-safety notes.
- Explain every recommendation in plain language.
- Export a report.

**Out of scope (version 1):**
- Packaging machinery selection, label artwork design, and physical lab testing.
- Real-time sensor monitoring inside packs.

### 1.4 Definitions

| Term | Meaning |
|------|---------|
| WVTR | Water vapour transmission rate of a packaging film |
| OTR | Oxygen transmission rate of a packaging film |
| aw | Water activity of a food |
| MAP | Modified atmosphere packaging |
| MCDM / TOPSIS | Multi-criteria decision making / a ranking method |
| FSSAI | Food Safety and Standards Authority of India |
| BIS | Bureau of Indian Standards |
| EPR | Extended Producer Responsibility (plastic packaging rules) |
| RAG | Retrieval-augmented generation |

### 1.5 References

- Food Safety and Standards (Packaging) Regulations, 2018 (FSSAI)
- Plastic Waste Management Rules, 2016 and later amendments, including EPR provisions
- BIS standards on food-contact plastics and migration testing
- IEEE 29148 (requirements engineering)
- Published packaging science literature for barrier values and shelf-life models (Labuza moisture-uptake model)

---

## 2. Overall Description

### 2.1 Product Perspective

A standalone, mobile-friendly web application with a REST API, a knowledge base (database) of foods and packaging materials, a recommendation and shelf-life engine, and an explanation assistant.

### 2.2 Product Functions (Summary)

1. Collect food, storage and business inputs.
2. Filter out unsafe or unsuitable packaging.
3. Rank the remaining options.
4. Predict shelf life for each option.
5. Show cost and sustainability scores.
6. Check compliance and give warnings.
7. Explain results and allow what-if changes.
8. Export a PDF report.

### 2.3 User Classes

| User | Description | Needs |
|------|-------------|-------|
| Food processor / MSME owner | Main user, low technical knowledge | Simple form, clear answer, low cost |
| Packaging or quality engineer | Technical user | Numbers, comparisons, export |
| Farmer / FPO / SHG | Fresh produce and primary processing | Local language, simple output |
| Reviewer / inspector | Checks compliance | Compliance notes and sources |
| Domain admin | Maintains the knowledge base | Add and edit foods, materials, rules |

### 2.4 Operating Environment

- Web browsers (Chrome, Edge, Firefox, Safari) on mobile and desktop.
- Backend on Linux, deployable on a cloud VM or container.

### 2.5 Constraints

- Barrier and shelf-life data must come from published, citable sources.
- Results are decision support, not a certified shelf-life test; the app must say so.
- The prototype must run on a low-cost server.
- Development window is about 3 to 4 weeks.

### 2.6 Assumptions and Dependencies

- Public literature and standards provide enough data for 30 to 50 commodities and 15 to 25 packaging options.
- Prices are indicative and stored in an editable table.
- Optional dependency on an LLM API or a local open model for explanations.

---

## 3. Functional Requirements

Priority: **M** = Must, **S** = Should, **C** = Could.

### 3.1 Input Collection (FR-1)

| ID | Requirement | Pri |
|----|-------------|-----|
| FR-1.1 | The system shall let the user select a food category and commodity. | M |
| FR-1.2 | The system shall pre-fill known properties (moisture, water activity, fat, acidity, oxygen and light sensitivity, respiration rate) and let the user override them. | M |
| FR-1.3 | The system shall accept target shelf life, pack size, storage temperature and humidity, transport mode and duration. | M |
| FR-1.4 | The system shall accept budget per unit and a sustainability priority (low, medium, high). | S |
| FR-1.5 | The system shall validate inputs and show clear error messages. | M |

### 3.2 Knowledge Base (FR-2)

| ID | Requirement | Pri |
|----|-------------|-----|
| FR-2.1 | The system shall store commodity profiles with their spoilage mechanisms and critical packaging needs. | M |
| FR-2.2 | The system shall store packaging materials with WVTR, OTR, light barrier, heat-seal ability, temperature range, indicative cost, recyclability and food-contact status. | M |
| FR-2.3 | The system shall store a source reference for every data value. | S |
| FR-2.4 | The system shall store regulatory rules as structured records with a citation. | M |

### 3.3 Recommendation Engine (FR-3)

| ID | Requirement | Pri |
|----|-------------|-----|
| FR-3.1 | The system shall first remove materials that fail hard constraints. | M |
| FR-3.2 | The system shall score the remaining options on barrier match, shelf-life fit, cost, sustainability and practicality. | M |
| FR-3.3 | The system shall return the top 3 ranked options with a score for each. | M |
| FR-3.4 | The system shall let the user change criteria weights and re-rank instantly. | S |
| FR-3.5 | The system shall recommend a multi-layer structure when a single film is not enough. | S |
| FR-3.6 | The system shall suggest MAP or an oxygen absorber where it is useful. | C |

### 3.4 Shelf-Life Prediction (FR-4)

| ID | Requirement | Pri |
|----|-------------|-----|
| FR-4.1 | The system shall estimate shelf life for each recommended option under the entered storage conditions. | M |
| FR-4.2 | For moisture-sensitive dry foods the system shall use a moisture-uptake model (Labuza). | M |
| FR-4.3 | For oxidation-sensitive foods the system shall use oxygen-ingress limits and a temperature acceleration factor (Q10). | S |
| FR-4.4 | The system shall show shelf life as a range, not a single exact number, and label it "estimate". | M |
| FR-4.5 | An ML model may adjust the estimate using training data. | C |

### 3.5 Cost and Sustainability (FR-5)

| ID | Requirement | Pri |
|----|-------------|-----|
| FR-5.1 | The system shall estimate packaging cost per unit and per kg of food. | M |
| FR-5.2 | The system shall give a sustainability score based on recyclability, material weight, recycled or bio-based content and EPR applicability. | S |
| FR-5.3 | The system shall flag over-packaging. | S |
| FR-5.4 | The system shall show a cost versus shelf-life chart. | S |

### 3.6 Compliance Checking (FR-6)

| ID | Requirement | Pri |
|----|-------------|-----|
| FR-6.1 | The system shall show relevant FSSAI packaging requirements. | M |
| FR-6.2 | The system shall warn when a material is not suitable for the food. | M |
| FR-6.3 | The system shall show plastic-waste and EPR notes where they apply. | S |
| FR-6.4 | The system shall include a disclaimer that final compliance needs testing and legal confirmation. | M |

### 3.7 Explanation and Assistant (FR-7)

| ID | Requirement | Pri |
|----|-------------|-----|
| FR-7.1 | The system shall explain each ranking in plain words. | M |
| FR-7.2 | The system shall provide a chat assistant that answers follow-up questions using only the knowledge base and regulations (RAG). | S |
| FR-7.3 | The assistant shall cite its sources and say when it does not know. | S |

> **Implementation note:** FR-7.2 and FR-7.3 are implemented as a template-based explanation engine rather than an LLM-powered chat, since no external LLM API dependency was desired for the prototype. The template engine generates plain-language explanations grounded in the knowledge base data and cited regulations.

### 3.8 Comparison and What-If (FR-8)

| ID | Requirement | Pri |
|----|-------------|-----|
| FR-8.1 | The system shall show a side-by-side comparison of the top options. | M |
| FR-8.2 | The system shall allow changing shelf-life target, temperature or budget and update results. | S |

### 3.9 Reports (FR-9)

| ID | Requirement | Pri |
|----|-------------|-----|
| FR-9.1 | The system shall generate a PDF report with inputs, recommendations, estimates, compliance notes and disclaimers. | M |
| FR-9.2 | The system shall save a history of recommendations for a logged-in user. | C |

> **Implementation note:** FR-9.2 (user history/login) is skipped for the prototype.

### 3.10 Administration (FR-10)

| ID | Requirement | Pri |
|----|-------------|-----|
| FR-10.1 | An admin shall be able to add, edit and delete commodities, materials, prices and rules. | S |
| FR-10.2 | The system shall keep an audit log of admin changes. | C |

### 3.11 Language and Feedback (FR-11)

| ID | Requirement | Pri |
|----|-------------|-----|
| FR-11.1 | The UI shall support English and Hindi, with room to add more languages. | S |
| FR-11.2 | The user shall be able to rate a recommendation and leave a comment. | C |

---

## 4. External Interface Requirements

### 4.1 User Interface (Screens)

- Home: short description and "Start" button.
- Input form: step-by-step with a progress bar (food, storage, business).
- Results: top 3 cards with score, shelf life, cost and eco rating.
- Compare and what-if: table, sliders and charts.
- Compliance: warnings and citations.
- Admin: knowledge base editor.
- The UI shall be responsive and usable on a 360px wide phone screen.

### 4.2 Software Interfaces

- REST API (JSON) between frontend and backend.
- Database (SQLite or PostgreSQL).
- Optional LLM API or local model for explanations; optional vector store for RAG.

### 4.3 Communication

- HTTPS for all traffic.

---

## 5. Non-Functional Requirements

| ID | Category | Requirement |
|----|----------|-------------|
| NFR-1 | Performance | Recommendation response in under 3 seconds. |
| NFR-2 | Performance | Support at least 50 concurrent users on a basic server. |
| NFR-3 | Accuracy | Expert-preferred material in top 3 at least 85% of the time. |
| NFR-4 | Explainability | Every score traceable to inputs and data sources. |
| NFR-5 | Usability | First-time user gets result within 2 minutes, at most 8 mandatory fields. |
| NFR-6 | Reliability | 99% availability during demo; graceful error messages. |
| NFR-7 | Security | Input validation, no storage of personal data beyond optional email. |
| NFR-8 | Privacy | No user data sent to external services without notice. |
| NFR-9 | Maintainability | Knowledge base changes shall not require code changes. |
| NFR-10 | Portability | Runs in Docker on any Linux host. |
| NFR-11 | Transparency | Every result page shall state that values are estimates. |

---

## 6. Data Requirements

### 6.1 Main Entities

| Entity | Key fields |
|--------|-----------|
| Commodity | id, name, category, moisture %, aw, fat %, pH, respiration rate, oxygen sensitive, light sensitive, main spoilage mode, critical moisture limit, source |
| PackagingMaterial | id, name, layers, thickness, WVTR, OTR, light barrier, heat sealable, temp min/max, cost per m², recyclability, food-contact status, source |
| Rule | id, commodity or material scope, condition, message, regulation citation, source |
| Recommendation | id, inputs (JSON), results (JSON), created time |
| User (optional) | id, email, role |

### 6.2 Data Sources

- Published barrier property tables for common films.
- FSSAI packaging regulations and BIS standards.
- Food science literature for water activity, critical moisture and Q10 values.
- Market price surveys, entered as indicative values with a date.

---

## 7. System Design Overview

### 7.1 Architecture

```
User browser
    ↓
Frontend: React + Tailwind CSS
    ↓ REST API (JSON)
Backend API: FastAPI
    ├── Rule filter
    ├── Scoring and ranking
    ├── Shelf-life model
    ├── Cost and eco scorer
    ├── Knowledge base (SQLite)
    └── Explanation assistant (template-based)
```

### 7.2 Recommendation Logic

1. **Filter:** Remove materials that violate hard rules.
2. **Score:** Score = w1·Barrier + w2·ShelfLife + w3·Cost + w4·Sustainability + w5·Practicality
3. **Rank:** Sort and return top 3.
4. **Predict:** Estimate shelf life for top options.
5. **Explain:** Generate reasons and warnings from rules and data.

### 7.3 Shelf-Life Model (Moisture-Sensitive Foods)

Labuza moisture-uptake model:

```
ln[(me − mi) / (me − mc)] = (k / x) · (A / Ws) · (p0 / b) · t
```

Solve for t. Values validated against published shelf-life data.

### 7.4 Role of AI

- **ML:** Ranking or classification model trained on expert-labelled pairs; shelf-life adjustment model.
- **Template explanations:** Natural-language explanations grounded in knowledge base and regulations (no LLM for prototype).

---

## 8. Sample Use Cases

### UC-1: Potato Chips
- Input: crisp snack, 40g, 90 days, 30°C, 70% RH, road transport
- Expected: metallised film laminate ranks first

### UC-2: Fresh Tomatoes
- Input: 500g, 7 days, 25°C, local market
- Expected: breathable film ranks first; high-barrier film rejected

### UC-3: Edible Oil
- Input: 1L, 9 months, ambient
- Expected: light and oxygen barrier options rank first

---

## 9. Acceptance and Test Criteria

| ID | Test | Pass condition |
|----|------|----------------|
| T-1 | Form validation | Invalid or missing inputs blocked with clear messages |
| T-2 | Hard-rule filtering | Unsafe material never shown for incompatible product |
| T-3 | Ranking | Expected top choice in top 3 for 3 sample use cases |
| T-4 | Shelf-life estimate | Within ±20% of reference for 5 documented products |
| T-5 | What-if | Changing parameters updates results within 3 seconds |
| T-6 | Compliance | Relevant citation shown for each warning |
| T-7 | Report | PDF downloads with all sections |
| T-8 | Mobile | All screens usable at 360px width |
| T-9 | Assistant | Refuses or says "not sure" for out-of-scope questions |

---

## 10. Risks and Open Issues

| Risk | Mitigation |
|------|-----------|
| Limited public data | Start with 30-50 commodities; mark every value with source |
| Shelf-life estimates may be wrong | Show ranges, label as estimates, validate against published cases |
| Prices change | Editable price table with date stamps |
| LLM may give wrong facts | Ground answers with RAG; refuse when no source found (template engine avoids this) |
| Regulation changes | Rules stored as data with citations, easy to update |
