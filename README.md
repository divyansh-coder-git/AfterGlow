# AFTERGLOW ✨

### Every Image Has a Feeling.

AFTERGLOW is an AI-powered visual interpretation system that explores the emotional atmosphere an image may convey.

It combines pretrained multimodal image understanding with handcrafted computer-vision features and a custom mood-fusion mechanism. After analysing an image, AFTERGLOW presents a visual category, a dominant and secondary mood, an evidence-based explanation, and a mood-guided image transformation.

AFTERGLOW is not intended to determine the objectively correct emotion of an image. It offers an interpretable creative reading of its visual characteristics.

---

## Overview

Images communicate more than the objects they contain. Lighting, colour, contrast, saturation, tonal variation and composition all influence how a scene may be perceived.

A quiet mountain landscape may feel serene. A crowded city at dusk may feel dramatic or nostalgic. A vivid abstract painting may appear energetic.

AFTERGLOW explores these relationships through two complementary forms of analysis:

- **Semantic analysis:** a pretrained CLIP model compares an image with text descriptions of possible moods and visual categories.
- **Visual analysis:** a custom OpenCV pipeline measures image characteristics and converts them into handcrafted mood scores.

The two score sets are combined to produce a final ranking. The highest-ranked mood guides the image transformation, while the two highest-ranked moods are shown as the primary and secondary interpretations.

## Features

- **Image context classification:** identifies the broad visual category of an uploaded image, such as landscape, nature, portrait, architecture, abstract art or cityscape.
- **Visual feature extraction:** measures brightness, global contrast, saturation, warm-colour proportion, cool-colour proportion, edge density and local contrast.
- **Dominant-colour analysis:** uses K-Means clustering to extract a compact representation of the image's colour palette and the proportion of pixels assigned to each cluster.
- **Semantic mood analysis:** uses OpenCLIP to compare the image with descriptions of eight possible moods.
- **Custom mood fusion:** combines normalized CLIP similarity scores with handcrafted visual scores.
- **Primary and secondary moods:** displays the two highest-ranked emotional interpretations rather than forcing the interface to communicate only one possible mood.
- **Explainable interpretation:** generates a rule-based explanation connecting measurable visual characteristics to the selected primary mood.
- **Mood-guided transformation:** applies mood-specific brightness, contrast, saturation, colour-temperature and vignette adjustments.
- **Interactive comparison:** provides a draggable before-and-after slider.
- **Image export:** allows users to download the transformed image.

---

## How It Works

AFTERGLOW follows a hybrid image-analysis and transformation pipeline.

```text
                         IMAGE INPUT
                              |
                              v
                       Image Preprocessing
                              |
                              v
                      Context Classification
                         (OpenCLIP)
                              |
                    +---------+---------+
                    |                   |
                Expressive         Informational
                    |                   |
                    v                   v
             Visual Analysis       Stop Mood
                (OpenCV)            Processing
                    |
                    v
             Semantic Mood Analysis
                 (OpenCLIP)
                    |
                    v
                Mood Fusion
                    |
                    v
           Primary and Secondary Mood
                    |
             +------+------+
             |             |
             v             v
        Explanation   Transformation
          Engine         (OpenCV)
             |             |
             +------+------+
                    |
                    v
             Before / After
                Comparison
```

### 1. Image context classification

Before interpreting mood, AFTERGLOW uses CLIP to compare the uploaded image against descriptions of visual categories.

The current categories are:

- Landscape
- Nature
- Portrait
- Architecture
- Abstract art
- Cityscape
- Technical diagram
- Scientific diagram
- Document

Images classified as expressive visual content continue through mood analysis. Images classified as primarily informational or technical content are not forced into an emotional interpretation.

Image category and mood are separate predictions: a nature photograph, for example, can be serene, mysterious, melancholic, energetic or hopeful.

### 2. Visual feature extraction

OpenCV extracts measurable characteristics from the image:

