import streamlit as st
import requests
import os

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
                if not filename or "." not in filename:
                    filename = "image_downloaded.jpg"

                st.success(f"Image downloaded: {filename} ({len(r.content)} bytes)")
                st.image(r.content, caption=filename)

                # Button for direct download to the user's PC
                st.download_button(
                    label="Download image",
                    data=r.content,
                    file_name=filename,
                    mime=content_type
                )
        except Exception as e:
            st.error(f"Error: {str(e)}")
