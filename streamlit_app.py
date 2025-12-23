import streamlit as st
import requests
import os

SAVE_DIR = "Fetched_Images"
os.makedirs(SAVE_DIR, exist_ok=True)

st.title("Ubuntu Image Fetcher")

url = st.text_input("Enter the image URL:")

if st.button("Download image"):
    if not url.strip():
        st.error("Enter a valid URL.")
    else:
        try:
            r = requests.get(url.strip(), timeout=10)
            content_type = r.headers.get("Content-Type", "")
            if "image" not in content_type:
                st.error("The URL does not point to an image.")
            elif len(r.content) > 10 * 1024 * 1024:
                st.error("Image too large (>10MB).")
            else:
                filename = os.path.basename(url.strip())
                if filename not in filename or "." not in filename:
                    filename = "image_downloaded.jpg"
                filepath = os.path.join(SAVE_DIR, filename)
                if os.path.exists(filepath):
                    st.warning(f"Already exists in {filepath}")
                else:
                    with open(filepath, "wb") as f:
                        f.write(r.content)
                    st.success(f"Downloaded: {filepath} ({len(r.content)} bytes)")
        except Exception as e:
            st.error(f"Error: {str(e)}")
