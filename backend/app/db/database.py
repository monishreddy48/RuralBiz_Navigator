"""
RuralBiz Navigator - Backend Database Access Layer
Provides clean data access for localities, businesses, competitors, and schemes.
"""
import sqlite3
import json
import logging
from typing import Dict, Any, List, Optional
import pandas as pd
from backend.app.config import DB_PATH, DATABASE_DIR, DATA_DIR

logger = logging.getLogger(__name__)

def get_db_connection() -> sqlite3.Connection:
    """Return an active connection to the SQLite database with Row factory."""
    DATABASE_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def get_localities() -> List[Dict[str, Any]]:
    """Fetch all locality records."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM localities ORDER BY village_name ASC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def get_locality_by_id(village_id: str) -> Optional[Dict[str, Any]]:
    """Fetch single locality by village_id."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM localities WHERE village_id = ?", (village_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def get_businesses() -> List[Dict[str, Any]]:
    """Fetch all business categories and benchmark profiles."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM businesses ORDER BY business_name ASC")
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def get_business_by_category(category: str) -> Optional[Dict[str, Any]]:
    """Fetch single business benchmark by category."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM businesses WHERE category = ? LIMIT 1", (category,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def get_competitors_df(locality_id: Optional[str] = None, business_type: Optional[str] = None) -> pd.DataFrame:
    """Return competitor entries as a Pandas DataFrame for engine calculations."""
    conn = get_db_connection()
    try:
        query = "SELECT * FROM competitors WHERE 1=1"
        params = []
        if locality_id:
            query += " AND locality_id = ?"
            params.append(locality_id)
        if business_type:
            query += " AND business_type = ?"
            params.append(business_type)
        return pd.read_sql_query(query, conn, params=params)
    finally:
        conn.close()

def get_schemes() -> List[Dict[str, Any]]:
    """Fetch government schemes with parsed documents and eligible business types."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM schemes ORDER BY min_project_cost ASC")
        rows = cursor.fetchall()
        results = []
        for row in rows:
            d = dict(row)
            if isinstance(d.get("business_types"), str):
                try:
                    d["business_types"] = json.loads(d["business_types"])
                except Exception:
                    d["business_types"] = [c.strip() for c in d["business_types"].split(",") if c.strip()]
            if isinstance(d.get("documents"), str):
                try:
                    d["documents"] = json.loads(d["documents"])
                except Exception:
                    d["documents"] = [doc.strip() for doc in d["documents"].split(",") if doc.strip()]
            results.append(d)
        return results
    finally:
        conn.close()

def save_assessment_record(assessment_dict: Dict[str, Any]) -> str:
    """Save an assessment evaluation to SQLite and return generated assessment_id."""
    import uuid
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        assessment_id = f"ASM_{uuid.uuid4().hex[:8].upper()}"
        cursor.execute("""
            INSERT INTO assessments (
                assessment_id, user_id, locality_id, business_id, own_capital,
                expected_investment, experience_level, is_existing_business,
                monthly_household_income, risk_tolerance, viability_score, recommendation
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            assessment_id,
            assessment_dict.get("user_id", "demo_guest"),
            assessment_dict["locality_id"],
            assessment_dict["business_id"],
            float(assessment_dict["own_capital"]),
            float(assessment_dict["expected_investment"]),
            assessment_dict.get("experience_level", "Intermediate"),
            1 if assessment_dict.get("is_existing_business") else 0,
            float(assessment_dict.get("monthly_household_income", 0.0)),
            assessment_dict.get("risk_tolerance", "Moderate"),
            float(assessment_dict.get("viability_score", 0.0)),
            assessment_dict.get("recommendation", "MODIFY")
        ))
        conn.commit()
        return assessment_id
    finally:
        conn.close()

