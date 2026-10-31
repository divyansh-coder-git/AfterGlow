# AFTERGLOW ✨

### Every Image Has a Feeling.

**AFTERGLOW** is an AI-powered visual interpretation system that explores the emotional character hidden within images.

By combining traditional computer vision, multimodal semantic understanding and custom mood-fusion algorithms, AFTERGLOW analyses an image, interprets its possible mood and translates that interpretation into a corresponding visual experience.

It doesn't just apply filters. It attempts to understand the visual characteristics behind an image and use them to guide its transformation.

---

## The Idea

Images communicate more than their subjects.

Lighting, colour temperature, contrast, saturation and visual composition all contribute to how an image is perceived.

A sunset over a city might feel nostalgic. A dimly lit street might appear mysterious. A vibrant landscape might communicate energy and optimism.

AFTERGLOW explores this relationship between visual characteristics and emotional interpretation.

The system combines semantic understanding with measurable visual properties to create a mood-guided transformation.

---

## Features

* **Visual Feature Extraction:** Analyses brightness, contrast, saturation, warm colour distribution and dominant colours using OpenCV.
* **Semantic Mood Interpretation:** Uses CLIP to estimate the possible emotional character of an image.
* **Image Context Classification:** Distinguishes expressive visual content from informational and technical images.
* **Custom Mood Fusion:** Combines semantic similarity scores with handcrafted visual analysis.
* **Mood-Guided Transformation:** Applies image-processing operations based on the interpreted mood.
* **Explainable Interpretation:** Generates rule-based explanations connecting visual characteristics to the selected mood.
* **Interactive Before/After Comparison:** Drag a slider to explore the original and transformed images.

---

## How It Works

AFTERGLOW follows a hybrid computer-vision pipeline.

```text
                 IMAGE INPUT
                      |
                      v
              Image Preprocessing
                      |
                      v
             Image Context Analysis
                      |
              +-------+-------+
              |               |
          Expressive       Informational
              |               |
              v               v
       Visual Analysis      Stop Mood
         (OpenCV)           Processing
              |
              v
       Semantic Analysis
            (CLIP)
              |
              v
         Mood Fusion
              |
              v
       Dominant Mood Selection
              |
        +-----+------+
        |            |
        v            v
   Explanation    Visual
     Engine     Transformation
        |            |
        +-----+------+
              |
              v
       BEFORE / AFTER
         COMPARISON
```

### 1. Visual Feature Extraction

OpenCV extracts measurable visual characteristics:

* Brightness: Average grayscale intensity.
* Contrast: Standard deviation of grayscale intensity.
* Saturation: Average HSV saturation.
* Warm Ratio: Proportion of pixels classified as warm using HSV colour ranges.
* Dominant Colours: K-Means clustering to identify the image's dominant colour palette.

These features form the image's visual fingerprint.

### 2. Semantic Mood Analysis

AFTERGLOW uses OpenCLIP to compare an image embedding against text descriptions representing eight possible moods:

| Mood        | Interpretation           |
| ----------- | ------------------------ |
| Serene      | Peaceful and calm        |
| Melancholic | Lonely and sorrowful     |
| Energetic   | Vibrant and lively       |
| Mysterious  | Dark and enigmatic       |
| Nostalgic   | Dreamy and sentimental   |
| Romantic    | Warm and intimate        |
| Dramatic    | Intense and powerful     |
| Hopeful     | Optimistic and uplifting |

The resulting similarity scores indicate how closely the image aligns with each mood description.

### 3. Custom Mood Fusion

Instead of relying entirely on CLIP, AFTERGLOW combines semantic similarity with handcrafted visual scores.

The fusion mechanism is:

$$
F_m = \alpha C'_m + (1-\alpha)V_m
$$

Where:

