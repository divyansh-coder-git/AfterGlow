MOOD_RULES = {
    "serene": {
        "brightness": "medium_high",
        "saturation": "low_medium",
        "warm_ratio": "low"
    },

    "melancholic": {
        "brightness": "low",
        "saturation": "low",
        "warm_ratio": "low"
    },

    "energetic": {
        "brightness": "high",
        "saturation": "high",
        "contrast": "high"
    },

    "mysterious": {
        "brightness": "low",
        "contrast": "medium_high",
        "saturation": "low_medium"
    },

    "nostalgic": {
        "warm_ratio": "high",
        "saturation": "low_medium"
    },

    "romantic": {
        "warm_ratio": "high",
        "brightness": "medium_high",
        "saturation": "medium"
    },

    "dramatic": {
        "contrast": "high",
        "brightness": "medium_low"
    },

    "hopeful": {
        "brightness": "high",
        "warm_ratio": "medium_high"
    }
}

FEATURE_RANGES = {
    "brightness": {
        "low": (0, 85),
        "medium": (85, 150),
        "high": (150, 255),
        "medium_high": (110, 200),
        "medium_low": (50, 120)
    },

    "saturation": {
        "low": (0, 70),
        "medium": (70, 140),
        "high": (140, 255),
        "low_medium": (40, 120)
    },

    "warm_ratio": {
        "low": (0, 0.25),
        "medium": (0.25, 0.50),
        "high": (0.50, 1.0),
        "medium_high": (0.35, 0.75)
    },

    "contrast": {
        "low": (0, 40),
        "medium": (40, 75),
        "high": (75, 150),
        "medium_high": (60, 120)
    }
}

def score_feature(value, feature_name, category):
    lower, upper = FEATURE_RANGES[feature_name][category]
    if lower <= value <= upper:
        return 1.0
    return 0.0

def calculate_visual_scores(features):
    visual_scores = {}
    for mood, rules in MOOD_RULES.items():
        scores = []
        for feature_name, category in rules.items():
            value = features[feature_name]
            score = score_feature(
                value,
                feature_name,
                category
            )
            scores.append(score)
        visual_scores[mood] = sum(scores) / len(scores)
    return visual_scores

def fuse_mood_scores(clip_scores, visual_scores, alpha=0.65):
    # 1. Extract minimum and maximum CLIP scores
    clip_values = list(clip_scores.values())
    min_score = min(clip_values)
    max_score = max(clip_values)
    # 2. Normalize CLIP scores
    normalized_clip = {}
    for mood, score in clip_scores.items():
        if max_score == min_score:
            normalized_clip[mood] = 0.0
        else:
            normalized_clip[mood] = (
                (score - min_score) / (max_score - min_score)
            )
    # 3. Combine CLIP and visual scores
    final_scores = {}
    for mood in clip_scores:
        clip_score = normalized_clip[mood]
        visual_score = visual_scores[mood]
        final_scores[mood] = (
            alpha * clip_score +
            (1 - alpha) * visual_score
        )
        
    # 4. Sort moods by final score
    final_scores = dict(
        sorted(
            final_scores.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )

    return final_scores