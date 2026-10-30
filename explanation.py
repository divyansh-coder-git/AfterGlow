MOOD_EVIDENCE_TEXT = {
    "romantic": {
        "brightness": {
            "low": "Subdued lighting gives the scene an intimate character.",
            "medium": "Balanced lighting creates a welcoming atmosphere.",
            "high": "Bright lighting gives the scene an inviting quality."
        },
        "warm_ratio": {
            "low": "The cooler palette creates a more restrained atmosphere.",
            "medium": "The mixture of warm and cool tones adds visual richness.",
            "high": "Golden and warm tones reinforce the romantic atmosphere."
        },
        "contrast": {
            "low": "Soft transitions give the scene a gentle appearance.",
            "medium": "Balanced tonal differences preserve visual harmony.",
            "high": "Pronounced light and shadow create a striking composition."
        },
        "saturation": {
            "low": "Muted colours give the scene a subdued character.",
            "medium": "Moderate colour intensity maintains visual harmony.",
            "high": "Rich colours add vibrancy to the composition."
        }
    },

    "nostalgic": {
        "brightness": {
            "low": "Dim lighting creates a reflective atmosphere.",
            "medium": "Balanced lighting gives the scene a familiar quality.",
            "high": "Bright lighting creates a dreamy visual character."
        },
        "warm_ratio": {
            "low": "Cool tones give the scene a distant, reflective quality.",
            "medium": "The mixture of warm and cool tones adds visual depth.",
            "high": "Warm tones evoke the appearance of an old photograph."
        },
        "contrast": {
            "low": "Soft tonal transitions create a faded appearance.",
            "medium": "Moderate contrast preserves a natural visual balance.",
            "high": "Strong tonal differences make the scene visually striking."
        },
        "saturation": {
            "low": "Muted colours reinforce a faded, sentimental appearance.",
            "medium": "Moderate saturation keeps the colours natural.",
            "high": "Vivid colours give the scene a lively character."
        }
    },

    "mysterious": {
        "brightness": {
            "low": "Dark lighting creates a sense of visual uncertainty.",
            "medium": "Balanced lighting leaves room for visual ambiguity.",
            "high": "Bright surroundings contrast with the mysterious interpretation."
        },
        "warm_ratio": {
            "low": "Cool tones reinforce the enigmatic atmosphere.",
            "medium": "The colour contrast adds complexity to the scene.",
            "high": "Warm highlights stand out against the surrounding composition."
        },
        "contrast": {
            "low": "Soft tonal transitions create a subdued atmosphere.",
            "medium": "Moderate contrast preserves visual ambiguity.",
            "high": "Strong shadows and highlights create visual tension."
        },
        "saturation": {
            "low": "Muted colours contribute to a restrained appearance.",
            "medium": "Moderate colour intensity preserves the scene's atmosphere.",
            "high": "Vivid colours introduce unexpected visual intensity."
        }
    }
}

MOOD_INTERPRETATIONS = {
    "romantic": "The image carries a romantic atmosphere.",
    "nostalgic": "The image evokes a sense of nostalgia.",
    "serene": "The image conveys a sense of serenity.",
    "mysterious": "The image carries a mysterious atmosphere.",
    "energetic": "The image carries an energetic atmosphere.",
    "melancholic": "The image evokes a melancholic atmosphere.",
    "dramatic": "The image carries a dramatic atmosphere.",
    "hopeful": "The image conveys a sense of hope and optimism."
}

MOOD_EVIDENCE = {
    "romantic": ["warmth", "brightness", "saturation"],
    "nostalgic": ["warmth", "contrast", "saturation"],
    "serene": ["brightness", "contrast", "saturation"],
    "mysterious": ["brightness", "contrast", "saturation"],
    "melancholic": ["brightness", "saturation", "contrast"],
    "energetic": ["saturation", "brightness", "contrast"],
    "dramatic": ["contrast", "brightness", "saturation"],
    "hopeful": ["brightness", "warmth", "saturation"]
}

