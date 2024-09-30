import streamlit as st
import streamlit.components.v1 as components
import  base64
from pathlib import Path



def img_to_bytes(img_path):
    img_bytes = Path(img_path).read_bytes()
    encoded = base64.b64encode(img_bytes).decode()
    return encoded

files = ['bw.png', 'sepia.png', 'vignette.png', 'pencil_sketch.png', 'edge_detection.png', 'embrossed_edges.png','blur.png', 'outline.png', 'sharpening.png' ,'hdr.png', 'warm.png', 'cold.png']

filesname = ["Black and White", "Sepia / Vintage", "Vignette Effect", "Pencil Sketch", "Canny Edge Detection", "Embossed Edges", "Blur Image", "Outline", "Sharpening Filter", "HDR Effect", "Warm Effect", "Cold Effect"]


image_html = ""
for file, filename in zip(files, filesname):
    image_html += f"""
    <div  class="slide">
      <p>{filename}</p>  
      <img src='data:image/png;base64,{img_to_bytes(f"./static/{file}")}' class='img-fluid'>
    </div>
    """




def html_content():
    html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Responsive Image Slider</title>
  <style>
    * {{
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }}
    
    body {{
        font-family: Arial, sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-color: transparent;
    }}
    
    .slider {{
        width: 100%;
        max-width: 1000px;
        position: relative;
        overflow: hidden;
    }}
    
    .slides {{
        display: flex;
        transition: transform 0.5s ease-in-out;
    }}
    
    .slide {{
    min-width: 20%; /* Show 4 images at a time on larger screens */
    display: flex;
    flex-direction: column;
  }}
  
  .slide img {{
    width: 100%;
    max-width: 180px;
    height: auto;
    display: block;
    margin-top:0.7rem;
  }}
  .slide p {{
    font-size: 1.1rem;
    background: linear-gradient(45deg, #2b113a, #e41de4);
    background-clip: text;
    -webkit-background-clip: text;
    color: transparent;
    font-weight: 700;
}}
    
    .navigation {{
        position: absolute;
        top: 50%;
        width: 100%;
        display: flex;
        justify-content: space-between;
        transform: translateY(-50%);
    }}
    
    .navigation button {{
        background-color: rgba(0, 0, 0, 0.5);
        border: none;
        padding: 10px;
        color: white;
        font-size: 18px;
        cursor: pointer;
    }}
    
    .navigation button:hover {{
        background-color: rgba(0, 0, 0, 0.8);
    }}
    
    /* Responsive design */
    /* Display 3 images on medium screens */
    @media screen and (max-width: 768px) {{
        .slide {{
            min-width: 28.5%;
        }}
    
        .slides {{
            gap: 5px;
        }}
    }}
    
    /* Display 2 images on smaller screens */
    @media screen and (max-width: 500px) {{
        .slide {{
            min-width: 30%;
        }}
    
   # Render the HTML content
components.html(html_content, height=200)     .slides {{
            gap: 10px;
        }}
    }}
    
    /* Display 1 image on very small screens */
    @media screen and (max-width: 320px) {{
        .slide {{
            min-width: 26%;
        }}
    
        .slides {{
            gap: 5px;
        }}
    }}
  </style>
</head>
<body>

<div class="slider">
  <div class="slides">
    <div class="slides">
    {image_html} 
  </div>
  </div>

  <!-- Buttons for manual control -->
  <div class="navigation">
    <button class="prev">❮</button>
    <button class="next">❯</button>
  </div>
</div>


<script>
const slides = document.querySelector('.slides');
const slideCount = document.querySelectorAll('.slide').length;
let currentIndex = 0;
let autoSlideInterval;

const nextButton = document.querySelector('.next');
const prevButton = document.querySelector('.prev');

// Function to show slides
function showSlides(index) {{
  const slideWidth = document.querySelector('.slide').clientWidth;
  slides.style.transform = `translateX(-${{(slideWidth + parseInt(getComputedStyle(slides).gap)) * index}}px)`;
  currentIndex = index;
}}

// Function to go to the next slide
function nextSlide() {{
  if (currentIndex < slideCount - getVisibleSlides()) {{
    showSlides(currentIndex + 1);
  }} else {{
    showSlides(0); // Go back to the first slide
  }}
}}

// Function to go to the previous slide
function prevSlide() {{
  if (currentIndex > 0) {{
    showSlides(currentIndex - 1);
  }} else {{
    showSlides(slideCount - getVisibleSlides()); // Go to the last set of slides
  }}
}}

// Function to get the number of visible slides based on screen width
function getVisibleSlides() {{
  const width = window.innerWidth;

  if (width <= 320) {{
    return 1; // 1 slide for very small screens
  }} else if (width <= 500) {{
    return 2; // 2 slides for small screens
  }} else if (width <= 768) {{
    return 3; // 3 slides for medium screens
  }} else {{
    return 4; // 4 slides for larger screens
  }}
}}

// Manual Controls
nextButton.addEventListener('click', nextSlide);
prevButton.addEventListener('click', prevSlide);


// Touch support for swiping
let startX = 0;
let endX = 0;

slides.addEventListener('touchstart', (e) => {{
  startX = e.touches[0].clientX;
}});

slides.addEventListener('touchmove', (e) => {{
  endX = e.touches[0].clientX;
}});

slides.addEventListener('touchend', () => {{
  if (startX - endX > 50) {{
    nextSlide(); // Swipe left
  }} else if (endX - startX > 50) {{
    prevSlide(); // Swipe right
  }}
}});

// Stop the auto-slide when hovering over the slider
document.querySelector('.slider').addEventListener('mouseenter', stopAutoSlide);
document.querySelector('.slider').addEventListener('mouseleave', startAutoSlide);

// Adjust the current slide when the window resizes
window.addEventListener('resize', () => showSlides(currentIndex));
</script>

</body>
</html>
"""
    return html


