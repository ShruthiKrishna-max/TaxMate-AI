import streamlit as st
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Tax_Bot", layout="centered")

st.markdown("""
<style>
    .card {
        background-color: #f5f7ff;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        color: black;
    }
    .big-card {
        background-color: #e8f0ff;
        padding: 18px;
        border-radius: 12px;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.15);
        margin-bottom: 10px;
        color: black;
        font-size: 18px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

st.set_page_config(page_title="Tax_Bot", layout="centered")

col1, col2 = st.columns([1, 4])

logo_path = "logo.png"

with col1:
    if os.path.exists(logo_path):
        st.image(logo_path, width=80)
    else:
        st.write("💰")

with col2:
    st.title("💰 AI Tax Assistant")

qa_map = {
"what is section 80c": "Section 80C allows deduction up to ₹1.5 lakh on investments like PPF, ELSS, LIC, EPF.",
"80c deduction": "Section 80C allows deduction up to ₹1.5 lakh on investments like PPF, ELSS, LIC, EPF.",
"how much 80c limit": "Maximum deduction under Section 80C is ₹1.5 lakh.",

"what is itr": "ITR is Income Tax Return form used to declare income to the government.",
"how to file itr": "You can file ITR on the Income Tax e-filing portal using PAN and Aadhaar.",
"steps to file itr": "Login → Fill form → Verify → Submit.",

"itr deadline": "The ITR filing deadline is usually July 31 every year.",
"last date for itr": "The ITR filing deadline is usually July 31 every year.",
"due date itr": "The ITR filing deadline is usually July 31 every year.",

"what is income tax": "Income tax is the tax paid to the government based on earnings.",
"why do we pay tax": "Taxes fund public services like roads, healthcare, education.",
"who should pay tax": "Anyone earning above exemption limit must pay tax.",

"what is gross income": "Gross income is total income before deductions.",
"what is net salary": "Net salary is income after tax.",
"what is taxable income": "Taxable income = Income - ₹75,000 deduction.",

"what is tds": "TDS is tax deducted before salary is credited.",
"what is form 16": "Form 16 shows salary and tax deducted.",

"what is pan card": "PAN is a unique ID for tax purposes.",

"what is 80d": "Section 80D gives health insurance deduction.",
"what is rebate 87a": "Section 87A gives rebate for low income.",

"old vs new tax regime": "Old allows deductions, new has lower rates.",

"what is standard deduction": "Standard deduction is ₹75,000.",

"documents for itr": "PAN, Aadhaar, Form 16, bank details needed.",

"miss itr deadline": "Late filing may attract penalty.",

"do students pay tax": "Only if income exceeds limit.",

"how to reduce tax": "Use deductions like 80C, 80D."
}

stopwords = ["what", "is", "how", "to", "the", "for", "a", "of", "do", "we", "are"]

def calculate_tax(income):
    std = 75000
    taxable = max(0, income - std)

    if taxable <= 400000:
        tax = 0
    elif taxable <= 800000:
        tax = (taxable - 400000) * 0.05
    elif taxable <= 1200000:
        tax = 20000 + (taxable - 800000) * 0.10
    elif taxable <= 1600000:
        tax = 60000 + (taxable - 1200000) * 0.15
    else:
        tax = 120000 + (taxable - 1600000) * 0.20

    cess = tax * 0.04
    total = tax + cess

    return {
        "taxable_income": taxable,
        "tax": tax,
        "cess": cess,
        "total": total,
        "std_deduction": std
    }

def get_applicable_slab(taxable_income):
    if taxable_income <= 400000:
        return "0% Slab"
    elif taxable_income <= 800000:
        return "5% Slab"
    elif taxable_income <= 1200000:
        return "10% Slab"
    elif taxable_income <= 1600000:
        return "15% Slab"
    else:
        return "20% Slab"

def generate_insights(result, income):
    slab_rate = get_applicable_slab(result["taxable_income"])
    slab_line = f"✔ Your income falls under: {slab_rate} (New Regime)"

    deduction_line = f"✔ Standard Deduction Applied: ₹{result['std_deduction']:,}"

    regime_line = " This calculation is based on the NEW TAX REGIME"

    suggestions = []

    if result["taxable_income"] > 150000:
        suggestions.append(" Consider investing in 80C instruments (PPF, ELSS, LIC)")
    if income > 500000:
        suggestions.append(" Use health insurance under 80D for extra savings")
    suggestions.append(" Compare Old vs New regime before filing ITR")

    return slab_line, deduction_line, regime_line, suggestions

def compare_regimes(income):
    new = calculate_tax(income)

    std = 50000
    taxable = max(0, income - std)

    if taxable <= 250000:
        old_tax = 0
    elif taxable <= 500000:
        old_tax = (taxable - 250000) * 0.05
    elif taxable <= 1000000:
        old_tax = 12500 + (taxable - 500000) * 0.20
    else:
        old_tax = 112500 + (taxable - 1000000) * 0.30

    old_cess = old_tax * 0.04
    old_total = old_tax + old_cess

    diff = old_total - new["total"]

    if diff > 0:
        best = " NEW REGIME is better"
        savings = diff
    else:
        best = " OLD REGIME is better"
        savings = abs(diff)

    return {
        "old_tax": old_tax,
        "old_total": old_total,
        "new_tax": new["tax"],
        "new_total": new["total"],
        "best": best,
        "savings": savings
    }

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def generate_pdf(report_text):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    style = styles["Normal"]

    content = []

    for line in report_text.split("\n"):
        content.append(Paragraph(line, style))
        content.append(Spacer(1, 5))

    doc.build(content)
    buffer.seek(0)
    return buffer

def chatbot_response(user_input, name, pan, fy, ay):
    user_input = user_input.lower()

    if any(greet in user_input for greet in ["hi", "hello", "hey"]):
        return "👋 Hey! I'm your AI Tax Assistant. Ask me anything about taxes!"

    best_match = None
    best_score = 0

    for question, answer in qa_map.items():
        keywords = [w for w in question.split() if w not in stopwords]
        score = sum(1 for word in keywords if word in user_input)

        if score > best_score:
            best_score = score
            best_match = answer

    if best_score > 0:
        return f"💡 {best_match}"

    for word in user_input.split():
        if word.isdigit():
            income = int(word)
            result = calculate_tax(income)

            return f"""
📄 Tax Summary

Name: {name}
PAN: {pan}
FY: {fy}
AY: {ay}

Total Tax: ₹{result['total']:,}
"""

    return "🤖 Try asking about ITR, tax, or deductions."

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

tab1, tab2 = st.tabs(["💸 Tax Calculator", "🤖 Chatbot"])

with tab1:
    name = st.text_input("👤 Name")
    pan = st.text_input("🆔 PAN")
    fy = st.text_input("📅 Financial Year (e.g., 2025-26)")

    if fy:
        try:
            start = int(fy.split("-")[0])
            ay = f"{start+1}-{start+2}"
        except:
            ay = ""
    else:
        ay = ""

    income = st.number_input("💰 Enter Annual Income", min_value=0)

    if st.button("Calculate Tax"):
        result = calculate_tax(income)

        slab_line, deduction_line, regime_line, suggestions = generate_insights(result, income)

        st.success("✅ Tax Calculated Successfully")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"<div class='card'>💰 Tax<br><b>₹{result['tax']:,.0f}</b></div>", unsafe_allow_html=True)

        with col2:
            st.markdown(f"<div class='card'>🧾 Cess<br><b>₹{result['cess']:,.0f}</b></div>", unsafe_allow_html=True)

        with col3:
            st.markdown(f"<div class='big-card'>🏁 Total Tax<br>₹{result['total']:,.0f}</b></div>", unsafe_allow_html=True)

        st.markdown("---")

        st.markdown("## 📄 Tax Report")

        st.markdown(f"""
### 👤 Personal Details
- Name: {name}
- PAN: {pan}
- FY: {fy}
- AY: {ay}

### 💰 Tax Summary
- Taxable Income: ₹{result['taxable_income']:,}
- Standard Deduction: ₹{result['std_deduction']:,}
- Tax: ₹{result['tax']:,}
- Cess: ₹{result['cess']:,}
- Total Tax: ₹{result['total']:,}
""")

        st.markdown("## 💡 Tax Insights")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class='card'>
                📊 Slab Analysis<br><br>
                <b>{slab_line}</b>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class='card'>
                📉 Deduction Info<br><br>
                <b>{deduction_line}</b>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='big-card'>
        📌 Regime Status<br><br>
        {regime_line}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("### ⭐ Suggestions")
        for s in suggestions:
            st.markdown(f"<div class='card'>👉 {s}</div>", unsafe_allow_html=True)

        comp = compare_regimes(income)

        st.markdown("## ⚖️ Old vs New Regime Comparison")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"""
            <div class='card'>
            🧾 OLD REGIME<br><br>
            Tax: ₹{comp['old_tax']:,.0f}<br>
            Total: ₹{comp['old_total']:,.0f}
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class='card'>
            💰 NEW REGIME<br><br>
            Tax: ₹{comp['new_tax']:,.0f}<br>
            Total: ₹{comp['new_total']:,.0f}
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='big-card'>
        🏆 Recommendation:<br><br>
        {comp['best']}<br><br>
         Savings: ₹{comp['savings']:,.0f}
        </div>
        """, unsafe_allow_html=True)

        remaining = max(0, income - result["total"])

        fig, ax = plt.subplots()
        ax.pie([result["total"], remaining],
               labels=["Tax", "Remaining"],
               autopct="%1.1f%%")
        st.pyplot(fig)

        fig2, ax2 = plt.subplots()
        ax2.bar(
            ["Income", "Tax", "Cess", "Net Take Home"],
            [income, result["tax"], result["cess"], income - result["total"]]
        )
        st.pyplot(fig2)


        report_text = f"""
TAX REPORT

Name: {name}
PAN: {pan}
FY: {fy}
AY: {ay}

----------------------------
FINANCIAL SUMMARY
----------------------------
Taxable Income: Rs.{result['taxable_income']:,}
Standard Deduction: Rs.{result['std_deduction']:,}
Tax: Rs.{result['tax']:,}
Cess: Rs.{result['cess']:,}
Total Tax: Rs.{result['total']:,}

----------------------------
INSIGHTS
----------------------------
{slab_line}
{deduction_line}
{regime_line}

----------------------------
SUGGESTIONS
----------------------------
{chr(10).join(suggestions)}

----------------------------
REGIME COMPARISON
----------------------------
Old Regime Tax: Rs.{comp['old_tax']:,.0f}
Old Regime Total: Rs.{comp['old_total']:,.0f}

New Regime Tax: Rs.{comp['new_tax']:,.0f}
New Regime Total: Rs.{comp['new_total']:,.0f}

Recommendation: {comp['best']}
Savings: Rs.{comp['savings']:,.0f}
"""

        pdf_buffer = generate_pdf(report_text)
        st.download_button(
           label="📥 Download Tax Report",
           data=pdf_buffer,
           file_name="tax_report.pdf",
           mime="application/pdf"
    )

with tab2:
    for chat in st.session_state.chat_history:
        with st.chat_message(chat["role"]):
            st.write(chat["content"])

    user_input = st.chat_input("Ask your tax question...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        response = chatbot_response(user_input, name, pan, fy, ay)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
        st.rerun()