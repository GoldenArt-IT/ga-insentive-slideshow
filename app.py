import streamlit as st
import streamlit_antd_components as sac
import pandas as pd
import time
from streamlit_gsheets import GSheetsConnection
import base64
from io import BytesIO
from PIL import Image
import requests
import numpy as np


#----------------------------------------------------------BACKEND--------------------------------------------------------------

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")

def get_image_url_display(url):
    """Convert Google Drive link to a direct image URL."""
    if isinstance(url, str) and "drive.google.com" in url:
        if "/file/d/" in url:
            file_id = url.split("/d/")[1].split("/")[0]
            return requests.get(f"https://drive.google.com/uc?export=view&id={file_id}").content
        elif "id=" in url:
            file_id = url.split("id=")[1]
            return requests.get(f"https://drive.google.com/uc?export=view&id={file_id}").content
    return url  # Return the original URL if it's not from Google Drive

def decode_image_display(base64_string):
    """Convert Base64 string to an image, handling errors safely."""
    try:
        base64_string = base64_string.strip()
        image_bytes = base64.b64decode(base64_string)
        return Image.open(BytesIO(image_bytes))
    except Exception:
        return None

@st.cache_data
def get_image_url(url, max_width=200, quality=20):
    """Fetch and compress images from URLs."""
    try:
        if "drive.google.com" in url:
            if "/file/d/" in url:
                file_id = url.split("/d/")[1].split("/")[0]
            elif "id=" in url:
                file_id = url.split("id=")[1]
            else:
                return None
            url = f"https://drive.google.com/uc?export=view&id={file_id}"
        
        response = requests.get(url, stream=True)
        image = Image.open(BytesIO(response.content))
        
        # Convert to JPEG if PNG and reduce quality
        image = image.convert("RGB")
        image.thumbnail((max_width, max_width))  # Resize
        output = BytesIO()
        image.save(output, format="JPEG", quality=quality, optimize=True)
        output.seek(0)

        return Image.open(output)
    except:
        return None

@st.cache_data
def decode_image(base64_string, max_width=200, quality=20):
    """Convert Base64 string to a compressed image."""
    try:
        image_bytes = base64.b64decode(base64_string.strip())
        image = Image.open(BytesIO(image_bytes))
        
        # Convert to JPEG and reduce quality
        image = image.convert("RGB")
        image.thumbnail((max_width, max_width))  # Resize
        output = BytesIO()
        image.save(output, format="JPEG", quality=quality, optimize=True)
        output.seek(0)

        return Image.open(output)
    except:
        return None

# Load Data
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="DATA", ttl=360)
df = df.dropna(thresh=2)
df = df.sort_values(by="TOTAL GRADE %", ascending=False).reset_index(drop=True)

selected_departments = ['INTERIOR', 'WELDER', 'FRAME', 'FABRIC', 'SEWING', 'SPONGE', 'SPRAY', 'PACKING', 'ASSEMBLY', 'OUTDOOR']
df = df[df['DEPARTMENT'].isin(selected_departments)]

# Initialize session state for slideshow
if "index" not in st.session_state:
    st.session_state.index = 0

# Get staff details
staff_name = df.iloc[st.session_state.index]["STAFF NAME"]
image_data = df.iloc[st.session_state.index]["PICTURE"]
incentive_value = df.iloc[st.session_state.index]['INCENTIVE']
department_value = df.iloc[st.session_state.index]['DEPARTMENT']
incentive_value = 0.00 if pd.isna(incentive_value) else float(incentive_value)

output_grade = df.iloc[st.session_state.index]["OUTPUT PARTICIPATION GRADE"]
commitment_grade = df.iloc[st.session_state.index]["COMMITMENT ON TASK GRADE"]
knowledge_grade = df.iloc[st.session_state.index]["KNOWLEDGE & QCQA GRADE"]
attendance_grade = df.iloc[st.session_state.index]["ATTENDANCE GRADE"]
communication_grade = df.iloc[st.session_state.index]["COMMUNICATION GRADE"]
total_grade = df.iloc[st.session_state.index]["TOTAL GRADE"]
happypoint_grade = df.iloc[st.session_state.index]["HAPPY POINTS BALANCE"]

department_totals = df.groupby("DEPARTMENT")["INCENTIVE"].sum().reset_index()
department_incentive = department_totals[department_totals["DEPARTMENT"] == department_value]["INCENTIVE"].values[0]


#---------------------------------------------------------UI DESIGN-------------------------------------------------------------


title_1, title_2 = st.columns([1,1])

st.sidebar.header("📊 Staff Ranking")
st.sidebar.dataframe(df[['STAFF NAME', 'TOTAL GRADE', 'TOTAL GRADE %']])
with st.sidebar.expander("Slideshow Enabler"):
    auto_slide = st.sidebar.checkbox("Enable Slideshow", value=True)
    slide_delay = st.sidebar.slider("Slide Delay (seconds)", 2, 10, 10)

