"""
RuralBiz Navigator - Database Manager
Handles SQLite connection, schema migration, seed data ingestion from CSV/JSON.
"""
import sqlite3
import json
import logging
from pathlib import Path
import pandas as pd
from config import DB_PATH, DATABASE_DIR, DATA_DIR

logger = logging.getLogger(__name__)

def get_connection() -> sqlite3.Connection:
    """Return an active connection to the SQLite database with row factory enabled."""
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def init_db(force: bool = False):
    """
    Initialize SQLite database schema and populate seed data from data/ CSVs and JSON.
    Idempotent and resilient.
    """
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    schema_path = DATABASE_DIR / "schema.sql"
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Execute Schema
    if schema_path.exists():
        with open(schema_path, "r", encoding="utf-8") as f:
            cursor.executescript(f.read())
        conn.commit()
    
    # 2. Ingest Localities
    cursor.execute("SELECT COUNT(*) FROM localities")
    if cursor.fetchone()[0] == 0 or force:
        localities_file = DATA_DIR / "localities.csv"
        if localities_file.exists():
            df_loc = pd.read_csv(localities_file)
            cursor.execute("DELETE FROM localities")
            for _, row in df_loc.iterrows():
                cursor.execute("""
                    INSERT INTO localities (
                        village_id, village_name, district, state, latitude, longitude,
                        population, households, average_household_size, market_distance_km,
                        nearest_town_distance_km, road_access_score, public_transport_score,
                        internet_access_score, bank_access_score, weekly_market_frequency,
                        agriculture_dependency, livestock_dependency, local_demand_index,
                        purchasing_power_index, is_prototype
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(row['village_id']), str(row['village_name']), str(row['district']), str(row['state']),
                    float(row['latitude']), float(row['longitude']), int(row['population']), int(row['households']),
                    float(row['average_household_size']), float(row['market_distance_km']), float(row['nearest_town_distance_km']),
                    float(row['road_access_score']), float(row['public_transport_score']), float(row['internet_access_score']),
                    float(row['bank_access_score']), int(row['weekly_market_frequency']), float(row['agriculture_dependency']),
                    float(row['livestock_dependency']), float(row['local_demand_index']), float(row['purchasing_power_index']),
                    1 if str(row.get('is_prototype', True)).lower() in ['true', '1'] else 0
                ))
            conn.commit()

    # 3. Ingest Businesses & Benchmarks
    cursor.execute("SELECT COUNT(*) FROM businesses")
    if cursor.fetchone()[0] == 0 or force:
        benchmarks_file = DATA_DIR / "business_benchmarks.csv"
        if benchmarks_file.exists():
            df_biz = pd.read_csv(benchmarks_file)
            cursor.execute("DELETE FROM businesses")
            for _, row in df_biz.iterrows():
                cursor.execute("""
                    INSERT INTO businesses (
                        business_id, business_name, category, typical_capex, typical_working_capital,
                        monthly_fixed_cost, variable_cost_ratio, typical_monthly_sales, typical_margin,
                        break_even_months, risk_level, skill_requirement, market_dependency,
                        growth_potential, unit_price_estimate, typical_monthly_units, data_source_label
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(row['business_id']), str(row['business_name']), str(row['category']),
                    float(row['typical_capex']), float(row['typical_working_capital']),
                    float(row['monthly_fixed_cost']), float(row['variable_cost_ratio']),
                    float(row['typical_monthly_sales']), float(row['typical_margin']),
                    int(row['break_even_months']), str(row['risk_level']), str(row['skill_requirement']),
                    str(row['market_dependency']), str(row['growth_potential']),
                    float(row.get('unit_price_estimate', 100)), float(row.get('typical_monthly_units', 500)),
                    str(row.get('data_source_label', 'Prototype benchmark / simulated data'))
                ))
            conn.commit()

    # 4. Ingest Competitors
    cursor.execute("SELECT COUNT(*) FROM competitors")
    if cursor.fetchone()[0] == 0 or force:
        comp_file = DATA_DIR / "competitors.csv"
        if comp_file.exists():
            df_comp = pd.read_csv(comp_file)
            cursor.execute("DELETE FROM competitors")
            for _, row in df_comp.iterrows():
                cursor.execute("""
                    INSERT INTO competitors (
                        competitor_id, locality_id, business_type, business_name,
                        latitude, longitude, estimated_monthly_sales, price_level,
                        customer_rating, distance_from_center, strength, weakness, is_prototype
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    str(row['competitor_id']), str(row['locality_id']), str(row['business_type']),
                    str(row['business_name']), float(row['latitude']), float(row['longitude']),
                    float(row['estimated_monthly_sales']), str(row['price_level']), float(row['customer_rating']),
                    float(row['distance_from_center']), str(row['strength']), str(row['weakness']),
                    1 if str(row.get('is_prototype', True)).lower() in ['true', '1'] else 0
                ))
            conn.commit()

    # 5. Ingest Schemes
    cursor.execute("SELECT COUNT(*) FROM schemes")
    if cursor.fetchone()[0] == 0 or force:
        schemes_file = DATA_DIR / "schemes.json"
        if schemes_file.exists():
            with open(schemes_file, "r", encoding="utf-8") as sf:
                schemes_data = json.load(sf)
            cursor.execute("DELETE FROM schemes")
            for s in schemes_data:
                cursor.execute("""
                    INSERT INTO schemes (
                        scheme_id, name, description, target_group, business_types,
                        min_project_cost, max_project_cost, loan_available, subsidy_available,
                        margin_requirement, interest_notes, collateral_notes, application_route,
                        documents, source_url, last_verified_date, verification_status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    s['scheme_id'], s['name'], s['description'], s['target_group'],
                    json.dumps(s['business_types']), float(s['min_project_cost']), float(s['max_project_cost']),
                    s['loan_available'], s['subsidy_available'], s['margin_requirement'],
                    s['interest_notes'], s['collateral_notes'], s['application_route'],
                    json.dumps(s['documents']), s['source_url'], s['last_verified_date'],
                    s['verification_status']
                ))
            conn.commit()
    
    conn.close()

