import streamlit as st
import os
import json
import base64
from PIL import Image

# Folders and files
upload_folder = "upload"
covers_folder = "covers"
metadata_file = "sheet_metadata.json"
stats_file = "download_stats.json"

# Ensure the folders exist
os.makedirs(upload_folder, exist_ok=True)
os.makedirs(covers_folder, exist_ok=True)

# Load metadata and download statistics
if os.path.exists(metadata_file):
    with open(metadata_file, "r") as f:
        sheet_metadata = json.load(f)
else:
    sheet_metadata = {}

if os.path.exists(stats_file):
    with open(stats_file, "r") as f:
        download_stats = json.load(f)
else:
    download_stats = {}

# Add custom CSS for spacing and centering the profile picture
st.markdown(
    """
    <style>
        .sheet-row {
            margin-bottom: 3rem; /* Adjust this value to increase/decrease row spacing */
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sheet Music Section
st.header("My Sheet Music")  # Main section title

# Function to display a single sheet music card
def display_sheet_card(file, metadata):
    file_path = os.path.join(upload_folder, file)
    cover_path = os.path.join(covers_folder, file.replace(".pdf", ".jpg"))

    # Display the cover image
    if os.path.exists(cover_path):
        st.image(cover_path, use_container_width=True)  # Updated parameter
    else:
        st.warning("No cover image available.")

    # Center the title
    st.markdown(
        f"""
        <div style="text-align: center;">
            <p style="font-size: 1.1rem; font-weight: bold; margin-bottom: 0.25rem;">{metadata.get('title', 'N/A')}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Download link (underlined and same color as default text)
    with open(file_path, "rb") as f:
        pdf_data = f.read()
    st.markdown(
        f"""
        <div style="text-align: center;">
            <a href="data:application/pdf;base64,{base64.b64encode(pdf_data).decode('utf-8')}" download="{file}" style="text-decoration: underline; color: inherit; font-weight: bold; font-size: 1rem;">Download</a>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Track downloads
    if file not in download_stats:
        download_stats[file] = {"downloads": 0, "title": metadata.get("title", file)}
    download_stats[file]["downloads"] += 1
    with open(stats_file, "w") as f:
        json.dump(download_stats, f)

# Display sheet music in a grid (3 per row)
files = os.listdir(upload_folder)

# Sort files by modification time (most recent first)
files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(upload_folder, x)), reverse=True)

if files:
    # Group files into rows of 3
    for i in range(0, len(files), 3):
        row_files = files[i:i + 3]
        # Create a container for the row
        with st.container():
            # Add a custom class to the row container
            st.markdown('<div class="sheet-row">', unsafe_allow_html=True)
            # Create columns for the row
            cols = st.columns(3)
            for j, file in enumerate(row_files):
                metadata = sheet_metadata.get(file, {})
                with cols[j]:
                    display_sheet_card(file, metadata)
            # Close the custom class div
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.warning("No sheet music available.")