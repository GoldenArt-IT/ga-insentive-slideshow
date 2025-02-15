import streamlit as st
import pandas as pd
import time
from streamlit_gsheets import GSheetsConnection

# App Layout
st.set_page_config(layout="wide")

st.title("🏆 Staff Incentive Dashboard")

# Load data
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="DATA", ttl=5)

# Sort by incentive (Descending)
df = df.sort_values(by="INCENTIVE", ascending=False).reset_index(drop=True)

# Sidebar for ranking
st.sidebar.header("📊 Staff Ranking")
st.sidebar.dataframe(df[['STAFF NAME', 'INCENTIVE']])

# Main panel for slideshow
col1, col2 = st.columns([1, 2])

# Slideshow container
slideshow_container = st.empty()

# Loop for slideshow
while True:
    for i in range(len(df)):
        with slideshow_container:
            st.subheader(f"🌟 {df.iloc[i]['STAFF NAME']}")

            # Get image URL
            image_url = df.iloc[i]['PICTURE']

            # Validate image URL
            if isinstance(image_url, str) and image_url.strip():
                st.image(image_url, width=300)
            else:
                st.write("🚫 No Image Available")

            # Format Incentive (Handle NaN)
            incentive_value = df.iloc[i]['INCENTIVE']
            if pd.isna(incentive_value):
                incentive_value = 0.00  # Default to zero if missing

            st.metric(label="💰 Incentive Earned", value=f"${float(incentive_value):,.2f}")

        # Auto-refresh delay
        time.sleep(5)  # Change for faster/slower slideshow
