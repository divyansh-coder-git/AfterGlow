import numpy as np
CLIP_LOW = 0.12187
CLIP_HIGH = 0.243395
MOODS = [
    "serene",
    "melancholic",
    "energetic",
    "mysterious",
    "nostalgic",
    "romantic",
    "dramatic",
    "hopeful"
]


def clamp(value):
    return float(np.clip(value, 0.0, 1.0))

def range_score(value, lower, upper, softness=0.10):
    """
        Continuous membership score.
        Maximum score inside the preferred range.
        Gradual penalty outside it.
        """
    if lower <= value <= upper:
        return 1.0

    distance = lower - value if value < lower else value - upper

    return float(np.exp(-distance / softness))

def gaussian_score(value, center, sigma):
    return float(
        np.exp(
            -0.5 * ((value - center) / sigma) ** 2
        )
    )

def calculate_visual_scores(features):

    b = features["brightness"]
    c = features["contrast"]
    s = features["saturation"]
    w = features["warm_ratio"]
    e = features["edge_density"]
    lc = features["local_contrast"]

    # Normalize features to approximately 0-1
    b /= 255
    c /= 128
    s /= 255
    lc /= 128

    scores = {}

    # Individual feature memberships

    bright = range_score(b, 0.50, 0.80)
    dark = range_score(b, 0.05, 0.25)

    saturated = range_score(s, 0.60, 0.90)
    muted = range_score(s, 0.10, 0.35)

    warm = range_score(w, 0.50, 0.85)
    cool = range_score(w, 0.0, 0.20)

    high_contrast = range_score(c, 0.50, 0.80)
    soft_contrast = range_score(c, 0.05, 0.25)

    high_edges = range_score(e, 0.10, 0.25, softness=0.025)
    low_edges = range_score(e, 0.0, 0.04, softness=0.025)

    high_local = range_score(lc, 0.40, 0.70)
    low_local = range_score(lc, 0.05, 0.18)

    serene_brightness = gaussian_score(b, center=0.46, sigma=0.24)
    serene_saturation = gaussian_score(s, center=0.40, sigma=0.16)
    serene_contrast = gaussian_score(c, center=0.36, sigma=0.20)
    serene_local = gaussian_score(lc, center=0.24, sigma=0.17)
    serene_edges = gaussian_score(e, center=0.035, sigma=0.055)

    serene_memberships = {
    "brightness": (serene_brightness, 0.10),
    "saturation": (serene_saturation, 0.25),
    "contrast": (serene_contrast, 0.15),
    "local_contrast": (serene_local, 0.25),
    "edge_density": (serene_edges, 0.25)
    }

    # print("\n--- FEATURE MEMBERSHIPS ---")

    # for name, value in {
    #     "bright": bright,
    #     "dark": dark,
    #     "saturated": saturated,
    #     "muted": muted,
    #     "warm": warm,
    #     "cool": cool,
    #     "high_contrast": high_contrast,
    #     "soft_contrast": soft_contrast,
    #     "high_edges": high_edges,
    #     "low_edges": low_edges,
    #     "high_local": high_local,
    #     "low_local": low_local
    # }.items():
    #     print(f"{name}: {value:.3f}")

    # Mood scoring

    # scores["serene"] = (
    #     0.20 * bright +
    #     0.25 * soft_contrast +
    #     0.25 * low_local +
    #     0.30 * low_edges
    # )

    scores["serene"] = float(np.exp(sum(weight * np.log(max(score, 1e-8)) for score, weight in serene_memberships.values())))

    scores["melancholic"] = (
        0.35 * dark +
        0.30 * muted +
        0.20 * cool +
        0.15 * soft_contrast
    )

    # scores["energetic"] = (
    #     0.25 * bright +
    #     0.25 * saturated +
    #     0.25 * high_contrast +
    #     0.25 * high_edges) * (
    #     0.5 + 0.5 * max(high_contrast, high_edges)
    # )

    # scores["energetic"] = (
    #     0.20 * bright +
    #     0.30 * saturated +
    #     0.25 * high_contrast +
    #     0.25 * high_edges
    # ) * (
    #     0.4 + 0.6 * max(high_contrast, high_edges)
    # )

    # scores["energetic"] = (
    #     bright *
    #     saturated *
    #     max(high_contrast, high_edges)
    # ) ** (1 / 3)

    scores["energetic"] = (
        bright * saturated * high_contrast
    ) ** (1 / 3) * (
        0.8 + 0.2 * high_edges
    )

    scores["mysterious"] = (
        0.30 * dark +
        0.25 * high_contrast +
        0.20 * muted +
        0.25 * high_local
    )

    scores["nostalgic"] = (
        0.35 * warm +
        0.30 * muted +
        0.20 * soft_contrast +
        0.15 * low_local
    )

    scores["romantic"] = (
        0.30 * warm +
        0.25 * bright +
        0.25 * soft_contrast +
        0.20 * muted
    )

    scores["dramatic"] = (
        0.30 * high_contrast +
        0.25 * dark +
        0.25 * high_local +
        0.20 * high_edges
    )

    scores["hopeful"] = (
        0.35 * bright +
        0.25 * warm +
        0.20 * saturated +
        0.20 * low_local
    )

    return {mood: clamp(score) for mood, score in scores.items()}

def normalize_clip_scores(clip_scores):
    normalized = {}
    clip_values = np.array(clip_scores)
    # CLIP_LOW = np.percentile(clip_values, 5)
    # CLIP_HIGH = np.percentile(clip_values, 95)
    print("CLIP_LOW:", CLIP_LOW)
    print("CLIP_HIGH:", CLIP_HIGH)
    for mood, score in clip_scores.items():
        normalized[mood] = float(np.clip((score - CLIP_LOW) /(CLIP_HIGH - CLIP_LOW),0,1))
    return normalized


def fuse_mood_scores(clip_scores, visual_scores, alpha=0.7):
    # clip_values = list(clip_scores.values())
    normalized_clip = normalize_clip_scores(clip_scores)
    final_scores = {}

    for mood in clip_scores:
        clip_score = normalized_clip[mood]
        visual_score = visual_scores[mood]

        final_scores[mood] = (
            alpha * clip_score +
            (1 - alpha) * visual_score
        )

    return dict(
        sorted(
            final_scores.items(),
            key=lambda item: item[1],
            reverse=True
        )
    )