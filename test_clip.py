import cv2
import time
from clip_analyzer import analyze_mood

image = cv2.imread("test.jpg")

if image is None:
    raise ValueError("Could not load image!")

start = time.perf_counter()

scores = analyze_mood(image)

elapsed = time.perf_counter() - start

print("\nCLIP Mood Analysis:")

for mood, score in scores.items():
    print(f"{mood}: {score:.4f}")

print(f"\nInference time: {elapsed:.3f} seconds")