EVIDENCE_RULES = {
    "brightness": [
        (70, "low", "The image has a relatively dark appearance."),
        (170, "medium", "The image has balanced lighting."),
        (float("inf"), "high", "The image is dominated by bright visual elements.")
    ],

    "contrast": [
        (40, "low", "Soft tonal transitions create a gentle appearance."),
        (80, "medium", "Moderate contrast maintains visual balance."),
        (float("inf"), "high", "Strong contrast creates visual intensity.")
    ],

    "saturation": [
        (60, "low", "Muted colours give the image a subdued character."),
        (140, "medium", "The image has moderately saturated colours."),
        (float("inf"), "high", "Rich colours make the composition vibrant.")
    ],

    "warm_ratio": [
        (0.10, "low", "Cool tones dominate the colour palette."),
        (0.30, "medium", "Warm and cool tones coexist in the composition."),
        (float("inf"), "high", "Warm colours occupy a significant portion of the image.")
    ]
}

MOOD_WEIGHTS = {
    "romantic": {
        "warm_ratio": 0.40,
        "brightness": 0.25,
        "saturation": 0.20,
        "contrast": 0.15
    },

    "nostalgic": {
        "warm_ratio": 0.35,
        "saturation": 0.30,
        "contrast": 0.20,
        "brightness": 0.15
    },

    "serene": {
        "contrast": 0.35,
        "brightness": 0.30,
        "saturation": 0.20,
        "warm_ratio": 0.15
    },

    "mysterious": {
        "contrast": 0.40,
        "brightness": 0.30,
        "saturation": 0.20,
        "warm_ratio": 0.10
    },

    "melancholic": {
        "brightness": 0.35,
        "saturation": 0.30,
        "contrast": 0.20,
        "warm_ratio": 0.15
    },

    "energetic": {
        "saturation": 0.40,
        "brightness": 0.30,
        "contrast": 0.20,
        "warm_ratio": 0.10
    },

    "dramatic": {
        "contrast": 0.45,
        "brightness": 0.25,
        "saturation": 0.20,
        "warm_ratio": 0.10
    },

    "hopeful": {
        "brightness": 0.40,
        "warm_ratio": 0.30,
        "saturation": 0.20,
        "contrast": 0.10
    }
}

MOOD_EXPECTATIONS = {
    "romantic": {
        "warm_ratio": ["medium", "high"],
        "brightness": ["medium", "high"],
        "saturation": ["medium", "high"],
        "contrast": ["low", "medium"]
    },

    "nostalgic": {
        "warm_ratio": ["medium", "high"],
        "brightness": ["low", "medium"],
        "saturation": ["low", "medium"],
        "contrast": ["low", "medium"]
    },

    "serene": {
        "brightness": ["medium", "high"],
        "contrast": ["low", "medium"],
        "saturation": ["low", "medium"],
        "warm_ratio": ["low", "medium"]
    },

    "mysterious": {
        "brightness": ["low", "medium"],
        "contrast": ["medium", "high"],
        "saturation": ["low", "medium"],
        "warm_ratio": ["low", "medium"]
    },

    "melancholic": {
        "brightness": ["low", "medium"],
        "saturation": ["low", "medium"],
        "contrast": ["low", "medium"],
        "warm_ratio": ["low", "medium"]
    },

    "energetic": {
        "saturation": ["medium", "high"],
        "brightness": ["medium", "high"],
        "contrast": ["medium", "high"],
        "warm_ratio": ["medium", "high"]
    },

    "dramatic": {
        "contrast": ["high"],
        "brightness": ["low", "medium"],
        "saturation": ["medium", "high"],
        "warm_ratio": ["low", "medium", "high"]
    },

    "hopeful": {
        "brightness": ["medium", "high"],
        "warm_ratio": ["medium", "high"],
        "saturation": ["medium", "high"],
        "contrast": ["low", "medium"]
    }
}

def evaluate_evidence(mood, features):

    expectations = MOOD_EXPECTATIONS[mood]
    weights = MOOD_WEIGHTS[mood]

    results = []

    for feature, expected_levels in expectations.items():

        value = features[feature]

        level, description = get_feature_description(
            feature, value
        )

        if level in expected_levels:
            status = "supporting"
        else:
            status = "contradictory"

        results.append({
            "feature": feature,
            "value": value,
            "level": level,
            "weight": weights[feature],
            "status": status,
            "description": description
        })

    return results