with title_1:
    st.markdown(f"""<h2>🏆 Top 10 Staff Terbaik !</h2>""", unsafe_allow_html=True)

    with st.container():
        st.subheader(f"🌟 {staff_name}")

        with st.container():

            col_1, col_2 = st.columns([1,0.8])
            with col_1:

                # Display Image
                if pd.isna(image_data) or image_data.strip() == "":
                    st.write("🚫 No Image Available")
                elif image_data.startswith("http"):
                    st.image(get_image_url_display(image_data), width=350)
                else:
                    image = decode_image_display(image_data)
                    st.image(image, width=300) if image else st.write("🚫 No Image Available")
            
            with col_2:

                grade_title_map = ["OUTPUT", "KOMITMEN", "ILMU & QCQA", "KEHADIRAN", "KOMUNIKASI", "KESELURUHAN", "HAPPY POINTS !"]
                grade_map = [output_grade, commitment_grade, knowledge_grade, attendance_grade, commitment_grade, total_grade, str(happypoint_grade)]
                for x in range(7):
                    with st.container(height=30):

                        if grade_map[x] == "S": st.markdown(f"**{grade_title_map[x]}** : 🔥 **{grade_map[x]}**")
                        elif grade_map[x] == "F": st.markdown(f"**{grade_title_map[x]}** : 🔴 :red-background[**{grade_map[x]}**]")
                        elif grade_map[x] == "A": st.markdown(f"**{grade_title_map[x]}** : 🔵 **{grade_map[x]}**")
                        elif grade_map[x] == "S+": st.markdown(f"**{grade_title_map[x]}** : 🔥🔥 **{grade_map[x]}** 🔥🔥")
                        else: st.markdown(f"**{grade_title_map[x]}** : **{grade_map[x]}**")


with title_2:
    st.markdown(f"""<h2>🚀 Department Ranking !</h2>""", unsafe_allow_html=True)
    
    with st.container():
        department_table = pd.pivot_table(df, values='TOTAL GRADE %', index=['DEPARTMENT'], aggfunc=np.sum)
        staff_table = pd.pivot_table(df, values='STAFF NAME', index=['DEPARTMENT'], aggfunc="count")
        staff_table = staff_table.rename(columns={"STAFF NAME": "STAFF COUNT"})
        staff_ranking_table = department_table.merge(staff_table, on="DEPARTMENT", how="outer").fillna(0)
        staff_ranking_table["Avg Percentage per Staff"] = staff_ranking_table["TOTAL GRADE %"] / staff_ranking_table["STAFF COUNT"]
        total_avg_incentive = staff_ranking_table["Avg Percentage per Staff"].sum()
        staff_ranking_table["Department Percentage"] = (staff_ranking_table ["Avg Percentage per Staff"] / total_avg_incentive) * 100
        staff_ranking_table = staff_ranking_table.sort_values(by=['Department Percentage'], ascending=False)

        for x in range(3):
            with st.container(height=140):
                INDEX_DEPARTMENT = staff_ranking_table.index[x]
                INDEX_PERCENTAGE = round(staff_ranking_table.iloc[x][-1], 2)
                # INDEX_INCENTIVE = staff_ranking_table.iloc[x][0] 

                if x == 0:
                    st.markdown(f"""<h4>🥇 {INDEX_DEPARTMENT} - {INDEX_PERCENTAGE}%</h4>""", unsafe_allow_html=True)
                if x == 1:
                    st.markdown(f"""<h4>🥈 {INDEX_DEPARTMENT} - {INDEX_PERCENTAGE}%</h4>""", unsafe_allow_html=True)
                if x == 2:
                    st.markdown(f"""<h4>🥉 {INDEX_DEPARTMENT} - {INDEX_PERCENTAGE}%</h4>""", unsafe_allow_html=True)
                elif x > 2:
                    st.markdown(f"""<h4> {x+1}. {INDEX_DEPARTMENT} - {INDEX_PERCENTAGE}%</h4>""", unsafe_allow_html=True)

                staff_image = df[df['DEPARTMENT'] == INDEX_DEPARTMENT]
                valid_images = [
                    get_image_url(img) if str(img).startswith("http") else decode_image(img) 
                    if not pd.isna(img) and str(img).strip() != "" else None
                    for img in staff_image["PICTURE"]
                ]
                image_list = [img for img in valid_images if img is not None]
                if image_list:
                    st.image(image_list, width=50)
                else:
                    st.write("🚫 No Images Available")

# Auto-slide
if auto_slide:
    time.sleep(slide_delay)
    st.session_state.index = (st.session_state.index + 1) % 10  # Loop Top 10 Staff Only
    st.rerun()