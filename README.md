#  Carbon Emission Tracker 

A clean, auditable Streamlit app to estimate annual greenhouse gas emissions (CO2e) across **Transport**, **Home Energy**, **Food**, **Purchases**, and **Waste**.

This project is part of my Global Talent application to showcase my ability to build structured, data-driven, and user-friendly climate tech tools.

##  Features
-  Clear sections with live calculations  
-  Export results as **CSV**, **JSON**, or **PDF**  
-  Upload your own emission factors (JSON format)  
-  Easy deployment on Streamlit Cloud

##  Quick Start
1. Open the app: [Your Streamlit App URL here](#) *(after deployment)*  
2. Enter your data for transport, home energy, food, purchases, and waste.  
3. Download your results as a report.

##  Installation (if running locally)
```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/carbon-emission-tracker.git
cd carbon-emission-tracker

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

##  Methodology
- Emissions = **activity × emission factor**.
- Food values are **annualized** from weekly inputs.
- Flight distances are **averaged** per trip type (short/medium/long haul).
- Users can **upload their own emission factors** to override defaults.

##  Emission Factor Sources (Example)
- UK Government GHG Conversion Factors
- IPCC Guidelines
- EPA (US)

##  About
Built by Olajumoke Akinremi as part of a portfolio demonstrating impact-focused digital tools for climate action.


