import cv2, numpy as np
import streamlit as st
from scipy.interpolate import UnivariateSpline

@st.cache_data
def bw_filter(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img_gray

@st.cache_data
def sepia(img):
    sepia_matrix = [
    [0.393, 0.769, 0.189],
    [0.349, 0.686, 0.168],
    [0.272, 0.534, 0.131]
    ]
    img_sepia = img.copy()
    # Converting to RGB as sepia matrix below is for RGB.
    img_sepia = cv2.cvtColor(img_sepia, cv2.COLOR_BGR2RGB)
    img_sepia = np.array(img_sepia, np.float64)
    img_sepia = cv2.transform(img_sepia, np.matrix(sepia_matrix))
    # Clip values to the range [0, 255].
    img_sepia = np.clip(img_sepia, 0, 255)
    img_sepia = np.array(img_sepia, np.uint8)
    img_sepia = cv2.cvtColor(img_sepia, cv2.COLOR_RGB2BGR)
    return img_sepia

@st.cache_data
def vignette(img, level = 2):
    height , width = img.shape[:2]

    #  Generate vignette mask using Gaussian kernals
    X_resultant_kernel = cv2.getGaussianKernel(width, width/level)
    Y_resultant_kernel = cv2.getGaussianKernel(height, height/level)

    # Generate resultant_kernel matrix
    kernel = Y_resultant_kernel * X_resultant_kernel.T
    mask = kernel / kernel.max()

    image_vignette = np.copy(img)

    # Applying the mask to each channel in the input image
    for i in range(3):
        image_vignette[:, :, i] = image_vignette[: , :, i] * mask

    return image_vignette

@st.cache_data
def blur_img(img, k=9):
    blur = cv2.GaussianBlur(img, (k,k), 0, 0)
    return blur

@st.cache_data
def Canny_edge(img, thresh1= 150, thresh2 = 200):
    img_blur = cv2.GaussianBlur(img, (5,5), 0, 0)
    img_edges = cv2.Canny(img_blur, thresh1, thresh2)
    return img_edges

@st.cache_data
def embossed_edges(img):
    kernel = np.array([
        [0, -3, -3], 
        [3,  0, -3], 
        [3,  3,  0]
    ])
    img_emboss = cv2.filter2D(img, -1, kernel)
    return img_emboss

@st.cache_data
def outline(img, k = 9):
    k = max(k, 9)
    kernel = np.array([
        [-1, -1, -1],
        [-1,  k, -1],
        [-1, -1, -1]
        ])
    img_outline = cv2.filter2D(img, ddepth = -1, kernel = kernel)
    return img_outline

@st.cache_data
def pencil_sketch(img):
    img_blur = cv2.GaussianBlur(img, (5,5), 0, 0)
    img_sketch_bw, _ = cv2.pencilSketch(img_blur)
    return img_sketch_bw

@st.cache_data
def sharping_filter(img, k=5):
    kernel = np.array([[ 0, -1,  0],
                       [-1,  k, -1],
                       [ 0, -1,  0]])
    img_sharp = cv2.filter2D(img, ddepth = -1, kernel = kernel)
    # Clip values to the range [0, 255].
    img_sharp = np.clip(img_sharp, 0, 255)
    return img_sharp

@st.cache_data
def HDR(img):
    img_hdr = cv2.detailEnhance(img, sigma_s = 10, sigma_r = 0.1)
    return img_hdr

@st.cache_data
def Warm_filter(img):
    # We are giving y values for a set of x values.
    # And calculating y for [0-255] x values accordingly to the given range.
    increase_table = UnivariateSpline(x=[0, 64, 128, 255], y=[0, 75, 155, 255])(range(256))
 
    # Similarly construct a lookuptable for decreasing pixel values.
    decrease_table = UnivariateSpline(x=[0, 64, 128, 255], y=[0, 45, 95, 255])(range(256))
    # Split the blue, green, and red channel of the image.
    blue_channel, green_channel, red_channel  = cv2.split(img)
    
    # Increase red channel intensity using the constructed lookuptable.
    red_channel = cv2.LUT(red_channel, increase_table).astype(np.uint8)
    
    # Decrease blue channel intensity using the constructed lookuptable.
    blue_channel = cv2.LUT(blue_channel, decrease_table).astype(np.uint8)
    
    # Merge the blue, green, and red channel. 
    filterd_img = cv2.merge((blue_channel, green_channel, red_channel))
    return filterd_img

@st.cache_data
def Cold_filter(img):
    # We are giving y values for a set of x values.
    # And calculating y for [0-255] x values accordingly to the given range.
    increase_table = UnivariateSpline(x=[0, 64, 128, 255], y=[0, 75, 155, 255])(range(256))
 
    # Similarly construct a lookuptable for decreasing pixel values.
    decrease_table = UnivariateSpline(x=[0, 64, 128, 255], y=[0, 45, 95, 255])(range(256))
    # Split the blue, green, and red channel of the image.
    blue_channel, green_channel, red_channel = cv2.split(img)
    
    # Decrease red channel intensity using the constructed lookuptable.
    red_channel = cv2.LUT(red_channel, decrease_table).astype(np.uint8)
    
    # Increase blue channel intensity using the constructed lookuptable.
    blue_channel = cv2.LUT(blue_channel, increase_table).astype(np.uint8)
    
    # Merge the blue, green, and red channel. 
    filterd_img = cv2.merge((blue_channel, green_channel, red_channel))
    
    return(filterd_img)