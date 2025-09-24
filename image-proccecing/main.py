import cv2 as cv

DISPLAY_SIZE = 1024

img = cv.imread("image-proccecing/test_images/board10.jpg")
assert (
    img is not None
), "file could not be read, check with os.path.exists()"  # TODO read about python assert

img_for_display = cv.resize(img, dsize=None, fx=0.3, fy=0.3)
cv.imshow("pic", img_for_display)
cv.waitKey(0)
cv.destroyAllWindows()
