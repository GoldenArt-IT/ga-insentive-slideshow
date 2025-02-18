import streamlit as st
import pandas as pd
import time
from streamlit_gsheets import GSheetsConnection
import base64
from io import BytesIO
from PIL import Image
import requests

#---------------------------------------------------------OPERATIONS-------------------------------------------------------------

def get_image_url(url):
    """Convert Google Drive link to a direct image URL."""
    if isinstance(url, str) and "drive.google.com" in url:
        if "/file/d/" in url:
            file_id = url.split("/d/")[1].split("/")[0]
            return requests.get(f"https://drive.google.com/uc?export=view&id={file_id}").content
        elif "id=" in url:
            file_id = url.split("id=")[1]
            return requests.get(f"https://drive.google.com/uc?export=view&id={file_id}").content
    return url  # Return the original URL if it's not from Google Drive

def decode_image(base64_string):
    """Convert Base64 string to an image, handling errors safely."""
    try:
        base64_string = base64_string.strip()
        image_bytes = base64.b64decode(base64_string)
        return Image.open(BytesIO(image_bytes))
    except Exception:
        return None

# Load Data
st.set_page_config(layout="wide")

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="DATA", ttl=10)
df = df.dropna(thresh=2)
df = df.sort_values(by="INCENTIVE", ascending=False).reset_index(drop=True)

# Initialize session state for slideshow
if "index" not in st.session_state:
    st.session_state.index = 0

# Get staff details
staff_name = df.iloc[st.session_state.index]["STAFF NAME"]
image_data = df.iloc[st.session_state.index]["PICTURE"]
incentive_value = df.iloc[st.session_state.index]['INCENTIVE']
incentive_value = 0.00 if pd.isna(incentive_value) else float(incentive_value)


#---------------------------------------------------------UI DESIGN-------------------------------------------------------------

# Side Bar
st.sidebar.header("📊 Staff Ranking")
st.sidebar.dataframe(df[['STAFF NAME', 'INCENTIVE', 'DEPARTMENT']])
st.sidebar.markdown("### ⏳ Auto-Slideshow")

auto_slide = st.sidebar.checkbox("Enable Slideshow", value=True)
slide_delay = st.sidebar.slider("Slide Delay (seconds)", 2, 10, 5)

# Main Page View
st.title("🏆 Top 10 Staff Terbaik GA !")
st.subheader(f"🌟 {staff_name}")

# Display Image
if pd.isna(image_data) or image_data.strip() == "":
    st.write("🚫 No Image Available")
elif image_data.startswith("http"):
    st.image(get_image_url(image_data), width=300)
else:
    image = decode_image(image_data)
    st.image(image, width=300) if image else st.write("🚫 No Image Available")

st.metric(label="💰 Incentive Earned", value=f"${incentive_value:,.2f}")

# Buttons
col1, col2, col3 = st.columns([1, 2, 1])

if col1.button("⏮️ Previous"):
    st.session_state.index = (st.session_state.index - 1) % len(df)

if col2.button("⏭️ Next"):
    st.session_state.index = (st.session_state.index + 1) % len(df)

# Auto-slide
if auto_slide:
    time.sleep(slide_delay)
    st.session_state.index = (st.session_state.index + 1) % 10
    st.rerun()
