# import torch
# import open_clip
# import cv2
# import numpy as np
# from PIL import Image

# MOODS = {
#     "serene": "A peaceful, calm and serene landscape",
#     "melancholic": "A melancholic, lonely and sorrowful scene",
#     "energetic": "A vibrant, lively and energetic scene",
#     "mysterious": "A mysterious, dark and enigmatic scene",
#     "nostalgic": "A nostalgic, dreamy and sentimental scene",
#     "romantic": "A romantic, warm and beautiful scene",
#     "dramatic": "A dramatic, intense and powerful scene",
#     "hopeful": "An uplifting, optimistic and hopeful scene"
# }

# device = "cpu"
# model, _, preprocess = open_clip.create_model_and_transforms(
#     "ViT-B-32",
#     pretrained="laion2b_s34b_b79k",
#     device=device
# )
# tokenizer = open_clip.get_tokenizer("ViT-B-32")
# model.eval()

# mood_texts = list(MOODS.values())
# text_tokens = tokenizer(mood_texts)

# with torch.no_grad():
#     text_features = model.encode_text(text_tokens)
#     text_features /= text_features.norm(
#         dim=-1,
#         keepdim=True
#     )

# print("CLIP model loaded successfully!")
# print("Number of mood descriptions:", len(mood_texts))
# print("Text embedding shape:", text_features.shape)

# def analyze_mood(image):
#     # 1. Convert OpenCV BGR image to RGB
#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

#     # 2. Convert NumPy array to PIL Image
#     pil_image = Image.fromarray(image_rgb)

#     # 3. Apply CLIP preprocessing
#     image_input = preprocess(pil_image).unsqueeze(0)

#     # 4. Encode the image
#     with torch.no_grad():
#         image_features = model.encode_image(image_input)

#         # Normalize image embedding
#         image_features /= image_features.norm(
#             dim=-1,
#             keepdim=True
#         )

#         # 5. Calculate similarity with mood descriptions
#         similarities = (image_features @ text_features.T).squeeze(0)

#     # 6. Convert results into a dictionary
#     mood_scores = {
#         mood: float(score)
#         for mood, score in zip(MOODS.keys(), similarities)
#     }

#     # 7. Sort moods from highest similarity to lowest
#     mood_scores = dict(
#         sorted(
#             mood_scores.items(),
#             key=lambda item: item[1],
#             reverse=True
#         )
#     )

#     return mood_scores

import torch
import open_clip
import cv2
import numpy as np
from PIL import Image

# =====================================================
# 1. MOOD DESCRIPTIONS
# =====================================================

MOODS = {
    "serene": "A peaceful, calm and serene scene",
    "melancholic": "A melancholic, lonely and sorrowful scene",
    "energetic": "A vibrant, lively and energetic scene",
    "mysterious": "A mysterious, dark and enigmatic scene",
    "nostalgic": "A nostalgic, dreamy and sentimental scene",
    "romantic": "A romantic, warm and beautiful scene",
    "dramatic": "A dramatic, intense and powerful scene",
    "hopeful": "An uplifting, optimistic and hopeful scene"
}


# =====================================================
# 2. IMAGE CATEGORY DESCRIPTIONS
# =====================================================

IMAGE_CATEGORIES = {

    "landscape":
        "A photograph of a natural outdoor landscape, "
        "such as mountains, forests, oceans or valleys.",

    "portrait":
        "A photograph focusing on a person, human face "
        "or human expression.",

    "architecture":
        "A photograph of buildings, architectural structures, "
        "interior spaces or designed environments.",

    "abstract_art":
        "An abstract artwork expressing ideas through colours, "
        "shapes, patterns and textures.",

    "technical_diagram":
        "An engineering schematic showing electrical circuits, "
        "components, symbols, measurements or technical connections.",

    "scientific_diagram":
        "A scientific or educational illustration explaining "
        "a scientific concept, process or structure.",

    "document":
        "A photograph or scan of a document, written notes, "
        "printed text or a page of a book.",

    "cityscape":
        "A photograph of an urban city environment, including "
        "streets, skyscrapers, buildings, traffic and city lights."
}

