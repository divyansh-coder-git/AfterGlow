from vision_features import extract_features
from clip_analyzer import analyze_mood
from mood_fusion import (
    calculate_visual_scores,
    fuse_mood_scores
)
from transformer import transform_image

def process_image(image):

    # 1. Extract OpenCV features
    features = extract_features(image)

    # 2. Get CLIP mood scores
    clip_scores = analyze_mood(image)

    # 3. Calculate handcrafted visual scores
    visual_scores = calculate_visual_scores(features)

    # 4. Fuse both scoring systems
    final_scores = fuse_mood_scores(
        clip_scores,
        visual_scores
    )

    # 5. Select the highest-ranked mood
    dominant_mood = next(iter(final_scores))

    # 6. Transform the original image
    transformed_image = transform_image(
        image,
        dominant_mood
    )

    return {
        "features": features,
        "clip_scores": clip_scores,
        "visual_scores": visual_scores,
        "final_scores": final_scores,
        "dominant_mood": dominant_mood,
        "transformed_image": transformed_image
    }