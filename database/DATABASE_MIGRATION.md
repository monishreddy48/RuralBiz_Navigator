# 🗄️ RuralBiz Navigator — Multi-User Database Migration Strategy

> **Production Storage Roadmap from SQLite (`app.db`) to PostgreSQL (Cloud SQL / Supabase / Neon)**  
> *SIH 2026 Problem Statement SIH26091 / PS 91*

---

## 1. Overview & Current Architecture

In the initial prototype and evaluation phase, RuralBiz Navigator uses **SQLite 3 (`database/app.db`)** with WAL (Write-Ahead Logging) enabled.

- **Pros in Development**: Zero-configuration, embeds directly in the repository, portable for offline judging.
- **Constraints in Multi-Tenant Production**:
  - File locking under concurrent write bursts (e.g. 5,000 rural entrepreneurs concurrently generating DPRs).
  - Lack of horizontal read-replica scaling.
  - No native Row-Level Security (RLS) for tenant isolation.

---

## 2. Target Production Stack: PostgreSQL 16+

For state-wide deployment (e.g. National Rural Livelihoods Mission or Ministry of MSME portal):

- **Engine**: Managed PostgreSQL 16 on **Google Cloud SQL** or **Supabase** / **AWS RDS**.
- **ORM / Query Layer**: **SQLAlchemy 2.0+** with `asyncpg` async driver.
- **Migration Engine**: **Alembic** versioned schema migrations.
- **Connection Pooling**: **PgBouncer** (pooling 500+ micro-service backend worker instances).

---

## 3. Schema Relational Design

```
+-------------------------------------------------------------+
| users (Firebase UID primary key)                            |
|-------------------------------------------------------------|
| id VARCHAR(128) PRIMARY KEY                                 |
| email VARCHAR(255)                                          |
| full_name VARCHAR(255)                                      |
| state VARCHAR(100)                                          |
| district VARCHAR(100)                                       |
| village_locality VARCHAR(150)                               |
| preferred_language VARCHAR(10) DEFAULT 'en'                 |
| business_category VARCHAR(100)                              |
| business_stage VARCHAR(50)                                  |
| created_at TIMESTAMPTZ DEFAULT NOW()                        |
+-------------------------------------------------------------+
                              | 1
                              |
                              | N
+-------------------------------------------------------------+
| assessments                                                 |
|-------------------------------------------------------------|
| id UUID PRIMARY KEY DEFAULT gen_random_uuid()               |
| user_id VARCHAR(128) REFERENCES users(id) ON DELETE CASCADE |
| village_id VARCHAR(50) REFERENCES localities(village_id)    |
| category VARCHAR(100) REFERENCES businesses(category)       |
| expected_investment NUMERIC(14,2) NOT NULL                  |
| own_capital NUMERIC(14,2) NOT NULL                          |
| loan_amount NUMERIC(14,2) NOT NULL                          |
| interest_rate NUMERIC(5,2) DEFAULT 9.5                      |
| tenure_months INT DEFAULT 60                                |
| monthly_emi NUMERIC(12,2) NOT NULL                          |
| dscr NUMERIC(5,2) NOT NULL                                  |
| viability_score NUMERIC(5,2) NOT NULL                       |
| verdict VARCHAR(20) NOT NULL                                |
| evaluation_json JSONB NOT NULL                              |
| created_at TIMESTAMPTZ DEFAULT NOW()                        |
+-------------------------------------------------------------+
```

---

## 4. Step-by-Step Migration Process

### Step 1: Install PostgreSQL Driver
```bash
pip install asyncpg psycopg2-binary alembic
```

### Step 2: Configure Environment Connection String
In `.env`:
```env
# Local SQLite (Development)
DATABASE_URL=sqlite:///./database/app.db

# Cloud PostgreSQL (Production)
# DATABASE_URL=postgresql+asyncpg://user:password@cloud-sql-host:5432/ruralbiz
```

### Step 3: Run Alembic Database Migrations
```bash
alembic init alembic
alembic revision --autogenerate -m "Initial PostgreSQL schema"
alembic upgrade head
```

### Step 4: Data Seed Script (From CSV to PostgreSQL)
The existing CSVs in `data/` (`localities.csv`, `businesses.csv`, `competitors.csv`, `schemes.json`) seed directly via pandas:
```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(POSTGRES_URL)
pd.read_csv("data/localities.csv").to_sql("localities", engine, if_exists="append", index=False)
pd.read_csv("data/businesses.csv").to_sql("businesses", engine, if_exists="append", index=False)
pd.read_csv("data/competitors.csv").to_sql("competitors", engine, if_exists="append", index=False)
```

---

## 5. Security & Row-Level Security (RLS)

Enable Row-Level Security on the `assessments` table so that entrepreneurs can strictly query only their own business records:

```sql
ALTER TABLE assessments ENABLE ROW LEVEL SECURITY;

CREATE POLICY entrepreneur_isolation_policy ON assessments
    FOR ALL
    USING (user_id = current_setting('request.jwt.claim.sub', true));
```

