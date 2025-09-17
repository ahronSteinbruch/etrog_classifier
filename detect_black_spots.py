import cv2
import numpy as np

def detect_black_spots(image_path,black_thresh=60, min_area=5, max_area=500, erosion_size=10):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("לא הצלחתי לפתוח את התמונה")

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_yellow = np.array([20, 40, 40])
    upper_yellow = np.array([40, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise ValueError("לא נמצא אתרוג בתמונה")
    etrog_contour = max(contours, key=cv2.contourArea)

    precise_mask = np.zeros_like(mask)
    cv2.drawContours(precise_mask, [etrog_contour], -1, 255, -1)

    erosion_kernel = np.ones((erosion_size, erosion_size), np.uint8)
    inner_mask = cv2.erode(precise_mask, erosion_kernel, iterations=1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, black_thresh, 255, cv2.THRESH_BINARY_INV)

    thresh = cv2.bitwise_and(thresh, thresh, mask=inner_mask)

    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8), iterations=1)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    spots = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if min_area < area < max_area:
            x, y, w, h = cv2.boundingRect(cnt)
            cx, cy = x + w // 2, y + h // 2
            spots.append({"center": (cx, cy), "area": int(area)})
            cv2.drawContours(img, [cnt], -1, (0, 0, 255), 2)

    

    x, y, w, h = cv2.boundingRect(etrog_contour)
    top_third = y + h // 3
    middle_third = y + 2 * h // 3

    counts = {"top": 0, "middle": 0, "bottom": 0}
    for s in spots:
        _, cy = s["center"]
        if cy < top_third:
            counts["top"] += 1
        elif cy < middle_third:
            counts["middle"] += 1
        else:
            counts["bottom"] += 1
    list_of_counts=[counts["top"],counts["middle"],counts["bottom"]]
    return counts

print(detect_black_spots(
    r"C:\Users\IMOE001\Pictures\Screenshots\Screenshot 2025-09-15 114351.png"
))

