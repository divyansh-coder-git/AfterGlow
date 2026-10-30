import streamlit as st
import streamlit.components.v1 as components
import textwrap
import cv2
import numpy as np
import io
import hashlib
from explanation import generate_final_explanation
from PIL import Image
from comparison import render_comparison

from vision_features import extract_features
from clip_analyzer import analyze_mood, classify_image, encode_image
from mood_fusion import (
    calculate_visual_scores,
    fuse_mood_scores
)
from transformer import transform_image


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="AFTERGLOW — Visual Mood Studio",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =====================================================
# CACHED IMAGE LOADING
# =====================================================

@st.cache_data
def load_image(image_bytes):

    image = Image.open(
        io.BytesIO(image_bytes)
    ).convert("RGB")

    image_array = np.array(image)

    image_bgr = cv2.cvtColor(
        image_array,
        cv2.COLOR_RGB2BGR
    )

    return image_array, image_bgr


# =====================================================
# CUSTOM CSS
# =====================================================

st.html("""
<style>

.stApp {
    background: #080D18;
    color: #F8FAFC;
}

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

.block-container {
    max-width: 1150px;
    padding-top: 3rem;
    padding-bottom: 4rem;
}

.hero {
    text-align: center;
    padding: 65px 0 45px 0;
}

.hero h1 {
    font-size: 64px;
    font-weight: 800;
    letter-spacing: 12px;
    margin-bottom: 10px;
    color: #F8FAFC;
}

.hero p {
    color: #94A3B8;
    font-size: 14px;
    letter-spacing: 5px;
    margin-top: 0;
}

.accent-line {
    width: 65px;
    height: 3px;
    background: linear-gradient(
        90deg,
        #A78BFA,
        #67E8F9
    );
    margin: 25px auto;
    border-radius: 10px;
}

.section-title {
    font-size: 23px;
    font-weight: 650;
    color: #F1F5F9;
    margin-bottom: 8px;
}

.section-subtitle {
    color: #94A3B8;
    font-size: 14px;
    margin-bottom: 25px;
}

[data-testid="stFileUploader"] {
    background: #111827;
    border: 1px solid #293449;
    border-radius: 16px;
    padding: 20px;
}

.stButton button {
    background: linear-gradient(
        110deg,
        #8B5CF6,
        #6366F1
    );
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 25px;
    font-weight: 600;
}

.stButton button:hover {
    border: 1px solid #A78BFA;
    color: white;
}

[data-testid="stImage"] img {
    border-radius: 14px;
    border: 1px solid #293449;
}

hr {
    border-color: #293449;
    margin: 40px 0;
}

</style>
""")


# =====================================================
# HERO SECTION
# =====================================================

hero_html = textwrap.dedent("""
    <div class="hero">
        <h1>AFTERGLOW</h1>
        <p>EVERY IMAGE HAS A FEELING</p>
        <div class="accent-line"></div>
    </div>
""")

st.markdown(hero_html, unsafe_allow_html=True)


# =====================================================
# IMAGE UPLOAD
# =====================================================

st.markdown(
    '<div class="section-title">Explore the unseen.</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Upload a photograph. Discover the emotions hidden within it.'
    '</div>',
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Choose your photograph",
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="collapsed"
)


# =====================================================
# IMAGE PREVIEW
# =====================================================

