import streamlit as st
import os
import json

# Folders and files
upload_folder = "upload"
covers_folder = "covers"
metadata_file = "sheet_metadata.json"

# Ensure the folders exist
os.makedirs(upload_folder, exist_ok=True)
os.makedirs(covers_folder, exist_ok=True)

# Load metadata if it exists
if os.path.exists(metadata_file):
    with open(metadata_file, "r") as f:
        sheet_metadata = json.load(f)
else:
    sheet_metadata = {}

# Admin app title
st.title("Admin App - Manage Sheet Music")

# Rest of the admin app (sheet music management)
st.header("Upload New Sheet Music")
uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)

if uploaded_files:
    # Save the uploaded files
    for uploaded_file in uploaded_files:
        file_path = os.path.join(upload_folder, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded {uploaded_file.name}")

# Select a file to add metadata, cover, and link
st.header("Add Metadata, Cover, and Link to Uploaded Files")
uploaded_file_names = [f for f in os.listdir(upload_folder) if f.endswith(".pdf")]
if uploaded_file_names:
    selected_file = st.selectbox("Select a file to add metadata, cover, and link", uploaded_file_names)

    # Add metadata for the selected file
    st.subheader(f"Add Metadata for {selected_file}")
    title = st.text_input("Title", key=f"title_{selected_file}")
    key = st.text_input("Key", key=f"key_{selected_file}")

    # Add link for the selected file
    st.subheader(f"Add Preview Link for {selected_file}")
    preview_link = st.text_input("Preview Link (e.g., Instagram post URL)", key=f"link_{selected_file}")

    # Upload cover image
    st.subheader(f"Upload Cover for {selected_file}")
    cover_image = st.file_uploader("Upload a cover image (JPEG/PNG)", type=["jpg", "jpeg", "png"], key=f"cover_{selected_file}")

    if st.button(f"Save Metadata, Cover, and Link for {selected_file}"):
        # Save metadata
        sheet_metadata[selected_file] = {
            "title": title,
            "key": key,
            "preview_link": preview_link,  # Save the preview link
        }
        with open(metadata_file, "w") as f:
            json.dump(sheet_metadata, f)

        # Save cover image
        if cover_image:
            cover_path = os.path.join(covers_folder, selected_file.replace(".pdf", ".jpg"))
            with open(cover_path, "wb") as f:
                f.write(cover_image.getbuffer())
            st.success(f"Cover saved for {selected_file}!")
        else:
            st.warning("No cover image uploaded.")
else:
    st.warning("No files uploaded yet.")

# Display existing sheet music metadata
st.header("Existing Sheet Music Metadata")
# Iterate over a copy of the dictionary to avoid runtime errors
for file, metadata in list(sheet_metadata.items()):
    st.subheader(file)
    st.write(f"**Title:** {metadata.get('title', 'N/A')}")
    st.write(f"**Key:** {metadata.get('key', 'N/A')}")
    st.write(f"**Preview Link:** {metadata.get('preview_link', 'N/A')}")
    if st.button(f"Delete {file}", key=f"delete_{file}"):
        # Delete the file, cover, and its metadata
        os.remove(os.path.join(upload_folder, file))
        cover_path = os.path.join(covers_folder, file.replace(".pdf", ".jpg"))
        if os.path.exists(cover_path):
            os.remove(cover_path)
        del sheet_metadata[file]
        with open(metadata_file, "w") as f:
            json.dump(sheet_metadata, f)
        st.success(f"Deleted {file}")
        