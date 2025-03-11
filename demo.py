import streamlit as st
import streamlit_antd_components as sac
import pandas as pd
import time
from streamlit_gsheets import GSheetsConnection
import base64
from io import BytesIO
from PIL import Image
import requests


#----------------------------------------------------------BACKEND--------------------------------------------------------------

st.set_page_config(layout="wide")

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
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="DATA", ttl=10)
df = df.dropna(thresh=2)
df = df.sort_values(by="INCENTIVE", ascending=False).reset_index(drop=True)

selected_departments = ['INTERIOR', 'WELDER', 'FRMAE', 'FABRIC', 'SEWING', 'SPONGE', 'SPRAY', 'PACKING', 'ASSEMBLY', 'OUTDOOR']
df = df[df['DEPARTMENT'].isin(selected_departments)]

# Side Bar
st.sidebar.header("📊 Staff Ranking")
st.sidebar.dataframe(df[['STAFF NAME', 'INCENTIVE', 'DEPARTMENT']])

st.sidebar.markdown("### ⏳ Auto-Slideshow")




# Initialize session state for slideshow
if "index" not in st.session_state:
    st.session_state.index = 0

# Get staff details
staff_name = df.iloc[st.session_state.index]["STAFF NAME"]
image_data = df.iloc[st.session_state.index]["PICTURE"]
incentive_value = df.iloc[st.session_state.index]['INCENTIVE']
department_value = df.iloc[st.session_state.index]['DEPARTMENT']
incentive_value = 0.00 if pd.isna(incentive_value) else float(incentive_value)

department_totals = df.groupby("DEPARTMENT")["INCENTIVE"].sum().reset_index()
department_incentive = department_totals[department_totals["DEPARTMENT"] == department_value]["INCENTIVE"].values[0]


#---------------------------------------------------------UI DESIGN-------------------------------------------------------------



auto_slide = st.sidebar.checkbox("Enable Slideshow", value=True)
slide_delay = st.sidebar.slider("Slide Delay (seconds)", 2, 10, 8)

segment_1, segment_2 = st.columns([5,5])
with segment_1:
    with st.container():
        sac.segmented(
            items=[
                sac.SegmentedItem(label='THIS WEEK', icon='fire'),
                sac.SegmentedItem(label='THIS MONTH', icon='water'),
            ], align='center', size='sm', radius='xl'
        )

title_1, title_2 = st.columns([5,5])
with title_1:
    st.title("🏆 Top 10 Staff Terbaik !")
with title_2:
    st.title("🫣 Department Kau Perform Tak ?")

body_1, body_2 = st.columns([5,5])
with body_1:
    with st.container():
        st.subheader(f"🌟 {staff_name}")

        with st.container():

            col_1, col_2, col_3 = st.columns([0.5,1,0.5])
            with col_2:

                # Display Image
                if pd.isna(image_data) or image_data.strip() == "":
                    st.write("🚫 No Image Available")
                elif image_data.startswith("http"):
                    st.image(get_image_url(image_data), width=400)
                else:
                    image = decode_image(image_data)
                    st.image(image, width=300) if image else st.write("🚫 No Image Available")

        incentive_1, incentive_2 = st.columns([1,1])
        with incentive_1:
            with st.container():
                st.subheader("Duit yang Kau Dapat! 💵")
                st.markdown("<h1 style='text-align: left;'> " f"RM {incentive_value:,.2f}" "</h1>", unsafe_allow_html=True)
        with incentive_2:
            with st.container():
                st.subheader("Total Duit Dept Kau!💰")
                st.markdown("<h1 style='text-align: left;'> " f"RM {department_incentive:,.2f}" "</h1>", unsafe_allow_html=True)
with body_2:
    with st.container(border=True, height=700):
        st.write("test_body_2")

# Auto-slide
if auto_slide:
    time.sleep(slide_delay)
    st.session_state.index = (st.session_state.index + 1) % 10  # Loop Top 10 Staff Only
    st.rerun()