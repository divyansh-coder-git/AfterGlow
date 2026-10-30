import cv2
from clip_analyzer import classify_image

image = cv2.imread("test6.jpg")
if image is None:
    raise ValueError("Could not load image!")

result = classify_image(image)

print("\nIMAGE CATEGORY ANALYSIS\n")
for category, score in result["scores"].items():
    print(f"{category}: {score:.4f}")

print("\nFINAL DECISION")
print("Category:", result["category"])
print("Top score:", result["top_score"])
print("Margin:", result["margin"])
print("Mood analysis allowed:", result["is_expressive"])