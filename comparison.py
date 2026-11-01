from PIL import Image
import base64
from io import BytesIO
import streamlit as st

def image_to_base64(image):
    buffer = BytesIO()
    image.save(buffer, format="JPEG", quality=82, optimize=False)

    encoded = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return f"data:image/jpeg;base64,{encoded}"

def render_comparison(original, transformed):

    original_src = image_to_base64(original)
    transformed_src = image_to_base64(transformed)
    html = f"""
    <style>
        html, body {{
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            width: 100%;
        }}

        body {{
            overflow-y: hidden !important;
        }}

        .comparison-container {{
            position: relative;
            width: 100%;
            aspect-ratio: 16 / 9;
            overflow: hidden;
            border-radius: 14px;
            cursor: ew-resize;
            user-select: none;
        }}

        .comparison-image {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            display: block;
        }}

        .comparison-overlay {{
            position: absolute;
            inset: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            clip-path: inset(0 50% 0 0);
        }}

        .comparison-overlay img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}

        .comparison-slider {{
            position: absolute;
            left: 50%;
            top: 0;
            bottom: 0;
            width: 3px;
            background: white;
            transform: translateX(-50%);
        }}

        .slider-handle {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            width: 42px;
            height: 42px;
            border-radius: 50%;
            background: white;
            color: #333;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 22px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        }}
    </style>

    <div class="comparison-container" id="comparison">

        <img src="{original_src}" class="comparison-image">

        <div class="comparison-overlay" id="overlay">
            <img src="{transformed_src}" class="comparison-image">
        </div>

        <div class="comparison-slider" id="slider">
            <div class="slider-handle">↔</div>
        </div>

    </div>

    <script>
        const container = document.getElementById("comparison");
        const overlay = document.getElementById("overlay");
        const slider = document.getElementById("slider");

        let dragging = false;

        function updateSlider(event) {{

            const rect = container.getBoundingClientRect();

            let position = (event.clientX - rect.left) / rect.width;

            position = Math.max(0, Math.min(1, position));

            const percentage = position * 100;

            overlay.style.clipPath = `inset(0 ${{100 - percentage}}% 0 0)`;
            slider.style.left = percentage + "%";
        }}

        container.addEventListener("pointerdown", (event) => {{
            dragging = true;
            container.setPointerCapture(event.pointerId);
            updateSlider(event);
        }});

        container.addEventListener("pointermove", (event) => {{
            if (dragging) {{
                updateSlider(event);
            }}
        }});

        container.addEventListener("pointerup", () => {{
            dragging = false;
        }});

        container.addEventListener("pointercancel", () => {{
            dragging = false;
        }});
    </script>
    """

    return html

def display_comparison(html):
    st.iframe(html, height='content')
