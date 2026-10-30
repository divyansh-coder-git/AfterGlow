import cv2
import time

from pipeline import process_image

def resize_for_display(image, max_width=700, max_height=600):

    height, width = image.shape[:2]

    scale = min(
        max_width / width,
        max_height / height
    )

    new_width = int(width * scale)
    new_height = int(height * scale)

    return cv2.resize(
        image,
        (new_width, new_height),
        interpolation=cv2.INTER_AREA
    )

image = cv2.imread("test.jpg")

if image is None:
    raise ValueError("Could not load image!")

start_time = time.perf_counter()

result = process_image(image)

elapsed = time.perf_counter() - start_time

# Print extracted features
print("\n========== VISUAL FEATURES ==========")

for key, value in result["features"].items():
    print(f"{key}: {value}")

# Print CLIP scores
print("\n========== CLIP SCORES ==========")

for mood, score in result["clip_scores"].items():
    print(f"{mood}: {score:.4f}")

# Print visual scores
print("\n========== VISUAL SCORES ==========")

for mood, score in result["visual_scores"].items():
    print(f"{mood}: {score:.3f}")

# Print final interpretation
print("\n========== FINAL MOOD SCORES ==========")

for mood, score in result["final_scores"].items():
    print(f"{mood}: {score:.3f}")

print("\nDominant mood:", result["dominant_mood"])

print(f"Total processing time: {elapsed:.3f} seconds")

# Display transformed image
original_display = resize_for_display(image)

transformed_display = resize_for_display(
    result["transformed_image"]
)

cv2.imshow("Original", original_display)
cv2.imshow("AFTERGLOW Result", transformed_display)

cv2.waitKey(0)
cv2.destroyAllWindows()