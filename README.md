# PackSmart

AI-Based Intelligent Food Packaging Material Recommendation System

**SIH26236** | Ministry of Food Processing Industries | Agriculture, FoodTech & Rural Development

## Problem

Small food processors (MSMEs, FPOs, women self-help groups) rarely have packaging experts. Wrong packaging choices cause spoilage, moisture gain, rancidity, higher cost, non-compliance with food-contact rules, or plastic waste.

## Solution

PackSmart recommends the most suitable packaging material for a food commodity by:

1. Filtering out unsafe/unsuitable materials (hard constraints)
2. Ranking remaining options on barrier match, shelf-life fit, cost, sustainability, practicality
3. Predicting shelf life using Labuza moisture-uptake and Q10 oxidation models
4. Checking FSSAI/BIS regulatory compliance
5. Generating plain-language explanations and downloadable PDF reports

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, FastAPI, SQLAlchemy, SQLite |
| Frontend | React, Tailwind CSS, Vite |
| Shelf-life | Labuza moisture-uptake model, Q10 oxidation model |
| PDF | ReportLab |
| Deployment | Docker, Docker Compose |

## Project Structure

```
PackSmart/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app
│   │   ├── auth.py              # Admin token auth
│   │   ├── config.py            # Settings
│   │   ├── database.py          # SQLAlchemy setup
│   │   ├── seed_data.py         # Knowledge base loader
│   │   ├── models/              # DB models
│   │   ├── schemas/             # Pydantic validation
│   │   ├── routes/              # API endpoints
│   │   └── services/            # Engine (filter, score, shelf-life, compliance, explain)
│   ├── data/                    # JSON seed data (42 foods, 21 materials, 20 rules)
│   ├── tests/                   # 19 acceptance tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main app with i18n
│   │   ├── api.js               # API client
│   │   ├── translations.js      # English + Hindi
│   │   └── components/          # React components
│   └── package.json
├── docker-compose.yml
└── .env.example
```

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
python -m app.seed_data
python -m uvicorn app.main:app --reload --port 8000
```

API docs: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

### Docker

```bash
docker-compose up --build
```

## Environment Variables

Copy `.env.example` to `backend/.env`:

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | SQLite database path | `sqlite:///./packsmart.db` |
| `ADMIN_TOKEN` | Auth token for admin API routes | `packsmart-admin-change-me` |
| `CORS_ORIGINS` | Comma-separated allowed origins | `http://localhost:5173,http://localhost:3000` |

## Admin API

POST/PUT/DELETE routes on `/api/commodities/`, `/api/materials/`, `/api/rules/` require the `X-Admin-Token` header:

```bash
curl -H "X-Admin-Token: packsmart-admin-change-me" -X POST http://localhost:8000/api/commodities/ -H "Content-Type: application/json" -d '{...}'
```

## Knowledge Base

- **42 food commodities** across 9 categories (Snacks, Fresh Produce, Dairy, Grains, Confections, Beverages, Oils & Pickles, Meat & Fish, Dry Fruits)
- **21 packaging materials** (LDPE, HDPE, PP, PET, BOPP, MetPET, Al laminate, glass, tinplate, etc.)
- **20 compliance rules** (FSSAI Packaging Regulations 2018, Plastic Waste Management Rules 2016, BIS standards)

All data values include source citations from published literature.

## Testing

```bash
cd backend
python -m pytest tests/test_acceptance.py -v
```

## SRS Compliance

See `SRS.md` for the full Software Requirements Specification.

**Note:** The chat assistant (FR-7.2) from the SRS is implemented as a template-based explanation engine rather than an LLM-powered chat, since no external LLM API dependency was desired for the prototype.

## License

MIT