def select_relevant_evidence(mood, features, top_k=2):

    weights = MOOD_WEIGHTS[mood]

    ranked_features = sorted(
        weights.items(),
        key=lambda item: item[1],
        reverse=True
    )

    selected = []

    for feature, weight in ranked_features[:top_k]:

        value = features[feature]

        level, description = get_feature_description(
            feature, value
        )

        selected.append({
            "feature": feature,
            "value": value,
            "level": level,
            "weight": weight,
            "description": description
        })

    return selected

def get_feature_description(feature, value):

    rules = EVIDENCE_RULES[feature]

    for threshold, level, description in rules:
        if value < threshold:
            return level, description

    return None, None

def describe_visual_features(features):

    descriptions = []

    brightness = features["brightness"]
    contrast = features["contrast"]
    saturation = features["saturation"]
    warm_ratio = features["warm_ratio"]

    # Brightness
    if brightness < 70:
        descriptions.append("The image has a relatively dark appearance.")
    elif brightness > 170:
        descriptions.append("The image is dominated by bright visual elements.")
    else:
        descriptions.append("The image has a balanced distribution of light.")

    # Contrast
    if contrast < 40:
        descriptions.append("Soft tonal transitions give the image a gentle appearance.")
    elif contrast > 80:
        descriptions.append("Strong contrast creates visual intensity and depth.")
    else:
        descriptions.append("Moderate contrast preserves a balanced visual structure.")

    # Saturation
    if saturation < 60:
        descriptions.append("Muted colours give the composition a subdued character.")
    elif saturation > 140:
        descriptions.append("Rich colours make the composition visually vibrant.")
    else:
        descriptions.append("The colours retain a moderate level of intensity.")

    # Warmth
    if warm_ratio < 0.10:
        descriptions.append("Cool tones dominate the colour palette.")
    elif warm_ratio > 0.30:
        descriptions.append("Warm colours occupy a significant portion of the image.")
    else:
        descriptions.append("Warm and cool colours coexist in the composition.")

    return descriptions


def generate_explanation(mood, features):

    explanation = MOOD_INTERPRETATIONS[mood]
    relevant_features = MOOD_EVIDENCE[mood]

    for feature in relevant_features:

        value = features[feature]

        level, _ = get_feature_description(feature, value)

        mood_text = MOOD_EVIDENCE_TEXT.get(mood, {})
        feature_text = mood_text.get(feature, {})

        description = feature_text.get(level)

        if description:
            explanation.append(description)

    return " ".join(explanation)

def calculate_evidence_score(mood, features):

    evidence = evaluate_evidence(mood, features)

    total_weight = 0
    supporting_weight = 0
    contradictory_weight = 0

    for item in evidence:

        weight = item["weight"]
        total_weight += weight

        if item["status"] == "supporting":
            supporting_weight += weight

        elif item["status"] == "contradictory":
            contradictory_weight += weight

    support_score = supporting_weight / total_weight
    contradiction_score = contradictory_weight / total_weight

    return {
        "support_score": support_score,
        "contradiction_score": contradiction_score,
        "evidence": evidence
    }

def generate_final_explanation(mood, features):

    result = calculate_evidence_score(mood, features)

    evidence = result["evidence"]

    supporting = [
        item for item in evidence
        if item["status"] == "supporting"
    ]

    contradictory = [
        item for item in evidence
        if item["status"] == "contradictory"
    ]

    explanation = [
        MOOD_INTERPRETATIONS[mood]
    ]

    if supporting:
        explanation.append(
            "Visual characteristics supporting this interpretation include:"
        )

        for item in supporting:
            explanation.append(item["description"])

    if contradictory:
        explanation.append(
            "However, some characteristics contrast with this interpretation:"
        )

        for item in contradictory:
            explanation.append(item["description"])

    return {
        "text": " ".join(explanation),
        "support_score": result["support_score"],
        "contradiction_score": result["contradiction_score"],
        "evidence": evidence
    }


features = {
    "brightness": 99.5,
    "contrast": 60.0,
    "saturation": 108.0,
    "warm_ratio": 0.14
}

result = generate_final_explanation("romantic", features)

print(result["text"])

print(
    f"\nEvidence support: "
    f"{result['support_score'] * 100:.1f}%"
)

print(
    f"Contradictory evidence: "
    f"{result['contradiction_score'] * 100:.1f}%"
)