* \(F_m\): Final score for mood \(m\).
* \(C'_m\): Normalized CLIP similarity score.
* \(V_m\): Handcrafted visual score.
* \(\alpha\): Weight controlling the contribution of semantic analysis.

This allows both semantic information and measurable visual characteristics to influence the final interpretation.

### 4. Mood-Guided Transformation

Once a dominant mood is selected, AFTERGLOW applies corresponding image-processing parameters.

The transformations include:

* Brightness adjustment.
* Contrast modification.
* Saturation adjustment.
* Colour temperature manipulation.
* Vignette effects.

These operations are implemented using OpenCV.

### 5. Explainable Creativity

AFTERGLOW also generates a rule-based explanation describing why an image received a particular mood interpretation.

It uses extracted visual features, mood-specific expectations and weighted evidence rules to produce an explanation.

The purpose is to connect the system's technical analysis with its creative output.

---

## Technology Stack

| Technology            | Purpose                                        |
| --------------------- | ---------------------------------------------- |
| Python                | Core development                               |
| OpenCV                | Image processing and visual feature extraction |
| NumPy                 | Numerical operations                           |
| PyTorch               | Deep learning inference                        |
| OpenCLIP              | Semantic image understanding                   |
| Pillow                | Image handling and conversion                  |
| Streamlit             | Interactive application interface              |
| HTML, CSS, JavaScript | Interactive comparison component               |

### Model

* Architecture: ViT-B-32
* Pretrained checkpoint: `laion2b_s34b_b79k`
* Framework: OpenCLIP / PyTorch

The project uses a pretrained model without additional fine-tuning. Its original contribution lies in the custom analysis, fusion, interpretation and transformation pipeline.

---

## Getting Started

### Prerequisites

* Python 3.12 (recommended for the current development environment).
* pip.
* An internet connection for downloading the pretrained model weights during initial setup.

A dedicated GPU is not required. CPU inference is supported, although performance will vary depending on hardware.

### 1. Clone the repository

```bash
git clone https://github.com/divyansh-coder-git/AfterGlow.git

cd AFTERGLOW
```

### 2. Create a virtual environment

**Windows:**

```bash
python -m venv .venv

.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

Open the local URL displayed in your terminal to access AFTERGLOW.

---

## Project Structure

```text
AFTERGLOW/
│
├── app.py                 # Streamlit application
├── vision_features.py     # OpenCV visual feature extraction
├── clip_analyzer.py       # CLIP-based image and mood analysis
├── mood_fusion.py         # Custom mood fusion logic
├── transformer.py         # Mood-guided image transformations
├── explanation.py         # Rule-based explanation engine
├── comparison.py          # Interactive before/after comparison
│
├── requirements.txt       # Project dependencies
├── README.md
│
└── .venv/                 # Virtual environment (not committed)
```

---

## Design Philosophy

AFTERGLOW is built around three principles:

**1. Hybrid Intelligence**

Combine pretrained multimodal models with traditional computer vision instead of depending entirely on a single model.

**2. Explainable Creativity**

Connect the system's visual analysis to its creative decisions, making the transformation more interpretable.

**3. Technology as Expression**

The objective isn't simply to modify an image. It's to explore how computational systems can interpret visual information and express it through artistic transformations.

---

## Future Roadmap

* [ ] Improve visual feature analysis and mood interpretation.
* [ ] Expand and validate mood-fusion strategies.
* [ ] Improve explanation quality and evidence selection.
* [ ] Add image download and export functionality.
* [ ] Improve interface responsiveness and visual polish.
* [ ] Optimize inference and image-processing performance.
* [ ] Expand testing across different image categories.
* [ ] Explore advanced generative image transformations.

---

## Limitations

* Emotional interpretation is subjective. AFTERGLOW presents possible moods rather than definitive emotional classifications.
* CLIP similarity scores are not calibrated probabilities.
* Mood fusion and visual interpretation rely partly on handcrafted heuristics.
* The current transformation pipeline uses conventional image-processing operations rather than a generative image model.
* Informational and technical images are intentionally excluded from mood-guided transformations.

---

AFTERGLOW was developed as a creative AI project for **Data Strata — CODE THE CANVAS**.

The project explores the intersection of computer vision, multimodal AI and creative expression.

---

*Build with 🫀 by Divyansh Pandey*<br />
*Special thanks to ChatGPT for being my debugging partner throughout the project, also for the english used in this code and this README too 🤖*
