import streamlit as st
import pandas as pd
import time
from streamlit_gsheets import GSheetsConnection
import base64
from io import BytesIO
from PIL import Image
import requests

def get_image_url(url):
    """Convert Google Drive link to a direct image URL."""
    if isinstance(url, str) and "drive.google.com" in url:
        if "/file/d/" in url:
            file_id = url.split("/d/")[1].split("/")[0]
            url = f"https://drive.google.com/uc?export=view&id={file_id}"
            return requests.get(url).content
        elif "id=" in url:
            file_id = url.split("id=")[1]
            url = f"https://drive.google.com/uc?export=view&id={file_id}"
            return requests.get(url).content
    return url  # Return the original URL if it's not from Google Drive


def decode_image(base64_string):
    """Convert Base64 string to an image, handling errors safely."""
    try:
        base64_string = base64_string.strip()  # Remove unwanted spaces/newlines
        image_bytes = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_bytes))
        return image
    except Exception as e:
        print("❌ Base64 Decoding Error:", e)  # Debugging
        return None  # Return None if invalid

# App Layout
st.set_page_config(layout="wide")

st.title("🏆 Staff Incentive Dashboard")

# Load data
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="DATA", ttl=10)
df = df.dropna(thresh=2)

# Sort by incentive (Descending)
df = df.sort_values(by="INCENTIVE", ascending=False).reset_index(drop=True)

# Sidebar for ranking
st.sidebar.header("📊 Staff Ranking")
st.sidebar.dataframe(df[['STAFF NAME', 'INCENTIVE', 'DEPARTMENT']])

# Slideshow Controls
if "index" not in st.session_state:
    st.session_state.index = 0

# Display staff info dynamically
staff_name = df.iloc[st.session_state.index]["STAFF NAME"]
st.subheader(f"🌟 {staff_name}")

# Get and display image
image_data = df.iloc[st.session_state.index]["PICTURE"]

if pd.isna(image_data) or image_data.strip() == "":
    st.write("🚫 No Image Available")
elif image_data.startswith("http"):  # URL-based image (Google Drive, etc.)
    st.image(get_image_url(image_data), width=300)
else:  # Base64 Image
    image = decode_image(image_data)
    if image:
        st.image(image, width=300)
    else:
        st.write("🚫 No Image Available")

# Format Incentive (Handle NaN)
incentive_value = df.iloc[st.session_state.index]['INCENTIVE']
incentive_value = 0.00 if pd.isna(incentive_value) else float(incentive_value)

st.metric(label="💰 Incentive Earned", value=f"${incentive_value:,.2f}")

# Auto-Slideshow Feature
st.sidebar.markdown("### ⏳ Auto-Slideshow")
auto_slide = st.sidebar.checkbox("Enable Slideshow", value=False)
slide_delay = st.sidebar.slider("Slide Delay (seconds)", 2, 10, 2)

col1, col2, col3 = st.columns([1, 2, 1])

if col1.button("⏮️ Previous"):
    st.session_state.index = (st.session_state.index - 1) % len(df)

if col2.button("⏭️ Next"):
    st.session_state.index = (st.session_state.index + 1) % len(df)

# Auto-slide
if auto_slide:
    time.sleep(slide_delay)
    st.session_state.index = (st.session_state.index + 1) % 5
    st.rerun()
