from mood_fusion import (
    calculate_visual_scores,
    fuse_mood_scores
)

features = {
    "brightness": 99.5,
    "contrast": 60,
    "saturation": 108,
    "warm_ratio": 0.14
}

clip_scores = {
    "serene": 0.2165,
    "energetic": 0.1928,
    "hopeful": 0.1895,
    "mysterious": 0.1600,
    "dramatic": 0.1548,
    "romantic": 0.1544,
    "nostalgic": 0.1503,
    "melancholic": 0.1219
}

visual_scores = calculate_visual_scores(features)

final_scores = fuse_mood_scores(
    clip_scores,
    visual_scores
)

print("\nFinal mood interpretation:\n")

for mood, score in final_scores.items():
    print(f"{mood}: {score:.3f}")