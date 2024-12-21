from PIL import Image, ImageOps
import streamlit as st
from io import BytesIO

# Constants for allowed file types
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Function to check allowed file types
def allowed_file(filename):
    """Check if the file is allowed based on its extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
st.title("Desde negativos fotográficos a fotos digitales a Color")

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
                
                # Add to processed_images list for rendering and download link
                processed_images.append({
                    'filename': f"postivo_{uploaded_file.name}",
                    'image': img_byte_arr
                })
                
                # Display the processed image
                st.image(processed_img, caption=f"Imagen procesada {uploaded_file.name}", use_container_width=True)

                # Provide download link for processed image (in memory)
                st.download_button(
                    label=f"Descargar {uploaded_file.name}",
                    data=img_byte_arr,
                    file_name=f"inverted_{uploaded_file.name}",
                    mime="image/png"
                )
        else:
            st.warning(f"El archivo {uploaded_file.name} no es una imagen válida. Los formatos soportados son: png, jpg, jpeg.")

# Footer with author info (using semantic HTML <footer>)
st.markdown("""
    <footer style="position: fixed; bottom: 0; left: 0; width: 100%; background-color: rgba(0, 0, 0, 0.5); color: white; text-align: center; padding: 10px;">
        <p style="margin: 0;">Creado por: Cayetano Simón Paradiso | <a href="https://github.com/CSParadiso" target="_blank" style="color: white;">@CSParadiso</a></p>
    </footer>
""", unsafe_allow_html=True)
