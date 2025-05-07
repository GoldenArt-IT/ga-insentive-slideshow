# GA Insentive Slideshow

A Streamlit app to display staff and department rankings based on Google Sheets data.

🔗 **Try it here:** [https://ga-tv-incentive.streamlit.app/](https://ga-tv-incentive.streamlit.app/)

## Features

- **Top 10 Staff Slideshow**  
  - Shows individual grades, happy-point balance and picture.  
  - Auto-advances every *n* seconds.  
- **Department Ranking**  
  - Ranks departments by average “TOTAL GRADE %”.  
  - Displays top 3 with small team photos.  
- **Google Sheets Integration**  
  - Read and write CRUD via `GSheetsConnection`.  
- **Image Handling**  
  - Fetch & compress images from URLs or Base64 strings.  
  - Supports Google Drive links and arbitrary URLs.  
  - Displays via `st.image()`.
  
