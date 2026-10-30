import cv2
from vision_features import extract_features

image = cv2.imread("test.jpg")

if image is None:
    raise ValueError("Could not load image!")

features = extract_features(image)

for key, value in features.items():
    print(f"{key}: {value}")