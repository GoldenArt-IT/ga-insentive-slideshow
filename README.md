# 🚀 Staff Performance Dashboard

A **Streamlit** app that displays and auto-cycles staff performance rankings, incentives, and department statistics with images. Integrated with **Google Sheets** for live data updates.

---

## 📑 Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Example Workflow](#example-workflow)
- [Project Structure](#project-structure)
- [Reference](#reference)

---

## ✨ Features

- Google Sheets data integration
- Top 10 staff ranking slideshow
- Department performance comparison
- Staff photos with Google Drive and Base64 support
- Dynamic session state for auto-slideshow
- Fully responsive layout

---

## ⚙️ Installation

1. **Clone the repository**

   ```
   git clone https://github.com/your-org/staff-performance-dashboard.git
   cd staff-performance-dashboard
   ```

2. **Install dependencies**

   ```
   pip install -r requirements.txt
   ```

   Example `requirements.txt`:

   ```
   streamlit
   streamlit_gsheets
   pandas
   pillow
   requests
   numpy
   streamlit-antd-components
   ```

3. **Create `secrets.toml`**

   ```toml
   [connections.gsheets]
   email = "your_service_account_email"
   private_key = "-----BEGIN PRIVATE KEY-----\n..."

   [allowed_users]
   emails = ["user1@example.com", "user2@example.com"]
   ```

4. **Run the app**

   ```
   streamlit run app.py
   ```

---

## ⚙️ Configuration

- **Google Sheets**
  - Your Google Sheet must have a `DATA` worksheet with columns:
    - `STAFF NAME`
    - `DEPARTMENT`
    - `PICTURE` (Google Drive link or Base64)
    - `TOTAL GRADE %`
    - `OUTPUT PARTICIPATION GRADE`
    - `COMMITMENT ON TASK GRADE`
    - `KNOWLEDGE & QCQA GRADE`
    - `ATTENDANCE GRADE`
    - `COMMUNICATION GRADE`
    - `TOTAL GRADE`
    - `HAPPY POINTS BALANCE`
    - `INCENTIVE`

- **Departments Filtered**
  - Only these departments are included in ranking:
    - INTERIOR, WELDER, FRAME, FABRIC, SEWING, SPONGE, SPRAY, PACKING, ASSEMBLY, OUTDOOR

- **Slideshow**
  - Enable or disable from the sidebar.
  - Adjust slide delay (2–10 seconds).

---

## 🛠️ Usage

1. **Login**
   - Launch the app.
   - Sidebar shows Top 10 staff dataframe.
   - Enable slideshow if desired.

2. **Slideshow Display**
   - Left panel shows staff name, picture, grades, and incentives.
   - Right panel shows department rankings with cumulative images.

3. **Auto Cycle**
   - When enabled, the slideshow advances every few seconds.

---

## 💡 Example Workflow

**Scenario:**

- Staff "Ahmad"
  - Department: SEWING
  - Incentive: RM200
  - Grades:
    - OUTPUT: A
    - KOMITMEN: S
    - ILMU & QCQA: B
    - KEHADIRAN: A
    - KOMUNIKASI: A
    - KESELURUHAN: S+
    - HAPPY POINTS: 75

---

## 📂 Project Structure

```
staff-performance-dashboard/
├── app.py              # Main Streamlit app
├── requirements.txt    # Dependencies
└── README.md           # This README
```

---

## 📚 Reference

- [Streamlit Documentation](https://docs.streamlit.io)
- [streamlit_gsheets](https://github.com/streamlit/streamlit-gsheets)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Pillow Docs](https://pillow.readthedocs.io)
- [NumPy Docs](https://numpy.org)

---
