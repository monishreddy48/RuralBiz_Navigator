"""
RuralBiz Navigator - Multilingual Translation System (i18n)
Supports English, Hindi, Telugu, and Kannada with graceful English fallback.
"""
from typing import Dict

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    # Navigation & General
    "app_title": {
        "en": "RuralBiz Navigator",
        "hi": "रूरलबिज़ नेविगेटर",
        "te": "రూరల్‌బిజ్ నేవిగేటర్",
        "kn": "ರೂರಲ್‍ಬಿಜ್ ನ್ಯಾವಿಗೇಟರ್"
    },
    "tagline": {
        "en": "Know your market. Know your money. Make a better business decision.",
        "hi": "अपना बाज़ार जानें। अपना पैसा समझें। बेहतर व्यावसायिक निर्णय लें।",
        "te": "మీ మార్కెట్‌ను తెలుసుకోండి. మీ డబ్బును లెక్కించండి. సరైన వ్యాపార నిర్ణయం తీసుకోండి.",
        "kn": "ನಿಮ್ಮ ಮಾರುಕಟ್ಟೆಯನ್ನು ತಿಳಿಯಿರಿ. ನಿಮ್ಮ ಹಣವನ್ನು ತಿಳಿಯಿರಿ. ಉತ್ತಮ ವ್ಯಾಪಾರ ನಿರ್ಧಾರ ತೆಗೆದುಕೊಳ್ಳಿ."
    },
    "nav_home": {
        "en": "Home / Dashboard",
        "hi": "होम / डैशबोर्ड",
        "te": "హోమ్ / డాష్‌బోర్డ్",
        "kn": "ಮುಖಪುಟ / ಡ್ಯಾಶ್‌ಬೋರ್ಡ್"
    },
    "nav_feasibility": {
        "en": "Business Feasibility",
        "hi": "व्यवसाय व्यवहार्यता",
        "te": "వ్యాపార సాధ్యత",
        "kn": "ವ್ಯವಹಾರ ಕಾರ್ಯಸಾಧ್ಯತೆ"
    },
    "nav_market": {
        "en": "Hyper-Local Market",
        "hi": "स्थानीय बाज़ार और प्रतिस्पर्धी",
        "te": "స్థానిక మార్కెట్ & పోటీదారులు",
        "kn": "ಸ್ಥಳೀಯ ಮಾರುಕಟ್ಟೆ & ಸ್ಪರ್ಧಿಗಳು"
    },
    "nav_financial": {
        "en": "Financial Calculator",
        "hi": "वित्तीय कैलकुलेटर व ईएमआई",
        "te": "ఆర్థిక కాలిక్యులేటర్ & ఈఎంఐ",
        "kn": "ಹಣಕಾಸು ಕ್ಯಾಲ್ಕುಲೇಟರ್ & ಇಎಂಐ"
    },
    "nav_whatif": {
        "en": "What-If Simulator",
        "hi": "क्या-यदि सिमुलेटर",
        "te": "వాట్-ఇఫ్ సిమ్యులేటర్",
        "kn": "ವಾಟ್-ಇಫ್ ಸಿಮ್ಯುಲೇಟರ್"
    },
    "nav_schemes": {
        "en": "Scheme Navigator",
        "hi": "सरकारी योजनाएं",
        "te": "ప్రభుత్వ పథకాల నావిగేటర్",
        "kn": "ಸರ್ಕಾರಿ ಯೋಜನೆಗಳ ನ್ಯಾವಿಗೇಟರ್"
    },
    "nav_alternatives": {
        "en": "Business Alternatives",
        "hi": "वैकल्पिक व्यवसाय",
        "te": "ప్రత్యామ్నాయ వ్యాపారాలు",
        "kn": "ಪರ್ಯಾಯ ವ್ಯವಹಾರಗಳು"
    },
    "nav_ai": {
        "en": "AI Assistant",
        "hi": "एआई सलाहकार",
        "te": "AI సలహాదారు",
        "kn": "AI ಸಹಾಯಕ"
    },
    "nav_dpr": {
        "en": "DPR / Business Report",
        "hi": "डीपीआर / व्यापार रिपोर्ट",
        "te": "DPR / వ్యాపార నివేదిక",
        "kn": "DPR / ವ್ಯಾಪಾರ ವರದಿ"
    },
    "nav_about": {
        "en": "About & Disclaimer",
        "hi": "परिचय व अस्वीकरण",
        "te": "గురించి & నిరాకరణ",
        "kn": "ಬಗ್ಗೆ & ಹಕ್ಕುತ್ಯಾಗ"
    },

    # CTA & Buttons
    "cta_start_assessment": {
        "en": "Start Business Assessment",
        "hi": "व्यवसाय मूल्यांकन शुरू करें",
        "te": "వ్యాపార అంచనాను ప్రారంభించండి",
        "kn": "ವ್ಯಾಪಾರ ಮೌಲ್ಯಮಾಪನ ಪ್ರಾರಂಭಿಸಿ"
    },
    "cta_explore_opps": {
        "en": "Explore Opportunities",
        "hi": "अवसर तलाशें",
        "te": "అవకాశాలను అన్వేషించండి",
        "kn": "ಅವಕಾಶಗಳನ್ನು ಅನ್ವೇಷಿಸಿ"
    },
    "btn_load_demo": {
        "en": "Load Demo Entrepreneur",
        "hi": "डेमो उद्यमी लोड करें",
        "te": "డెమో వ్యవస్థాపకుడిని లోడ్ చేయండి",
        "kn": "ಡೆಮೊ ಉದ್ಯಮಿಯನ್ನು ಲೋಡ್ ಮಾಡಿ"
    },
    "btn_run_assessment": {
        "en": "Analyze Viability",
        "hi": "व्यवहार्यता का विश्लेषण करें",
        "te": "సాధ్యతను విశ్లేషించండి",
        "kn": "ಕಾರ್ಯಸಾಧ್ಯತೆಯನ್ನು ವಿಶ್ಲೇಷಿಸಿ"
    },
    "btn_download_pdf": {
        "en": "Download Official DPR (PDF)",
        "hi": "आधिकारिक डीपीआर (PDF) डाउनलोड करें",
        "te": "అధికారిక DPR (PDF) డౌన్‌లోడ్ చేయండి",
        "kn": "ಅಧಿಕೃತ DPR (PDF) ಡೌನ್‌ಲೋಡ್ ಮಾಡಿ"
    },

    # Cards on Home
    "card_market_opp": {
        "en": "Market Opportunity",
        "hi": "बाज़ार का अवसर",
        "te": "మార్కెట్ అవకాశం",
        "kn": "ಮಾರುಕಟ್ಟೆ ಅವಕಾಶ"
    },
    "card_market_opp_desc": {
        "en": "Evaluate rural customer density, purchasing power and competitor saturation in 5-10 km radius.",
        "hi": "5-10 किमी के दायरे में ग्रामीण ग्राहक घनत्व, क्रय शक्ति और प्रतिस्पर्धी संतृप्ति का मूल्यांकन करें।",
        "te": "5-10 కి.మీ పరిధిలో గ్రామీణ వినియోగదారుల సాంద్రత, కొనుగోలు శక్తి మరియు పోటీని అంచనా వేయండి.",
        "kn": "5-10 ಕಿಮೀ ವ್ಯಾಪ್ತಿಯಲ್ಲಿ ಗ್ರಾಹಕರ ಸಾಂದ್ರತೆ, ಕೊಳ್ಳುವ ಶಕ್ತಿ ಮತ್ತು ಸ್ಪರ್ಧೆಯನ್ನು ಮೌಲ್ಯಮಾಪನ ಮಾಡಿ."
    },
    "card_fin_readiness": {
        "en": "Financial Readiness",
        "hi": "वित्तीय तत्परता",
        "te": "ఆర్థిక సంసిద్ధత",
        "kn": "ಹಣಕಾಸು ಸಿದ್ಧತೆ"
    },
    "card_fin_readiness_desc": {
        "en": "Calculate realistic CapEx, working capital, reducing-balance EMI and monthly debt servicing capability.",
        "hi": "वास्तविक पूंजीगत व्यय, कार्यशील पूंजी, ईएमआई और ऋण चुकाने की क्षमता की सटीक गणना करें।",
        "te": "వాస్తవిక మూలధనం, నిర్వహణ నిధులు, EMI మరియు రుణ చెల్లింపు సామర్థ్యాన్ని లెక్కించండి.",
        "kn": "ವಾಸ್ತವಿಕ ಬಂಡವಾಳ, ಕಾರ್ಯನಿರತ ಬಂಡವಾಳ, ಇಎಂಐ ಮತ್ತು ಸಾಲ ಮರುಪಾವತಿ ಸಾಮರ್ಥ್ಯವನ್ನು ಲೆಕ್ಕಹಾಕಿ."
    },
    "card_funding_options": {
        "en": "Funding & Schemes",
        "hi": "वित्त पोषण और योजनाएं",
        "te": "నిధులు & పథకాలు",
        "kn": "ನಿಧಿಗಳು & ಯೋಜನೆಗಳು"
    },
    "card_funding_options_desc": {
        "en": "Direct rule-based matching with verified government credit schemes like PMEGP, MUDRA and PMFME.",
        "hi": "पीएमईजीपी, मुद्रा और पीएमएफएमई जैसी सत्यापित सरकारी योजनाओं के साथ सीधा नियम-आधारित मिलान।",
        "te": "PMEGP, MUDRA మరియు PMFME వంటి ప్రభుత్వ పథకాలతో అర్హత సరిపోలిక.",
        "kn": "PMEGP, ಮುದ್ರಾ ಮತ್ತು PMFME ನಂತಹ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳೊಂದಿಗೆ ನಿಯಮ ಆಧಾರಿತ ಹೊಂದಾಣಿಕೆ."
    },
    "card_business_risk": {
        "en": "Business Risk & Stress",
        "hi": "व्यावसायिक जोखिम व तनाव",
        "te": "వ్యాపార ప్రమాదం & ఒత్తిడి",
        "kn": "ವ್ಯಾಪಾರ ಅಪಾಯ & ಒತ್ತಡ"
    },
    "card_business_risk_desc": {
        "en": "Stress test your business model: Will you survive if sales drop 20% or raw material costs rise 15%?",
        "hi": "तनाव परीक्षण: क्या आपका व्यवसाय टिकेगा यदि बिक्री 20% गिर जाए या लागत 15% बढ़ जाए?",
        "te": "ఒత్తిడి పరీక్ష: అమ్మకాలు 20% తగ్గినా లేదా ముడిసరుకు ఖర్చు 15% పెరిగినా వ్యాపారం నిలబడుతుందా?",
        "kn": "ಒತ್ತಡ ಪರೀಕ್ಷೆ: ಮಾರಾಟ 20% ಕುಸಿದರೆ ಅಥವಾ ಕಚ್ಚಾ ವಸ್ತುಗಳ ವೆಚ್ಚ 15% ಹೆಚ್ಚಾದರೆ ನಿಮ್ಮ ವ್ಯಾಪಾರ ಉಳಿಯುವುದೇ?"
    },

    # Core Form Fields
    "lbl_select_locality": {
        "en": "Select Village / Locality",
        "hi": "गांव / स्थानीय क्षेत्र चुनें",
        "te": "గ్రామం / ప్రాంతాన్ని ఎంచుకోండి",
        "kn": "ಗ್ರಾಮ / ಪ್ರದೇಶವನ್ನು ಆಯ್ಕೆಮಾಡಿ"
    },
    "lbl_select_business": {
        "en": "Select Business Category",
        "hi": "व्यवसाय श्रेणी चुनें",
        "te": "వ్యాపార విభాగాన్ని ఎంచుకోండి",
        "kn": "ವ್ಯವಹಾರ ವರ್ಗವನ್ನು ಆಯ್ಕೆಮಾಡಿ"
    },
    "lbl_own_capital": {
        "en": "Available Own Capital (₹)",
        "hi": "उपलब्ध स्वयं की पूंजी (₹)",
        "te": "అందుబాటులో ఉన్న సొంత మూలధనం (₹)",
        "kn": "ಲಭ್ಯವಿರುವ ಸ್ವಂತ ಬಂಡವಾಳ (₹)"
    },
    "lbl_expected_investment": {
        "en": "Total Expected Project Cost (₹)",
        "hi": "कुल अपेक्षित परियोजना लागत (₹)",
        "te": "మొత్తం అంచనా ప్రాజెక్ట్ ఖర్చు (₹)",
        "kn": "ಒಟ್ಟು ಅಂದಾಜು ಯೋಜನೆ ವೆಚ್ಚ (₹)"
    },
    "lbl_experience": {
        "en": "Prior Business Experience",
        "hi": "पूर्व व्यावसायिक अनुभव",
        "te": "మునుపటి వ్యాపార అనుభవం",
        "kn": "ಹಿಂದಿನ ವ್ಯಾಪಾರ ಅನುಭವ"
    },
    "lbl_existing_biz": {
        "en": "Is this an Existing Business?",
        "hi": "क्या यह पहले से चल रहा व्यवसाय है?",
        "te": "ఇది ఇప్పటికే ఉన్న వ్యాపారమా?",
        "kn": "ಇದು ಈಗಾಗಲೇ ಇರುವ ವ್ಯವಹಾರವೇ?"
    },
    "lbl_risk_tolerance": {
        "en": "Risk Tolerance",
        "hi": "जोखिम सहने की क्षमता",
        "te": "రిస్క్ తీసుకునే సామర్థ్యం",
        "kn": "ಅಪಾಯ ಸಹಿಷ್ಣುತೆ"
    },

    # Recommendations
    "rec_go": {
        "en": "GO - RECOMMENDED",
        "hi": "आगे बढ़ें (GO) - अनुशंसित",
        "te": "ముందుకు సాగండి (GO) - సిఫార్సు చేయబడింది",
        "kn": "ಮುಂದುವರಿಯಿರಿ (GO) - ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ"
    },
    "rec_modify": {
        "en": "MODIFY - ADJUST STRUCTURE",
        "hi": "संशोधन करें (MODIFY) - योजना में बदलाव करें",
        "te": "మార్పులు చేయండి (MODIFY) - సర్దుబాటు అవసరం",
        "kn": "ಮಾರ್ಪಡಿಸಿ (MODIFY) - ರಚನೆಯಲ್ಲಿ ಬದಲಾವಣೆ ಮಾಡಿ"
    },
    "rec_avoid": {
        "en": "AVOID - HIGH RISK",
        "hi": "बचें (AVOID) - उच्च जोखिम",
        "te": "నివారించండి (AVOID) - అధిక రిస్క్",
        "kn": "ತಪ್ಪಿಸಿ (AVOID) - ಹೆಚ್ಚಿನ ಅಪಾಯ"
    },

    # Financial Labels
    "lbl_monthly_sales": {
        "en": "Monthly Projected Revenue",
        "hi": "मासिक अनुमानित आय",
        "te": "నెలవారీ అంచనా రాబడి",
        "kn": "ಮಾಸಿಕ ಅಂದಾಜು ಆದಾಯ"
    },
    "lbl_monthly_emi": {
        "en": "Monthly Loan EMI",
        "hi": "मासिक ऋण ईएमआई",
        "te": "నెలవారీ లోన్ ఈఎంఐ",
        "kn": "ಮಾಸಿಕ ಸಾಲ ಇಎಂಐ"
    },
    "lbl_net_profit": {
        "en": "Net Monthly Cash Flow",
        "hi": "शुद्ध मासिक नकदी प्रवाह",
        "te": "నికర నెలవారీ నగదు ప్రవాహం",
        "kn": "ನಿವ್ವಳ ಮಾಸಿಕ ನಗದು ಹರಿವು"
    },
    "lbl_break_even": {
        "en": "Break-Even Revenue",
        "hi": "ब्रेक-इवन (लागत-संतुलन) आय",
        "te": "బ్రేక్-ఈవెన్ రాబడి",
        "kn": "ಬ್ರೇಕ್-ಈವನ್ ಆದಾಯ"
    },
    "lbl_dscr": {
        "en": "Debt Service Coverage (DSCR)",
        "hi": "ऋण सेवा कवरेज अनुपात (DSCR)",
        "te": "రుణ సేవా కవరేజ్ (DSCR)",
        "kn": "ಸಾಲ ಸೇವಾ ಕವರೇಜ್ (DSCR)"
    },

    # Disclaimers
    "disclaimer_text": {
        "en": "RuralBiz Navigator provides informational and decision-support estimates based on available data and prototype assumptions. It does not constitute financial, legal, investment or lending advice and does not guarantee business success, scheme eligibility, loan approval or returns.",
        "hi": "रूरलबिज़ नेविगेटर उपलब्ध डेटा और प्रोटोटाइप मान्यताओं के आधार पर सूचनात्मक और निर्णय-समर्थन अनुमान प्रदान करता है। यह वित्तीय, कानूनी या ऋण सलाह नहीं है और व्यावसायिक सफलता या ऋण स्वीकृति की गारंटी नहीं देता है।",
        "te": "రూరల్‌బిజ్ నేవిగేటర్ అందుబాటులో ఉన్న డేటా మరియు నమూనా అంచనాల ఆధారంగా సమాచారాన్ని అందిస్తుంది. ఇది బ్యాంక్ రుణం లేదా లాభాలకు హామీ ఇవ్వదు.",
        "kn": "ರೂರಲ್‍ಬಿಜ್ ನ್ಯಾವಿಗೇಟರ್ ಲಭ್ಯವಿರುವ ಡೇಟಾ ಆಧಾರದ ಮೇಲೆ ಮಾಹಿತಿಯನ್ನು ಒದಗಿಸುತ್ತದೆ. ಇದು ಹಣಕಾಸು ಅಥವಾ ಕಾನೂನು ಸಲಹೆಯಲ್ಲ ಮತ್ತು ಸಾಲ ಅನುಮೋದನೆಯನ್ನು ಖಾತರಿಪಡಿಸುವುದಿಲ್ಲ."
    },
    "prototype_data_note": {
        "en": "Prototype simulated data — for demonstration only.",
        "hi": "प्रोटोटाइप सिम्युलेटेड डेटा — केवल प्रदर्शन उद्देश्यों के लिए।",
        "te": "నమూనా సిమ్యులేటెడ్ డేటా — ప్రదర్శన కోసం మాత్రమే.",
        "kn": "ಮಾದರಿ ಸಿಮ್ಯುಲೇಟೆಡ್ ಡೇಟಾ — ಕೇವಲ ಪ್ರದರ್ಶನಕ್ಕಾಗಿ ಮಾತ್ರ."
    }
}

def t(key: str, lang: str = "en") -> str:
    """
    Translates key to requested language.
    Gracefully falls back to English if key or language is missing.
    """
    key_dict = TRANSLATIONS.get(key)
    if not key_dict:
        return key.replace("_", " ").title()
    return key_dict.get(lang, key_dict.get("en", key))
