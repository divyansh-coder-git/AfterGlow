import cv2
import numpy as np
import time

def extract_features(image):
    start_time = time.perf_counter()
    # 1. Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 2. Calculate brightness
    brightness = np.mean(gray)

    # 3. Calculate contrast
    contrast = np.std(gray)

    # 4. Convert to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 5. Calculate average saturation
    saturation = np.mean(hsv[:, :, 1])

    # 6. Calculate warm colour proportion
    warm_mask_1 = cv2.inRange(
        hsv,
        np.array([0, 50, 50]),
        np.array([35, 255, 255])
    )

    warm_mask_2 = cv2.inRange(
        hsv,
        np.array([160, 50, 50]),
        np.array([179, 255, 255])
    )

    warm_mask = cv2.bitwise_or(warm_mask_1, warm_mask_2)
    warm_ratio = np.count_nonzero(warm_mask) / warm_mask.size

    # 7. Calculate edge density
    edges = cv2.Canny(gray, 100, 200)

    edge_density = np.count_nonzero(edges) / edges.size

    # 8. Calculate local contrast
    height, width = gray.shape

    grid_size = 4
    local_contrasts = []
    for row in range(grid_size):
        for col in range(grid_size):

            y1 = row * height // grid_size
            y2 = (row + 1) * height // grid_size

            x1 = col * width // grid_size
            x2 = (col + 1) * width // grid_size

            region = gray[y1:y2, x1:x2]

            local_contrasts.append(np.std(region))

    local_contrast = np.mean(local_contrasts)

    kmeans_start = time.perf_counter()

    # 7. Find dominant colours using K-Means

    pixels = image.reshape((-1, 3)).astype(np.float32)

    # Randomly sample 10,000 pixels
    if len(pixels) > 10000:
        indices = np.random.choice(
            len(pixels),
            10000,
            replace=False
        )

        pixels = pixels[indices]

    criteria = (
        cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER,
        50,
        0.2
    )

    compactness, labels, centers = cv2.kmeans(
        pixels,
        5,
        None,
        criteria,
        3,
        cv2.KMEANS_PP_CENTERS
    )

    counts = np.bincount(labels.flatten())
    sorted_indices = np.argsort(counts)[::-1]
    dominant_colors = centers[sorted_indices].astype(np.uint8)
    color_ratios = counts[sorted_indices] / len(labels)

    print("K-Means time:", round(time.perf_counter() - kmeans_start, 4), "seconds")
    print("Total feature extraction time:", round(time.perf_counter() - start_time, 4),"seconds")
    # 8. Return extracted features
    return {
        "brightness": float(brightness),
        "contrast": float(contrast),
        "saturation": float(saturation),
        "warm_ratio": float(warm_ratio),

        "edge_density": float(edge_density),
        "local_contrast": float(local_contrast),

        "dominant_colors": dominant_colors.tolist(),
        "color_ratios": color_ratios.tolist()
    }