def get_localities() -> pd.DataFrame:
    """Fetch all localities as a pandas DataFrame."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM localities", conn)
    conn.close()
    return df

def get_locality_by_id(village_id: str) -> dict:
    """Fetch a single locality by village_id as dict."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM localities WHERE village_id = ?", (village_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else {}

def get_businesses() -> pd.DataFrame:
    """Fetch all businesses/benchmarks as a pandas DataFrame."""
    conn = get_connection()
    df = pd.read_sql_query("SELECT * FROM businesses", conn)
    conn.close()
    return df

def get_business_by_category(category: str) -> dict:
    """Fetch a single business record by category name."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM businesses WHERE category = ? LIMIT 1", (category,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else {}

def get_competitors(locality_id: str = None, business_type: str = None) -> pd.DataFrame:
    """Fetch competitor records filtered by locality and/or business type."""
    conn = get_connection()
    query = "SELECT * FROM competitors WHERE 1=1"
    params = []
    if locality_id:
        query += " AND locality_id = ?"
        params.append(locality_id)
    if business_type:
        query += " AND business_type = ?"
        params.append(business_type)
    df = pd.read_sql_query(query, conn, params=params)
    conn.close()
    return df

def get_schemes() -> list[dict]:
    """Fetch all verified government schemes as list of dicts."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM schemes")
    rows = cursor.fetchall()
    conn.close()
    schemes = []
    for r in rows:
        d = dict(r)
        d['business_types'] = json.loads(d['business_types']) if isinstance(d['business_types'], str) else d['business_types']
        d['documents'] = json.loads(d['documents']) if isinstance(d['documents'], str) else d['documents']
        schemes.append(d)
    return schemes

def save_assessment(assessment_data: dict) -> str:
    """Save an entrepreneur assessment record into SQLite."""
    import uuid
    assessment_id = assessment_data.get("assessment_id") or f"ASM_{uuid.uuid4().hex[:8].upper()}"
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO assessments (
            assessment_id, user_id, locality_id, business_id, own_capital,
            expected_investment, experience_level, is_existing_business,
            monthly_household_income, risk_tolerance, viability_score, recommendation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        assessment_id,
        assessment_data.get("user_id", "ANON_USER"),
        assessment_data["locality_id"],
        assessment_data["business_id"],
        float(assessment_data.get("own_capital", 0)),
        float(assessment_data.get("expected_investment", 0)),
        assessment_data.get("experience_level", "Beginner"),
        1 if assessment_data.get("is_existing_business") else 0,
        float(assessment_data.get("monthly_household_income", 0)),
        assessment_data.get("risk_tolerance", "Moderate"),
        float(assessment_data.get("viability_score", 0)),
        assessment_data.get("recommendation", "MODIFY")
    ))
    conn.commit()
    conn.close()
    return assessment_id
