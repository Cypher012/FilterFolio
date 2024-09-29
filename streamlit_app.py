import io, base64
import cv2, numpy as np
import streamlit as st
from PIL import Image
from filters import *
import streamlit.components.v1 as components
from html_script import *



def get_image_download_link(img, filename, text):
    buffered = io.BytesIO()
    img.save(buffered, format='JPEG')
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/txt;base64,{img_str}" download="{filename}">{text}</a>'
    return href

def markdown_text(text, mb=0):
    st.markdown(
        f"""
        <h1 style='
        background: linear-gradient(90deg, #FF5733, #FFC300);
        -webkit-background-clip: text;
        color: transparent;
        font-size: 40px;
        margin-bottom: {mb}px
        '>
        {text}
        </h1>
        """,
        unsafe_allow_html=True
    )

markdown_text("FilterFolio: A Collection of Artistic Image Filters", 70)
uploaded_file = st.file_uploader("Choose an image file:", type=["png", "jpg"])

if uploaded_file is not None:
    raw_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(raw_bytes, cv2.IMREAD_COLOR)
    input_col, output_col = st.columns(2)

    with input_col:
        markdown_text("Original")
        st.image(img, channels='BGR', use_column_width=True)
        st.markdown("<div style='margin-bottom: 5rem'></div>", unsafe_allow_html=True)
        markdown_text("Filters")

    option = st.selectbox("Select a filter", [
        "None", "Black and White", "Sepia / Vintage", "Vignette Effect", 
        "Pencil Sketch", "Canny Edge Detection", "Embossed Edges", 
        "Blur Image", "Outline", "Sharpening Filter", "HDR Effect", 
        "Warm Effect", "Cold Effect"
    ])

    html_content()
    # Render the HTML content
    components.html(html_content(), height=200)

    # Slider for vignette effect
    vignette_level = 2  # default value
    if option == "Vignette Effect":
        vignette_level = st.slider("Level", 0, 5, vignette_level)
    if option == "Blur Image":
        ksize = st.slider("Blur kernel size", 1, 15, 9, step=2)
    if option == 'Canny Edge Detection':
        slider = st.slider(
    "Threshold", 0, 255, (150, 200)
    )
        
    

    output_image = None
    color = 'BGR'

    # Generate filtered image based on the selected option
    if option == "Black and White":
        output_image = bw_filter(img)
        
        color = 'GRAY'
    elif option == "Sepia / Vintage":
        output_image = sepia(img)
    elif option == "Vignette Effect":
        output_image = vignette(img, vignette_level)
    elif option == "Pencil Sketch":
        output_image = pencil_sketch(img)
        color = "GRAY"
    elif option == "Canny Edge Detection":
        output_image = Canny_edge(img,slider[0], slider[1])
        color = "GRAY"
    elif option == "Embossed Edges":
        output_image = embossed_edges(img)
    elif option == "Blur Image":
        output_image = blur_img(img, ksize)
    elif option == "Outline":
        output_image = outline(img)
    elif option == "Sharpening Filter":
        output_image = sharping_filter(img)
    elif option == "HDR Effect":
        output_image = HDR(img)
    elif option == "Warm Effect":
        output_image = Warm_filter(img)
    elif option == "Cold Effect":
        output_image = Cold_filter(img)

    with output_col:
        markdown_text("Output")
        if output_image is not None:
            st.image(output_image, channels=color)
            if color == 'BGR':
                result = Image.fromarray(output_image[:, :, ::-1])
            else:
                result = Image.fromarray(output_image)
            # Display link
            st.markdown(get_image_download_link(result, "output.png", "Download Output"), unsafe_allow_html=True)