if uploaded_file is not None:

    image_bytes = uploaded_file.getvalue()

    # Identify the uploaded image
    image_key = hashlib.sha256(image_bytes).hexdigest()

    # Clear previous results when a new image is uploaded
    if st.session_state.get("image_key") != image_key:

        st.session_state["image_key"] = image_key
        st.session_state.pop("result", None)
        st.session_state.pop("original", None)

    image_array, image_bgr = load_image(image_bytes)

    image = Image.fromarray(image_array)

    st.markdown("---")

    st.markdown(
        '<div class="section-title">Your canvas</div>',
        unsafe_allow_html=True
    )

    st.image(
        image,
        use_container_width=True
    )

    st.markdown("")

    # =================================================
    # ANALYSIS BUTTON
    # =================================================

    analyse = st.button(
        "✦  Discover the mood",
        use_container_width=True
    )

    if analyse:

        progress = st.progress(0)
        status = st.empty()

        try:

            # -----------------------------------------
            # STAGE 1: IMAGE PREPARATION
            # -----------------------------------------

            status.markdown("🔍 Preparing your image...")

            image_array = np.array(image)

            image_bgr = cv2.cvtColor(
                image_array,
                cv2.COLOR_RGB2BGR
            )

            progress.progress(10)


            # -----------------------------------------
            # STAGE 2: CONTEXT CLASSIFICATION
            # -----------------------------------------

            status.markdown(
                "🧠 Understanding what your image represents..."
            )

            context = classify_image(image_bgr)

            image_features = encode_image(image_bgr)

            progress.progress(30)


            # -----------------------------------------
            # STAGE 3: CONDITIONAL MOOD ANALYSIS
            # -----------------------------------------

            if context["is_expressive"]:

                status.markdown(
                    "🎨 Interpreting its emotional atmosphere..."
                )

                features = extract_features(image_bgr)

                progress.progress(50)

                clip_scores = analyze_mood(
                    image_bgr,
                    image_features
                )

                progress.progress(70)

                visual_scores = calculate_visual_scores(
                    features
                )

                final_scores = fuse_mood_scores(
                    clip_scores,
                    visual_scores
                )

                dominant_mood = next(iter(final_scores))

                explanation = generate_final_explanation(dominant_mood, features)
                
                status.markdown(
                    "✨ Creating your artistic transformation..."
                )

                transformed_image = transform_image(
                    image_bgr,
                    dominant_mood
                )

                progress.progress(100)

                result = {
                    "context": context,
                    "features": features,
                    "clip_scores": clip_scores,
                    "visual_scores": visual_scores,
                    "final_scores": final_scores,
                    "dominant_mood": dominant_mood,
                    "transformed_image": transformed_image,
                    "is_expressive": True,
                    "explanation": explanation
                }

            else:

                progress.progress(100)

                result = {
                    "context": context,
                    "is_expressive": False
                }
                

            st.session_state["result"] = result
            st.session_state["original"] = image

            status.success("Your image has been interpreted!")

        except Exception as e:

            status.error(f"Something went wrong: {e}")


# =====================================================
# DISPLAY RESULTS
# =====================================================

