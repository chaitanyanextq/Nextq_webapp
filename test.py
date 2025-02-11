import streamlit as st
import requests
import time

# API Endpoints
API_URL = "http://127.0.0.1:8000/store-url/"  # Change this if hosted on another server
DOWNLOAD_URL = "http://127.0.0.1:8000/download-file/"

st.title("FastAPI URL Submission & File Download")

# User input for the URL
url = st.text_input("Enter a URL:", "")

# Placeholder for download button (hidden initially)
download_button_placeholder = st.empty()

if st.button("Submit"):
    if url:
        try:
            check = requests.get(url, timeout=5)  # Check if the URL is reachable (5 sec timeout)
            if check.status_code == 200:
                response = requests.post(API_URL, json={"url": url})
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ URL Stored Successfully!")

                    # Wait a bit to ensure the file is created before download
                    time.sleep(1)

                    # Check if the file exists before showing the download button
                    file_check = requests.get(DOWNLOAD_URL)
                    if file_check.status_code == 200:
                        with download_button_placeholder:
                            st.download_button(
                                label="📥 Download Report",
                                data=file_check.content,
                                file_name="stored_urls.docx",
                                mime="application/octet-stream",
                            )
                    else:
                        st.warning("⚠️ File is not available yet. Please try again.")
                else:
                    st.error(f"❌ Error from FastAPI: {response.json()}")

            else:
                st.error("❌ The provided URL is unreachable. Please check and try again.")
        
        except requests.exceptions.RequestException:
            st.error("❌ Invalid or Unreachable URL. Please check and try again.")

    else:
        st.warning("⚠️ Please enter a valid URL.")
