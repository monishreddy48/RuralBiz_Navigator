"""
RuralBiz Navigator - Deterministic Mock AI Provider (Demo Mode)
Provides intelligent, evidence-grounded, context-injected responses without external API calls.
Supports English, Hindi, Telugu, and Kannada.
"""
from typing import Dict, Any
from ai.base_provider import BaseAIProvider

class MockProvider(BaseAIProvider):
    """
    Offline deterministic response engine.
    Ensures the application works 100% reliably without requiring any external API keys.
    """
    
    def get_provider_name(self) -> str:
        return "Demo Engine (Offline Local AI)"
    
    def is_available(self) -> bool:
        return True
    
    def generate_response(
        self,
        prompt: str,
        context: Dict[str, Any],
        language: str = "en"
    ) -> str:
        p_lower = prompt.lower()
        
        # Extract context
        loc_name = context.get("locality_name", "your selected village")
        biz_name = context.get("business_name", "your selected business")
        score = context.get("viability_score", 78)
        recommendation = context.get("recommendation", "GO")
        emi = context.get("monthly_emi", 3500)
        profit = context.get("monthly_profit", 18500)
        dscr = context.get("dscr", 1.45)
        own_cap = context.get("own_capital", 300000)
        project_cost = context.get("project_cost", 215000)
        loan_amount = context.get("loan_amount", 50000)
        scheme_matches = context.get("matched_schemes", ["PMEGP", "PM MUDRA"])
        
        # Determine intent
        if any(w in p_lower for w in ["why", "score", "recommend", "78", "82", "decision"]):
            return self._build_why_response(loc_name, biz_name, score, recommendation, dscr, profit, language)
        elif any(w in p_lower for w in ["emi", "repay", "loan", "interest", "bank"]):
            return self._build_emi_response(loan_amount, emi, dscr, profit, language)
        elif any(w in p_lower for w in ["what business", "start with", "budget", "lakh", "capital"]):
            return self._build_budget_response(own_cap, loc_name, language)
        elif any(w in p_lower for w in ["stress", "sales fall", "fall 20", "drop", "what-if", "shock"]):
            return self._build_stress_response(biz_name, profit, emi, language)
        elif any(w in p_lower for w in ["scheme", "subsidy", "mudra", "pmegp", "government"]):
            return self._build_scheme_response(scheme_matches, project_cost, language)
        else:
            return self._build_general_response(loc_name, biz_name, score, recommendation, emi, profit, language)

    def _build_why_response(self, loc, biz, score, rec, dscr, profit, lang: str) -> str:
        if lang == "hi":
            return f"""**उत्तर (ANSWER):** {biz} को {score}/100 की व्यवहार्यता स्कोर के साथ **{rec}** अनुशंसित किया गया है।

**कारण (WHY):** स्थानीय कृषि व मांग का अच्छा तालमेल है और ऋण चुकाने का अनुपात (DSCR {dscr:.2f}) सुरक्षित है।

**साक्ष्य (EVIDENCE):** {loc} के जनसांख्यिकीय डेटा और 5-10 किमी के ग्राहक क्षेत्र में कम प्रतिस्पर्धी संतृप्ति पाई गई।

**वित्तीय प्रभाव (FINANCIAL IMPACT):** ईएमआई भुगतान के बाद अनुमानित मासिक शुद्ध लाभ ₹{profit:,.0f} है।

**जोखिम (RISK):** कच्चे माल की कीमतों में मौसमी उतार-चढ़ाव।

**अगला कदम (NEXT STEP):** क्या-यदि (What-If) सिमुलेटर में 15% लागत वृद्धि का तनाव परीक्षण जांचें और पीएमईजीपी/मुद्रा योजना के लिए आवेदन तैयार करें।"""
        elif lang == "te":
            return f"""**సమాధానం (ANSWER):** {biz} వ్యాపారానికి {score}/100 స్కోరుతో **{rec}** సిఫార్సు చేయబడింది.

**ఎందుకు (WHY):** {loc} గ్రామంలో స్థానిక డిమాండ్ సమృద్ధిగా ఉంది మరియు రుణ చెల్లింపు సామర్థ్యం (DSCR {dscr:.2f}) బలంగా ఉంది.

**ఆధారం (EVIDENCE):** 5-10 కి.మీ పరిధిలో తక్కువ పోటీదారులు మరియు నిరంతర స్థానిక వినియోగదారుల కొనుగోలు శక్తి.

**ఆర్థిక ప్రభావం (FINANCIAL IMPACT):** నెలకు నికర మిగులు లాభం దాదాపు ₹{profit:,.0f}.

**రిస్క్ (RISK):** ముడిసరుకుల ధరల హెచ్చుతగ్గులు మరియు విద్యుత్ సరఫరా అంతరాయాలు.

**తదుపరి చర్య (NEXT STEP):** వాట్-ఇఫ్ సిమ్యులేటర్‌ని తనిఖీ చేసి ప్రభుత్వ పథకాల ద్వారా సబ్సిడీ కోసం దరఖాస్తు చేసుకోండి."""
        elif lang == "kn":
            return f"""**ಉತ್ತರ (ANSWER):** {biz} ವ್ಯವಹಾರಕ್ಕೆ {score}/100 ಕಾರ್ಯಸಾಧ್ಯತೆಯ ಸ್ಕೋರ್‌ನೊಂದಿಗೆ **{rec}** ಶಿಫಾರಸು ಮಾಡಲಾಗಿದೆ.

**ಕಾರಣ (WHY):** {loc} ಗ್ರಾಮದಲ್ಲಿ ಸ್ಥಳೀಯ ಬೇಡಿಕೆ ಉತ್ತಮವಾಗಿದೆ ಮತ್ತು ಸಾಲ ಮರುಪಾವತಿ ಸಾಮರ್ಥ್ಯ (DSCR {dscr:.2f}) ಸುರಕ್ಷಿತವಾಗಿದೆ.

**ಸಾಕ್ಷ್ಯ (EVIDENCE):** 5-10 ಕಿಮೀ ವ್ಯಾಪ್ತಿಯಲ್ಲಿ ಸೀಮಿತ ಸ್ಪರ್ಧೆ ಮತ್ತು ಬಲವಾದ ಗ್ರಾಹಕ ಮಾರುಕಟ್ಟೆ.

**ಹಣಕಾಸಿನ ಪರಿಣಾಮ (FINANCIAL IMPACT):** ಮಾಸಿಕ ಇಎಂಐ ಪಾವತಿಯ ನಂತರ ಅಂದಾಜು ನಿವ್ವಳ ಲಾಭ ₹{profit:,.0f}.

**ಅಪಾಯ (RISK):** ಕಚ್ಚಾ ವಸ್ತುಗಳ ಬೆಲೆ ಏರಿಳಿತಗಳು.

**ಮುಂದಿನ ಹೆಜ್ಜೆ (NEXT STEP):** 'ವಾಟ್-ಇಫ್' ಸಿಮ್ಯುಲೇಟರ್‌ನಲ್ಲಿ ಒತ್ತಡ ಪರೀಕ್ಷಿಸಿ ಮತ್ತು ಪಿಎಂಇಜಿಪಿ/ಮುದ್ರಾ ಸಬ್ಸಿಡಿಗೆ ಅರ್ಜಿ ಸಲ್ಲಿಸಿ."""
        else:
            return f"""**ANSWER:**
The business **{biz}** received a Viability Score of **{score}/100** with a final recommendation of **{rec}**.

**WHY:**
1. Strong alignment with local agrarian resources and household consumption patterns in {loc}.
2. Robust debt-servicing ability with a calculated DSCR of {dscr:.2f} (well above the safe threshold of 1.20).
3. Sustainable operating margin with competitive room in the local village catchment.

**EVIDENCE:**
Demographic analysis of {loc} indicates steady purchasing power, while our prototype competitor map indicates healthy unmet demand within the 5–10 km radius.

**FINANCIAL IMPACT:**
Projected monthly net cash flow is ₹{profit:,.0f} after meeting all monthly operating expenses and loan EMI commitments.

**RISK:**
Raw material input price volatility and working capital lockup during initial customer acquisition.

**NEXT STEP:**
Review the sensitivity analysis on the 'What-If Simulator' page and inspect eligible credit-linked subsidy schemes (e.g. PMEGP or MUDRA)."""

    def _build_emi_response(self, loan, emi, dscr, profit, lang: str) -> str:
        if lang == "hi":
            return f"""**उत्तर (ANSWER):** ₹{loan:,.0f} के अनुमानित ऋण पर आपकी मासिक ईएमआई लगभग **₹{emi:,.0f}** होगी।

**कारण (WHY):** यह 9.5% वार्षिक ब्याज दर और 60 महीनों के कम होते मूलधन (Reducing Balance) फॉर्मूले पर आधारित है।

**साक्ष्य (EVIDENCE):** डीएससीआर (DSCR) {dscr:.2f} है, जो दर्शाता है कि आपका व्यवसाय सुरक्षित रूप से ईएमआई का भुगतान कर सकता है।

**वित्तीय प्रभाव (FINANCIAL IMPACT):** ईएमआई घटाने के बाद भी आपके पास ₹{profit:,.0f} का शुद्ध मासिक नकदी प्रवाह बचता है।

**जोखिम (RISK):** यदि बिक्री 25% से अधिक गिरती है, तो ईएमआई का दबाव बढ़ सकता है।

**अगला कदम (NEXT STEP):** 3 महीने की मोराटोरियम (Moratorium) अवधि का उपयोग करें ताकि व्यवसाय स्थिर हो सके।"""
        else:
            return f"""**ANSWER:**
For a loan requirement of ₹{loan:,.0f}, your calculated monthly EMI will be approximately **₹{emi:,.0f}**.

**WHY:**
Calculated using the standard reducing-balance amortization method at 9.5% p.a. over a 60-month tenure with a 3-month moratorium buffer.

**EVIDENCE:**
Your projected EBITDA operating profit provides a Debt Service Coverage Ratio (DSCR) of {dscr:.2f}, which is classified as safe by commercial lending norms.

**FINANCIAL IMPACT:**
After paying the ₹{emi:,.0f} EMI, you retain an estimated net cash surplus of ₹{profit:,.0f} each month.

**RISK:**
Default vulnerability if monthly sales fall below the calculated Break-Even Point.

**NEXT STEP:**
Check the 'Financial Calculator' amortization table to view month-by-month principal and interest breakdown."""

    def _build_budget_response(self, own_cap, loc, lang: str) -> str:
        return f"""**ANSWER:**
With available capital of ₹{own_cap:,.0f} in {loc}, strong starting candidates include **Food Processing**, **Tailoring Unit**, or a **Digital / CSC Kiosk**.

**WHY:**
These businesses have capital expenditures well within your reach, requiring manageable debt while yielding steady rural cash flows.

**EVIDENCE:**
Benchmark CapEx for Food Processing is ~₹1,80,000, Tailoring ~₹75,000, and Digital Kiosk ~₹85,000, leaving a comfortable working capital reserve.

**FINANCIAL IMPACT:**
Minimal loan burden results in higher net take-home margins (25% - 40%) from the first quarter.

**RISK:**
Low barrier to entry in retail/kiosks requires superior customer service and local community trust.

**NEXT STEP:**
Visit the 'Business Alternatives' page to view a ranked comparison table tailored to your exact budget."""

    def _build_stress_response(self, biz, profit, emi, lang: str) -> str:
        surplus = max(0, profit - (profit * 0.3))
        return f"""**ANSWER:**
If sales drop by 20%, the business will still **survive with an operational buffer**, though net profit will compress to approximately ₹{surplus:,.0f}/month.

**WHY:**
The contribution margin ratio is sufficiently high to absorb a 20% volume decline before breaching the monthly fixed cost + EMI threshold.

**EVIDENCE:**
The base case Margin of Safety is positive. The simulated break-even revenue sits below 75% of your baseline sales projection.

**FINANCIAL IMPACT:**
Cash flow remains positive, and loan EMI of ₹{emi:,.0f} can still be honored on time without external borrowing.

**RISK:**
If sales fall beyond 35% simultaneously with raw material inflation, the venture will enter the danger zone.

**NEXT STEP:**
Use the sliders in the 'What-If Simulator' tab to test combined shocks (e.g. Sales -20% AND Costs +15%)."""

    def _build_scheme_response(self, schemes, cost, lang: str) -> str:
        scheme_list = ", ".join(schemes[:2]) if schemes else "PMEGP and PM MUDRA"
        return f"""**ANSWER:**
For your project setup of ₹{cost:,.0f}, the most relevant government schemes are **{scheme_list}**.

**WHY:**
These schemes offer credit-linked capital subsidies (up to 25%-35% under PMEGP in rural areas) or collateral-free loans under MUDRA (Kishore category).

**EVIDENCE:**
Verified Ministry guidelines (MSME / MoFPI) match your investment scale and rural micro-enterprise classification.

**FINANCIAL IMPACT:**
A 25% PMEGP subsidy could reduce your effective loan principal by thousands of rupees, directly reducing monthly EMI.

**RISK:**
Final sanction is dependent on bank appraisal, credit bureau history, and District Task Force Committee approval.

**NEXT STEP:**
Open the 'Scheme Navigator' page to view document checklists, application routes, and official portal links."""

    def _build_general_response(self, loc, biz, score, rec, emi, profit, lang: str) -> str:
        return f"""**ANSWER:**
RuralBiz Navigator has evaluated **{biz}** in **{loc}**: Viability is **{score}/100** ({rec}).

**WHY:**
The evaluation balances hyper-local demand, competitor density in the 5-10 km radius, debt coverage (DSCR), and break-even safety margin.

**EVIDENCE:**
Derived from our prototype rural demographic dataset, verified benchmark unit economics, and reducing-balance debt modeling.

**FINANCIAL IMPACT:**
Projected monthly revenue supports operating expenses and the estimated ₹{emi:,.0f} EMI with positive monthly net cash flow.

**RISK:**
Market competition, input cost inflation, and initial working capital delays.

**NEXT STEP:**
Download your complete Detailed Project Report (DPR) from the 'DPR Report' tab."""
