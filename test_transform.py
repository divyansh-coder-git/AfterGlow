import cv2

from transformer import transform_image

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

for mood in ["serene", "mysterious", "energetic", "nostalgic"]:

    result = transform_image(image, mood)

    cv2.imshow(mood, resize_for_display(result))

cv2.waitKey(0)
cv2.destroyAllWindows()
