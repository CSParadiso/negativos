import streamlit as st
from PIL import Image, ImageOps
from io import BytesIO
import base64

# Constants for allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Function to check allowed file types
def allowed_file(filename):
    """Check if the file is allowed based on its extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@st.cache_data
# Function to process image: invert colors
def process_image(image):
    """Process the image by inverting the colors."""
    try:
        img = Image.open(image)
        inverted_img = ImageOps.invert(img.convert('RGB'))  # Invert colors
        return inverted_img
    except Exception as e:
        st.error(f"Error procesando imagen: {str(e)}")
        return None

# Streamlit UI
st.title("Desde NEGATIVOS a Color")

# File uploader in Streamlit
uploaded_files = st.file_uploader("Subir archivos", type=['png', 'jpg', 'jpeg'], accept_multiple_files=True)

# If files are uploaded
if uploaded_files:
    # List to store processed images for download
    processed_images = []
    
    for uploaded_file in uploaded_files:
        if allowed_file(uploaded_file.name):
            # Process image
            processed_img = process_image(uploaded_file)
            if processed_img:
                # Convert processed image to BytesIO object for memory handling
                img_byte_arr = BytesIO()
                processed_img.save(img_byte_arr, format="PNG")
                img_byte_arr.seek(0)

                # Encode image to base64
                img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode("utf-8")

                # Display the processed image
                st.image(processed_img, caption=f"Imagen procesada {uploaded_file.name}", use_container_width=True)

                # JavaScript download button using base64 data
                download_button_html = f"""
                <a href="data:image/png;base64,{img_base64}" download="PARADISOFT_{uploaded_file.name}">
                    <button>Descargar {uploaded_file.name}</button>
                </a>
                """
                st.markdown(download_button_html, unsafe_allow_html=True)
        else:
            st.warning(f"El archivo {uploaded_file.name} no es una imagen válida. Los formatos soportados son: png, jpg, jpeg.")
