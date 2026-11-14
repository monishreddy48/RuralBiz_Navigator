import pytest
from backend.app.api.voice import (
    generate_grounded_voice_response,
    SUPPORTED_VOICE_LANGUAGES,
    VoiceQueryRequest
)

def test_voice_supported_languages():
    assert "kn" in SUPPORTED_VOICE_LANGUAGES
    assert "te" in SUPPORTED_VOICE_LANGUAGES
    assert "hi" in SUPPORTED_VOICE_LANGUAGES
    assert "en" in SUPPORTED_VOICE_LANGUAGES
    assert SUPPORTED_VOICE_LANGUAGES["kn"]["locale"] == "kn-IN"
    assert SUPPORTED_VOICE_LANGUAGES["te"]["locale"] == "te-IN"
    assert SUPPORTED_VOICE_LANGUAGES["hi"]["locale"] == "hi-IN"
    assert SUPPORTED_VOICE_LANGUAGES["en"]["locale"] == "en-IN"

def test_kannada_voice_grounding():
    context = {
        "expected_investment": 1200000,
        "own_contribution": 360000,
        "monthly_emi": 18500,
        "dscr": 1.65,
        "score": 82.5,
        "feasibility_label": "ಉತ್ತಮ ಕಾರ್ಯಸಾಧ್ಯತೆ",
        "business_category": "ಕೃಷಿ ಸಂಸ್ಕರಣೆ",
        "village": "ತುಮಕೂರು ಗ್ರಾಮೀಣ"
    }
    reply, follow_ups = generate_grounded_voice_response("ನನ್ನ ಸಾಲದ ಇಎಂಐ ಎಷ್ಟು?", context, "kn")
    assert "18,500" in reply
    assert "1.65" in reply
    assert len(follow_ups) >= 2
    assert any("ಸಬ್ಸಿಡಿ" in f or "ಪಿಎಮ್‌ಇಜಿಪಿ" in f for f in follow_ups)

def test_telugu_voice_grounding():
    context = {
        "project_cost": 1500000,
        "own_contribution": 450000,
        "monthly_emi": 22300,
        "dscr": 1.58,
        "score": 85.0,
        "feasibility_label": "అత్యధిక సాధ్యత",
        "business_category": "డైరీ ప్రాసెసింగ్",
        "village": "విజయవాడ రూరల్"
    }
    reply, follow_ups = generate_grounded_voice_response("నాకు పిఎమ్‌ఇజిపి సబ్సిడీ ఎంత లభిస్తుంది?", context, "te")
    assert "35%" in reply or "పిఎమ్‌ఇజిపి" in reply
    assert "1,500,000" in reply
    assert len(follow_ups) >= 2

def test_hindi_voice_grounding():
    context = {
        "project_cost": 500000,
        "own_contribution": 100000,
        "monthly_emi": 8200,
        "dscr": 1.42,
        "score": 76.0,
        "feasibility_label": "सकारात्मक",
        "business_category": "ग्रामीण खुदरा स्टोर",
        "village": "रामपुर"
    }
    reply, follow_ups = generate_grounded_voice_response("क्या यह व्यवसाय मेरे गाँव में सुरक्षित है?", context, "hi")
    assert "रामपुर" in reply
    assert len(follow_ups) >= 2

def test_english_voice_grounding():
    context = {
        "project_cost": 800000,
        "own_contribution": 200000,
        "monthly_emi": 12800,
        "dscr": 1.72,
        "score": 88.0,
        "feasibility_label": "Highly Feasible",
        "business_category": "Custom Hiring Centre",
        "village": "Dharwad Rural"
    }
    reply, follow_ups = generate_grounded_voice_response("Can I afford this monthly EMI?", context, "en")
    assert "12,800" in reply
    assert "1.72" in reply
    assert "tenure" in reply.lower() or "dscr" in reply.lower()
    assert len(follow_ups) >= 2