# Categories suitable for our ordinary mood interpretation

EXPRESSIVE_CATEGORIES = {
    "landscape",
    "portrait",
    "architecture",
    "abstract_art",
    "cityscape"
}

# =====================================================
# 3. LOAD CLIP MODEL
# =====================================================

device = "cpu"
model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="laion2b_s34b_b79k",
    device=device
)
tokenizer = open_clip.get_tokenizer("ViT-B-32")
model.eval()


# =====================================================
# 4. PRECOMPUTE TEXT EMBEDDINGS
# =====================================================

# Mood embeddings
mood_names = list(MOODS.keys())
mood_texts = list(MOODS.values())
mood_tokens = tokenizer(mood_texts).to(device)


# Category embeddings
category_names = list(IMAGE_CATEGORIES.keys())
category_texts = list(IMAGE_CATEGORIES.values())
category_tokens = tokenizer(category_texts).to(device)


with torch.inference_mode():
    mood_text_features = model.encode_text(mood_tokens) # type: ignore
    category_text_features = model.encode_text(category_tokens) # type: ignore

    # Normalize embeddings
    mood_text_features /= mood_text_features.norm(
        dim=-1,
        keepdim=True
    )

    category_text_features /= category_text_features.norm(
        dim=-1,
        keepdim=True
    )


print("CLIP model loaded successfully!")
print("Number of moods:", len(mood_names))
print("Number of image categories:", len(category_names))


# =====================================================
# 5. ENCODE AN IMAGE
# =====================================================

def encode_image(image):
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2RGB
    )

    # Convert NumPy array to PIL
    pil_image = Image.fromarray(image_rgb)

    # Apply CLIP preprocessing
    image_input = preprocess(pil_image).unsqueeze(0).to(device) # type: ignore

    # Generate image embedding
    with torch.inference_mode():
        image_features = model.encode_image(image_input) # type: ignore
        image_features /= image_features.norm(
            dim=-1,
            keepdim=True
        )

    return image_features


# =====================================================
# 6. GENERIC SIMILARITY SCORING
# =====================================================

def calculate_similarity(image_features, text_features, names):
    similarities = (
        image_features @ text_features.T
    ).squeeze(0)

    scores = {
        name: float(score.item())
        for name, score in zip(names, similarities)

    }

    return dict(
        sorted(
            scores.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )


# =====================================================
# 7. IMAGE CONTEXT CLASSIFICATION
# =====================================================

def classify_image(image, image_features=None):
    if image_features is None:
        image_features = encode_image(image)

    scores = calculate_similarity(
        image_features,
        category_text_features,
        category_names
    )
    # image_features = encode_image(image)
    # scores = calculate_similarity(
    #     image_features,
    #     category_text_features,
    #     category_names
    # )

    ranked_categories = list(scores.items())
    top_category, top_score = ranked_categories[0]
    second_category, second_score = ranked_categories[1]
    margin = top_score - second_score

    # Initial decision rule.
    # These thresholds are experimental and must be
    # evaluated on our own test images.

    # is_expressive = (
    #     top_category in EXPRESSIVE_CATEGORIES
    #     and top_score >= 0.20
    #     and margin >= 0.01
    # )
    is_expressive = (top_category in EXPRESSIVE_CATEGORIES or top_score >= 0.2)

    return {
        "category": top_category,
        "scores": scores,
        "top_score": top_score,
        "second_category": second_category,
        "second_score": second_score,
        "margin": margin,
        "is_expressive": is_expressive
         }
# =====================================================
# 8. MOOD ANALYSIS
# =====================================================

def analyze_mood(image, image_features=None):
    # Reuse embedding if already calculated
    if image_features is None:
        image_features = encode_image(image)

    mood_scores = calculate_similarity(
        image_features,
        mood_text_features,
        mood_names
    )
    return mood_scores