| Feature | Description |
|---|---|
| Brightness | Mean grayscale intensity. |
| Global contrast | Standard deviation of grayscale intensity. |
| Saturation | Mean saturation channel value in HSV colour space. |
| Warm ratio | Proportion of pixels that fall within the selected warm-colour HSV masks. |
| Cool ratio | Proportion of pixels that fall within the selected cool-colour HSV mask. |
| Edge density | Proportion of pixels identified as edges by Canny edge detection. |
| Local contrast | Average grayscale standard deviation across regions of a 4 × 4 image grid. |
| Dominant colours | Five K-Means colour centres, ordered by cluster frequency. |
| Colour proportions | Fraction of sampled pixels assigned to each colour cluster. |

These measurements describe different aspects of an image. They are not direct measurements of emotion. Their relationship to mood is represented through handcrafted heuristic scoring rules.

### 3. Semantic mood analysis

AFTERGLOW uses OpenCLIP to compare an image embedding against text descriptions representing eight possible moods.

| Mood | Interpretation |
|---|---|
| Serene | Peaceful and calm |
| Melancholic | Lonely and sorrowful |
| Energetic | Vibrant and lively |
| Mysterious | Dark and enigmatic |
| Nostalgic | Dreamy and sentimental |
| Romantic | Warm and intimate |
| Dramatic | Intense and powerful |
| Hopeful | Optimistic and uplifting |

The model returns cosine-similarity scores between the image embedding and the mood text embeddings. These scores represent semantic similarity; they are not probabilities.

### 4. Custom mood fusion

AFTERGLOW does not rely entirely on CLIP. It combines semantic similarity scores with handcrafted visual scores.

The fusion equation is:

$$
F_m = \alpha C'_m + (1-\alpha)V_m
$$

Where:

- $ F_m $ is the final score for mood $ m $.
- $ C'_m $ is the normalized CLIP similarity score.
- $ V_m $ is the handcrafted visual score.
- $ \alpha $ controls the relative contribution of semantic analysis.

The current application uses an equal weighting of the two components ( $ \alpha $= 0.5 ).

CLIP similarities are normalized using fixed lower and upper percentile boundaries estimated from a small calibration set. Values outside those boundaries are clipped to the range 0–1. The boundaries are calibration parameters for the current model and prompt configuration; they are not universal constants and should be recalculated when the model, prompts or calibration data change.

The handcrafted visual scores use continuous feature-membership functions and mood-specific combinations of visual characteristics. Serenity uses Gaussian membership functions to avoid assigning the same full score to every image falling within a broad feature interval.

The final scores are used to rank possible moods. They are not calibrated probabilities or measures of certainty.

### 5. Primary and secondary moods

AFTERGLOW displays the two highest-ranked moods from the fused score ranking.

The **primary mood** guides the image transformation. The **secondary mood** provides an additional interpretation when an image may convey more than one emotional quality.

A small difference between the top two scores indicates that the system's ranking is close. Neither score should be interpreted as a probability.

### 6. Explainable interpretation

A rule-based explanation engine connects the selected primary mood to measurable image properties.

It evaluates extracted features against mood-specific expectations and produces a readable explanation describing supporting and contrasting visual evidence.

This makes the creative interpretation more transparent: the system can show which measurable characteristics contributed to its interpretation rather than presenting only a mood label.

### 7. Mood-guided transformation

After selecting the primary mood, AFTERGLOW applies a corresponding set of image-processing parameters using OpenCV.

The transformation operations include:

- Brightness and contrast adjustment.
- Saturation adjustment.
- Colour-temperature manipulation.
- Vignette application.

The current transformation pipeline uses conventional image processing rather than a generative image model. The purpose is to translate the system's mood interpretation into a visible change while retaining the underlying image.

### 8. Before-and-after comparison

The interface presents the original and transformed images in an interactive comparison slider. Users can drag the divider to reveal either version.

The comparison uses resized preview images for display, while the transformed full-resolution image remains available for download.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application and analysis logic |
| OpenCV | Image processing and visual feature extraction |
| NumPy | Numerical operations |
| PyTorch | Deep-learning inference |
| OpenCLIP | Semantic image and text embeddings |
| Pillow | Image loading, conversion and preview handling |
| Streamlit | Interactive application interface |
| HTML, CSS and JavaScript | Interactive before-and-after comparison |

### Model configuration

