import io
import tempfile
from datetime import datetime

import matplotlib.pyplot as plt
import streamlit as st
from fpdf import FPDF

# ---------------- Helpers ----------------
def safe_text(text: str) -> str:
    """Convert any non-Latin-1 characters so FPDF 1.x won't crash."""
    return str(text).encode("latin-1", "replace").decode("latin-1")


# ---------------- Session ----------------
if "history" not in st.session_state:
    st.session_state.history = []  # list of tuples: (activity, value, emissions)


# ---------------- Sidebar ----------------
st.sidebar.header("Premium Report Settings")
user_name = st.sidebar.text_input("Your Name", "John Doe")
organization = st.sidebar.text_input("Organization (Optional)", "")
include_chart = st.sidebar.checkbox("Include Emissions Chart", True)
include_tips = st.sidebar.checkbox("Include Sustainability Tips", True)
include_cover = st.sidebar.checkbox("Include Cover Page", True)


# ---------------- Main ----------------
st.title("Carbon Emissions Tracker")
st.subheader("Estimate your carbon footprint from daily activities")

activity = st.selectbox("Choose an activity:", ["Driving", "Flying", "Electricity Use"])

# Friendlier unit label
unit_label = "distance (km)" if activity in ("Driving", "Flying") else "energy used (kWh)"
value = st.number_input(f"Enter {unit_label}:", min_value=0.0)

# Simple factors (kg CO2 per unit)
factors = {"Driving": 0.21, "Flying": 0.25, "Electricity Use": 0.233}

# Add entry
col_add, col_clear = st.columns(2)
with col_add:
    if st.button("Add to Report"):
        emissions = value * factors[activity]
        st.session_state.history.append((activity, value, emissions))
        st.success(f"Added: {emissions:.2f} kg CO2 for {value} units of {activity}")
with col_clear:
    if st.button("Clear Report"):
        st.session_state.history = []
        st.experimental_rerun()


# ---------------- Results ----------------
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

    # ---------------- PDF Export ----------------
    if st.button("Download Premium PDF Report"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.alias_nb_pages()   # enable page numbers

        # ----- Optional cover page -----
        if include_cover:
            pdf.add_page()
            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 12, safe_text("Carbon Emissions Premium Report"), ln=True, align="C")

            pdf.set_font("Arial", "", 12)
            pdf.ln(4)
            pdf.cell(0, 8, safe_text(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"), ln=True, align="C")
            pdf.ln(4)

            # User info centered
            if user_name:
                pdf.cell(0, 8, safe_text(f"Prepared for: {user_name}"), ln=True, align="C")
            if organization:
                pdf.cell(0, 8, safe_text(f"Organization: {organization}"), ln=True, align="C")

            pdf.ln(8)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 7, safe_text(
                "This report summarizes estimated greenhouse gas emissions (CO2) "
                "based on entered activities and standard emission factors. "
                "Values are indicative and intended for awareness and planning."
            ))

            # Summary on cover
            pdf.ln(6)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, safe_text("Summary"), ln=True)
            pdf.set_font("Arial", "", 12)
            for k, v in breakdown.items():
                pdf.cell(0, 7, safe_text(f"{k}: {v:.2f} kg CO2"), ln=True)
            pdf.ln(2)
            pdf.cell(0, 8, safe_text(f"Total: {total:.2f} kg CO2"), ln=True)

        # ----- Main content page -----
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, safe_text("Detailed Breakdown"), ln=True)

        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 8, safe_text(f"Name: {user_name}"), ln=True)
        if organization:
            pdf.cell(0, 8, safe_text(f"Organization: {organization}"), ln=True)
        pdf.cell(0, 8, safe_text(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"), ln=True)
        pdf.ln(4)

        # Entries
        for act, val, emis in st.session_state.history:
            line = f"{act}: {val} units - {emis:.2f} kg CO2"
            pdf.cell(0, 8, safe_text(line), ln=True)

        pdf.ln(3)
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 8, safe_text(f"Total Emissions: {total:.2f} kg CO2"), ln=True)

        # Optional tips
        if include_tips:
            pdf.ln(6)
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, safe_text("Sustainability Tips:"), ln=True)
            pdf.set_font("Arial", "", 12)
            tips = [
                "- Walk or cycle for short distances",
                "- Switch to energy-efficient appliances",
                "- Reduce single-use plastic",
                "- Unplug devices when not in use",
                "- Support renewable energy initiatives",
            ]
            for tip in tips:
                pdf.cell(0, 7, safe_text(tip), ln=True)

        # Optional: embed the pie chart
        if include_chart and breakdown:
            fig2, ax2 = plt.subplots()
            ax2.pie(breakdown.values(), labels=breakdown.keys(), autopct="%1.1f%%")
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tmp:
                fig2.savefig(tmp.name, dpi=150, bbox_inches="tight")
                plt.close(fig2)
                pdf.ln(6)
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 8, safe_text("Emissions Breakdown Chart"), ln=True)
                pdf.image(tmp.name, w=180)

        # Footer with page number (place near end so it's on the current page)
        pdf.set_y(-15)
        pdf.set_font("Arial", "I", 8)
        pdf.cell(0, 10, safe_text(f"Page {pdf.page_no()}/{{nb}}"), align="C")

        # Output and download
        filename = f"carbon_emissions_report_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        pdf_bytes = pdf.output(dest="S").encode("latin-1")
        st.download_button(
            label="Click to Download Your Premium PDF Report",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
        )
else:
    st.info("Add at least one activity to generate your report.")




