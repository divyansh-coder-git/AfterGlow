import cv2
import numpy as np

MOOD_STYLES = {
    "serene": {
        "brightness": 10,
        "contrast": 0.90,
        "saturation": 0.85,
        "warmth": -5,
        "vignette": 0.10
    },

    "melancholic": {
        "brightness": -15,
        "contrast": 1.10,
        "saturation": 0.55,
        "warmth": -15,
        "vignette": 0.35
    },

    "energetic": {
        "brightness": 15,
        "contrast": 1.20,
        "saturation": 1.50,
        "warmth": 10,
        "vignette": 0.05
    },

    "mysterious": {
        "brightness": -20,
        "contrast": 1.30,
        "saturation": 0.75,
        "warmth": -10,
        "vignette": 0.50
    },

    "nostalgic": {
        "brightness": 5,
        "contrast": 0.85,
        "saturation": 0.70,
        "warmth": 20,
        "vignette": 0.25
    },

    "romantic": {
        "brightness": 12,
        "contrast": 0.90,
        "saturation": 1.10,
        "warmth": 25,
        "vignette": 0.20
    },

    "dramatic": {
        "brightness": -5,
        "contrast": 1.50,
        "saturation": 0.90,
        "warmth": -5,
        "vignette": 0.40
    },

    "hopeful": {
        "brightness": 20,
        "contrast": 1.05,
        "saturation": 1.15,
        "warmth": 15,
        "vignette": 0.05
    }
}

def adjust_brightness_contrast(image, brightness, contrast):

    transformed = cv2.convertScaleAbs(
        image,
        alpha=contrast,
        beta=brightness
    )

    return transformed

def adjust_saturation(image, saturation):

    hsv = cv2.cvtColor(
        image,
        cv2.COLOR_BGR2HSV
    )

    hsv = hsv.astype(np.float32)

    hsv[:, :, 1] *= saturation

    hsv[:, :, 1] = np.clip(
        hsv[:, :, 1],
        0,
        255
    )

    hsv = hsv.astype(np.uint8)

    transformed = cv2.cvtColor(
        hsv,
        cv2.COLOR_HSV2BGR
    )

    return transformed

def adjust_warmth(image, warmth):

    image = image.astype(np.float32)

    # Adjust blue and red channels
    image[:, :, 0] -= warmth
    image[:, :, 2] += warmth

    image = np.clip(image, 0, 255)

    return image.astype(np.uint8)

def apply_vignette(image, strength):

    height, width = image.shape[:2]

    # Find image centre
    center_x = width / 2
    center_y = height / 2

    # Create coordinate grids
    x = np.arange(width)
    y = np.arange(height)

    xx, yy = np.meshgrid(x, y)

    # Calculate distance from centre
    distance = np.sqrt(
        ((xx - center_x) / center_x) ** 2 +
        ((yy - center_y) / center_y) ** 2
    )

    # Create vignette mask
    mask = 1 - strength * np.clip(distance, 0, 1)

    # Apply mask to all colour channels
    result = image.astype(np.float32)

    result *= mask[:, :, np.newaxis]

    result = np.clip(result, 0, 255)

    return result.astype(np.uint8)

def transform_image(image, mood):

    # Retrieve parameters for the selected mood
    style = MOOD_STYLES[mood]

    # 1. Adjust brightness and contrast
    result = adjust_brightness_contrast(
        image,
        brightness=style["brightness"],
        contrast=style["contrast"]
    )

    # 2. Adjust saturation
    result = adjust_saturation(
        result,
        saturation=style["saturation"]
    )

    # 3. Adjust warmth
    result = adjust_warmth(
        result,
        warmth=style["warmth"]
    )

    # 4. Apply vignette
    result = apply_vignette(
        result,
        strength=style["vignette"]
    )

    return result