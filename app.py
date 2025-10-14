import streamlit as st
import matplotlib.pyplot as plt
from fpdf import FPDF
import io

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar premium details
st.sidebar.header("Premium Report Settings")
user_name = st.sidebar.text_input("Your Name", "John Doe")
organization = st.sidebar.text_input("Organization (Optional)", "")
include_chart = st.sidebar.checkbox("Include Emissions Chart", True)
include_tips = st.sidebar.checkbox("Include Sustainability Tips", True)

# Main App
st.title("Carbon Emissions Tracker")
st.subheader("Estimate your carbon footprint from daily activities")

# Input
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
    st.success(f"Added: {emissions:.2f} kg CO₂ for {value} units of {activity}")

# Display history
if st.session_state.history:
    st.subheader("Emission Breakdown")
    total = 0
    breakdown = {}
    for act, val, emis in st.session_state.history:
        total += emis
        breakdown[act] = breakdown.get(act, 0) + emis

    if include_chart:
        fig, ax = plt.subplots()
        ax.pie(breakdown.values(), labels=breakdown.keys(), autopct='%1.1f%%')
        st.pyplot(fig)

    st.markdown(f"**Total emissions:** {total:.2f} kg CO₂")

    if st.button("Download Premium PDF Report"):
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Carbon Emissions Premium Report", ln=True, align='C')
        pdf.ln(10)

        pdf.cell(200, 10, txt=f"Name: {user_name}", ln=True)
        if organization:
            pdf.cell(200, 10, txt=f"Organization: {organization}", ln=True)
        pdf.cell(200, 10, txt="", ln=True)

        for act, val, emis in st.session_state.history:
            pdf.cell(200, 10, txt=f"{act}: {val} units → {emis:.2f} kg CO₂", ln=True)

        pdf.cell(200, 10, txt=f"Total Emissions: {total:.2f} kg CO₂", ln=True)

        if include_tips:
            pdf.ln(10)
            pdf.set_font("Arial", 'B', 12)
            pdf.cell(200, 10, txt="Sustainability Tips:", ln=True)
            pdf.set_font("Arial", size=12)
            tips = [
                "- Walk or cycle for short distances",
                "- Switch to energy-efficient appliances",
                "- Reduce single-use plastic",
                "- Unplug devices when not in use",
                "- Support renewable energy initiatives"
            ]
            for tip in tips:
                pdf.cell(200, 10, txt=tip, ln=True)

        pdf_output = io.BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)

        st.download_button(
            label="Click to Download Your Premium PDF Report",
            data=pdf_output,
            file_name="carbon_emissions_premium_report.pdf",
            mime="application/pdf"
        )