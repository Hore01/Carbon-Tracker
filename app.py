import io
import matplotlib.pyplot as plt
import streamlit as st
from fpdf import FPDF

# ---------- Helpers ----------
def safe_text(text: str) -> str:
    """Convert any non-Latin-1 characters so FPDF 1.x won't crash."""
    return str(text).encode("latin-1", "replace").decode("latin-1")

# ---------- Session ----------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------- Sidebar ----------
st.sidebar.header("Premium Report Settings")
user_name = st.sidebar.text_input("Your Name", "John Doe")
organization = st.sidebar.text_input("Organization (Optional)", "")
include_chart = st.sidebar.checkbox("Include Emissions Chart", True)
include_tips = st.sidebar.checkbox("Include Sustainability Tips", True)

# ---------- Main ----------
st.title("Carbon Emissions Tracker")
st.subheader("Estimate your carbon footprint from daily activities")

activity = st.selectbox("Choose an activity:", ["Driving", "Flying", "Electricity Use"])
value = st.number_input("Enter distance (km) or energy used (kWh):", min_value=0.0)

factors = {
    "Driving": 0.21,
    "Flying": 0.25,
    "Electricity Use": 0.233
}

# Add entry
if st.button("Add to Report"):
    emissions = value * factors[activity]
    st.session_state.history.append((activity, value, emissions))
    st.success(f"Added: {emissions:.2f} kg CO2 for {value} units of {activity}")

# Show results
if st.session_state.history:
    st.subheader("Emission Breakdown")

    total = 0.0
    breakdown = {}
    for act, val, emis in st.session_state.history:
        total += emis
        breakdown[act] = breakdown.get(act, 0.0) + emis

    if include_chart and breakdown:
        fig, ax = plt.subplots()
        ax.pie(breakdown.values(), labels=breakdown.keys(), autopct="%1.1f%%")
        st.pyplot(fig)

    st.markdown(f"**Total emissions:** {total:.2f} kg CO2")

    # ---------- PDF export ----------
    if st.button("Download Premium PDF Report"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Header
        pdf.cell(200, 10, txt=safe_text("Carbon Emissions Premium Report"), ln=True, align="C")
        pdf.ln(5)

        # User info
        pdf.cell(200, 10, txt=safe_text(f"Name: {user_name}"), ln=True)
        if organization:
            pdf.cell(200, 10, txt=safe_text(f"Organization: {organization}"), ln=True)
        pdf.ln(5)

        # Breakdown lines
        for act, val, emis in st.session_state.history:
            line = f"{act}: {val} units - {emis:.2f} kg CO2"
            pdf.cell(200, 8, txt=safe_text(line), ln=True)

        # Total
        pdf.ln(3)
        pdf.cell(200, 10, txt=safe_text(f"Total Emissions: {total:.2f} kg CO2"), ln=True)

        # Tips
        if include_tips:
            pdf.ln(6)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(200, 10, txt=safe_text("Sustainability Tips:"), ln=True)
            pdf.set_font("Arial", size=12)
            tips = [
                "- Walk or cycle for short distances",
                "- Switch to energy-efficient appliances",
                "- Reduce single-use plastic",
                "- Unplug devices when not in use",
                "- Support renewable energy initiatives",
            ]
            for tip in tips:
                pdf.cell(200, 8, txt=safe_text(tip), ln=True)

        # Output as bytes (most reliable for FPDF 1.x)
        pdf_bytes = pdf.output(dest="S").encode("latin-1")

        st.download_button(
            label="Click to Download Your Premium PDF Report",
            data=pdf_bytes,
            file_name="carbon_emissions_premium_report.pdf",
            mime="application/pdf",
        )
