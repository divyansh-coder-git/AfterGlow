import torch
import open_clip
import cv2
import numpy as np
from PIL import Image

MOODS = {
    "serene": "A peaceful, calm and serene landscape",
    "melancholic": "A melancholic, lonely and sorrowful scene",
    "energetic": "A vibrant, lively and energetic scene",
    "mysterious": "A mysterious, dark and enigmatic scene",
    "nostalgic": "A nostalgic, dreamy and sentimental scene",
    "romantic": "A romantic, warm and beautiful scene",
    "dramatic": "A dramatic, intense and powerful scene",
    "hopeful": "An uplifting, optimistic and hopeful scene"
}

device = "cpu"
model, _, preprocess = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="laion2b_s34b_b79k",
    device=device
)
tokenizer = open_clip.get_tokenizer("ViT-B-32")
model.eval()

mood_texts = list(MOODS.values())
text_tokens = tokenizer(mood_texts)

with torch.no_grad():
    text_features = model.encode_text(text_tokens)
    text_features /= text_features.norm(
        dim=-1,
        keepdim=True
    )

print("CLIP model loaded successfully!")
print("Number of mood descriptions:", len(mood_texts))
print("Text embedding shape:", text_features.shape)

def analyze_mood(image):
    # 1. Convert OpenCV BGR image to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 2. Convert NumPy array to PIL Image
    pil_image = Image.fromarray(image_rgb)

    # 3. Apply CLIP preprocessing
    image_input = preprocess(pil_image).unsqueeze(0)

    # 4. Encode the image
    with torch.no_grad():
        image_features = model.encode_image(image_input)

        # Normalize image embedding
        image_features /= image_features.norm(
            dim=-1,
            keepdim=True
        )

        # 5. Calculate similarity with mood descriptions
        similarities = (image_features @ text_features.T).squeeze(0)

    # 6. Convert results into a dictionary
    mood_scores = {
        mood: float(score)
        for mood, score in zip(MOODS.keys(), similarities)
    }

    # 7. Sort moods from highest similarity to lowest
    mood_scores = dict(
        sorted(
            mood_scores.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

    return mood_scores