- **Architecture:** ViT-B-32
- **Pretrained checkpoint:** `laion2b_s34b_b79k`
- **Framework:** OpenCLIP with PyTorch
- **Fine-tuning:** No additional fine-tuning is performed.

The pretrained model supplies general image-text representations. The project's custom contribution is the surrounding context-classification, visual-feature extraction, mood-scoring, fusion, explanation and transformation pipeline.

---

## Getting Started

### Prerequisites

- Python 3.12 is recommended for the current project environment.
- `pip`
- An internet connection for downloading pretrained model weights during initial setup.

A dedicated GPU is not required. The application supports CPU inference. If a compatible CUDA-enabled PyTorch installation is available, the CLIP model can use a supported NVIDIA GPU.

### 1. Clone the repository

```bash
git clone https://github.com/divyansh-coder-git/AfterGlow.git
cd AfterGlow
```

### 2. Create and activate a virtual environment

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the application

```bash
python -m streamlit run app.py
```

Streamlit will print a local URL in the terminal. Open that URL in a browser to use AFTERGLOW.

### Supported image formats

The uploader currently accepts:

- JPG / JPEG
- PNG
- WEBP

---

## Project Structure

```text
AFTERGLOW/
│
├── app.py                 # Streamlit interface and application orchestration
├── clip_analyzer.py       # CLIP model, context classification and mood analysis
├── vision_features.py     # OpenCV visual feature extraction and K-Means colours
├── mood_fusion.py         # Continuous visual scoring, CLIP normalization and fusion
├── explanation.py         # Rule-based explanation and evidence engine
├── transformer.py         # Mood-guided image transformations
├── comparison.py          # Interactive before-and-after slider
│
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
└── .gitignore             # Files excluded from version control
```

---

## Design Philosophy

AFTERGLOW is built around three principles.

### 1. Hybrid intelligence

Combine pretrained multimodal models with traditional computer vision rather than depending entirely on a single model.

### 2. Explainable creativity

Connect visual analysis to creative decisions so that the resulting interpretation is more transparent and understandable.

### 3. Technology as expression

The objective is not simply to modify an image. It is to explore how computational systems can interpret visual information and express that interpretation through artistic transformations.

---

## Limitations

- **Subjectivity:** Emotional interpretation is subjective. Different people may perceive the same image differently. AFTERGLOW presents possible interpretations, not definitive emotional classifications.
- **CLIP limitations:** CLIP similarity scores are not calibrated probabilities. Results depend on the model, text descriptions and candidate mood set.
- **Heuristic visual scoring:** The handcrafted scoring system uses manually designed rules and parameters. It can misinterpret images whose emotional character is not adequately represented by the extracted global features.
- **Calibration data:** The current numerical calibration was explored using a small image set. It is not a statistically representative human-perception benchmark.
- **Context classification:** The system uses a finite set of predefined image categories. Images that do not fit these categories may be assigned an imperfect category.
- **Non-generative transformations:** The current transformation pipeline uses conventional image-processing operations rather than a generative image model. It changes visual characteristics but does not create new scene content.
- **Informational content:** Images classified as primarily technical or informational are intentionally excluded from ordinary mood-guided transformations.

---

## Future Directions

Potential directions for further development include:

- Build a larger human-labelled dataset to evaluate mood interpretations.
- Improve visual features to capture spatial colour relationships and composition.
- Evaluate mood-fusion parameters on images not used during calibration.
- Improve category coverage and context classification.
- Explore more nuanced, category-aware mood descriptions.
- Investigate generative transformations while retaining transparent control over the visual changes.
- Improve runtime performance and deployment reliability.

---

## Acknowledgements

**AFTERGLOW was developed for **Data Strata — CODE THE CANVAS**.**

The project explores the intersection of computer vision, multimodal AI and creative expression.

*The semantic image understanding component uses the pretrained OpenCLIP model and its associated LAION checkpoint. Please refer to the model and dataset documentation for the applicable licences and usage terms.*

---

**_Build with 🫀 by Divyansh Pandey_**<br />
*Special thanks to ChatGPT for being my debugging partner throughout the project, also for the english used in this code and this README too 🤖*