if "result" in st.session_state:

    result = st.session_state["result"]
    context = result["context"]

    st.markdown("---")

    st.markdown("## What are we looking at?")

    st.markdown(
        f"""
        **Detected category:** {context['category'].replace('_', ' ').title()}
        """
    )

    st.caption(
        f"Category similarity: {context['top_score']:.3f} "
        f"| Margin over second category: {context['margin']:.3f}"
    )

    with st.expander("Explore category analysis"):

        for category, score in context["scores"].items():

            st.write(
                f"**{category.replace('_', ' ').title()}**: {score:.3f}"
            )

    if not result["is_expressive"]:

        st.info(
            "This image appears to contain primarily technical "
            "or informational content. A conventional emotional "
            "interpretation may not be meaningful."
        )

        st.markdown(
            "### Why we stopped here"
        )

        st.write(
            "AFTERGLOW first examines the visual context of an image. "
            "It avoids forcing an emotional interpretation when the "
            "image is classified as technical or document-like."
        )

    else:

        # KEEP YOUR EXISTING MOOD INTERPRETATION,
        # MOOD SPECTRUM, TRANSFORMATION AND DOWNLOAD
        # SECTIONS INSIDE THIS ELSE BLOCK.

        dominant_mood = result["dominant_mood"]
        final_scores = result["final_scores"]

        # Anchor for automatic scrolling

        st.markdown(
            '<div id="afterglow-results"></div>',
            unsafe_allow_html=True
        )

        # =================================================
        # MOOD DISCOVERY
        # =================================================

        st.markdown("---")

        st.markdown(
            '<div class="section-title">'
            'The emotional interpretation'
            '</div>',
            unsafe_allow_html=True
        )

        mood_card = f"""
        <div style="
            background: linear-gradient(120deg, #17152B, #111827);
            border: 1px solid #6D5BA6;
            border-radius: 18px;
            padding: 30px;
            margin: 20px 0;
        ">
            <p style="color: #A78BFA; letter-spacing: 3px;">
                PRIMARY INTERPRETATION
            </p>

            <h1 style="
                font-size: 42px;
                text-transform: capitalize;
                margin: 0;
            ">
                {dominant_mood}
            </h1>

            <p style="color: #94A3B8;">
                The dominant emotional atmosphere interpreted from your image.
            </p>
        </div>
        """

        st.html(mood_card)

        st.markdown("### ✨ Why this mood?")
        st.write(result["explanation"]["text"])
    
        # =================================================
        # MOOD SPECTRUM
        # =================================================

        st.markdown("### The mood spectrum")

        st.caption(
            "Relative fusion scores from our visual and "
            "semantic analysis. These are not probabilities."
        )

        for mood, score in final_scores.items():

            st.markdown(
                f"**{mood.capitalize()}**"
            )

            st.progress(
                float(np.clip(score, 0, 1)),
                text=f"{score:.3f}"
            )

        # =================================================
        # ARTISTIC TRANSFORMATION
        # =================================================

        st.markdown("---")

        st.markdown(
            "## The transformation"
        )

        st.caption(
            "See how AFTERGLOW translates its emotional interpretation "
            "into a visual experience."
        )

        original_image = st.session_state["original"]

        transformed_bgr = result["transformed_image"]

        transformed_rgb = cv2.cvtColor(
            transformed_bgr,
            cv2.COLOR_BGR2RGB
        )

        transformed_pil = Image.fromarray(transformed_rgb)
        # print("Original:", type(original_image))
        # print("Transformed:", type(transformed_pil))
        render_comparison(original_image, transformed_pil)

        st.markdown("### Experience the transformation")
        

        # col1, col2 = st.columns(2)

        # with col1:

        #     st.markdown("### Original")

        #     st.image(
        #         original_image,
        #         use_container_width=True
        #     )

        # with col2:

        #     st.markdown(
        #         f"### AFTERGLOW · {dominant_mood.capitalize()}"
        #     )

        #     st.image(
        #         transformed_pil,
        #         use_container_width=True
        #     )



        # =================================================
        # DOWNLOAD TRANSFORMATION
        # =================================================

        success, encoded_image = cv2.imencode(
            ".png",
            transformed_bgr
        )

        if success:
            st.download_button(
                label="↓  Download your AFTERGLOW image",
                data=encoded_image.tobytes(),
                file_name=f"afterglow_{dominant_mood}.png",
                mime="image/png",
                use_container_width=True
            )

        # =================================================
        # VISUAL FINGERPRINT
        # =================================================

        st.markdown("---")

        st.markdown("## Visual fingerprint")

        st.caption(
            "The visual characteristics extracted from your photograph."
        )

        features = result["features"]

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Brightness",
                f"{features['brightness']:.1f}/255"
            )

        with col2:

            st.metric(
                "Contrast",
                f"{features['contrast']:.1f}"
            )

        with col3:

            st.metric(
                "Saturation",
                f"{features['saturation']:.1f}/255"
            )

        st.markdown("### Dominant colour palette")

        dominant_colors = features["dominant_colors"]

        color_columns = st.columns(len(dominant_colors))

        for index, color in enumerate(dominant_colors):

            # OpenCV stores colours in BGR
            blue, green, red = color

            hex_color = "#{:02x}{:02x}{:02x}".format(
                red,
                green,
                blue
            )

            with color_columns[index]:

                st.markdown(
                    f"""
                    <div style="
                        height: 65px;
                        background-color: {hex_color};
                        border-radius: 10px;
                        border: 1px solid #293449;
                    "></div>
                    <p style="
                        text-align: center;
                        color: #94A3B8;
                        font-size: 12px;
                    ">
                        {hex_color.upper()}
                    </p>
                    """,
                    unsafe_allow_html=True
                )
        # =================================================
        # AUTOMATIC SCROLL
        # =================================================

        components.html(
            """
            <script>

                const parentDoc = window.parent.document;

                const target = parentDoc.getElementById(
                    "afterglow-results"
                );

                if (target) {

                    target.scrollIntoView({
                        behavior: "smooth",
                        block: "start"
                    });

                }

            </script>
            """,
            height=0
        )
