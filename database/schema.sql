-- RuralBiz Navigator SQLite Schema
-- SIH26091 / PS 91

CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    name TEXT,
    state TEXT,
    district TEXT,
    village TEXT,
    preferred_language TEXT DEFAULT 'en',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS localities (
    village_id TEXT PRIMARY KEY,
    village_name TEXT NOT NULL,
    district TEXT NOT NULL,
    state TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    population INTEGER NOT NULL,
    households INTEGER NOT NULL,
    average_household_size REAL,
    market_distance_km REAL,
    nearest_town_distance_km REAL,
    road_access_score REAL,
    public_transport_score REAL,
    internet_access_score REAL,
    bank_access_score REAL,
    weekly_market_frequency INTEGER,
    agriculture_dependency REAL,
    livestock_dependency REAL,
    local_demand_index REAL,
    purchasing_power_index REAL,
    is_prototype BOOLEAN DEFAULT 1
);

CREATE TABLE IF NOT EXISTS businesses (
    business_id TEXT PRIMARY KEY,
    business_name TEXT NOT NULL,
    category TEXT NOT NULL,
    typical_capex REAL NOT NULL,
    typical_working_capital REAL NOT NULL,
    monthly_fixed_cost REAL NOT NULL,
    variable_cost_ratio REAL NOT NULL,
    typical_monthly_sales REAL NOT NULL,
    typical_margin REAL NOT NULL,
    break_even_months INTEGER,
    risk_level TEXT,
    skill_requirement TEXT,
    market_dependency TEXT,
    growth_potential TEXT,
    unit_price_estimate REAL,
    typical_monthly_units REAL,
    data_source_label TEXT
);

CREATE TABLE IF NOT EXISTS competitors (
    competitor_id TEXT PRIMARY KEY,
    locality_id TEXT NOT NULL,
    business_type TEXT NOT NULL,
    business_name TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    estimated_monthly_sales REAL,
    price_level TEXT,
    customer_rating REAL,
    distance_from_center REAL,
    strength TEXT,
    weakness TEXT,
    is_prototype BOOLEAN DEFAULT 1,
    FOREIGN KEY (locality_id) REFERENCES localities(village_id)
);

CREATE TABLE IF NOT EXISTS schemes (
    scheme_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    target_group TEXT,
    business_types TEXT,
    min_project_cost REAL,
    max_project_cost REAL,
    loan_available TEXT,
    subsidy_available TEXT,
    margin_requirement TEXT,
    interest_notes TEXT,
    collateral_notes TEXT,
    application_route TEXT,
    documents TEXT,
    source_url TEXT,
    last_verified_date TEXT,
    verification_status TEXT
);

CREATE TABLE IF NOT EXISTS assessments (
    assessment_id TEXT PRIMARY KEY,
    user_id TEXT,
    locality_id TEXT NOT NULL,
    business_id TEXT NOT NULL,
    own_capital REAL NOT NULL,
    expected_investment REAL NOT NULL,
    experience_level TEXT,
    is_existing_business BOOLEAN DEFAULT 0,
    monthly_household_income REAL,
    risk_tolerance TEXT,
    viability_score REAL,
    recommendation TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (locality_id) REFERENCES localities(village_id),
    FOREIGN KEY (business_id) REFERENCES businesses(business_id)
);

CREATE TABLE IF NOT EXISTS financial_scenarios (
    scenario_id TEXT PRIMARY KEY,
    assessment_id TEXT,
    scenario_type TEXT DEFAULT 'BASE', -- 'BASE' or 'STRESS'
    project_cost REAL,
    own_contribution REAL,
    loan_amount REAL,
    interest_rate REAL,
    tenure_months INTEGER,
    monthly_sales REAL,
    variable_costs REAL,
    fixed_costs REAL,
    monthly_emi REAL,
    net_monthly_profit REAL,
    break_even_revenue REAL,
    dscr REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id)
);

CREATE TABLE IF NOT EXISTS reports (
    report_id TEXT PRIMARY KEY,
    assessment_id TEXT,
    report_file_path TEXT,
    generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id)
);
