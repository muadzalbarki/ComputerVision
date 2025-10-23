import cv2
import numpy as np
import math
import os

output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# =========================
# 1. Buat kanvas hitam
# =========================
height, width = 512, 512
canvas = np.zeros((height, width, 3), dtype=np.uint8)
center_x, center_y = width // 2, height // 2
radius = 100
# =========================
# 2. Gambar 6 elips di tengah, tiap elips diputar 60 derajat
# =========================
center = (256, 256)

for i in range(6):
    angle = i * 60  # tiap kelopak berputar 60 derajat
    # Outline hitam
    cv2.ellipse(canvas, center, (70, 130), angle, 0, 360, (0, 0, 0), -1)
    # Isi merah
    cv2.ellipse(canvas, center, (60, 120), angle, 0, 360, (0, 0, 255), -1)

# Tambahkan lingkaran tengah dan luar
cv2.circle(canvas, center, 200, (0, 0, 0), 10)  # outer border
cv2.circle(canvas, center, 40, (0, 0, 0), -1)   # pupil

# =========================
# 4. Tampilkan dan simpan hasil
# =========================
cv2.imshow("Mangekyou Sharingan Tengah", canvas)
cv2.imwrite(os.path.join(output_folder, "Mangekyou.png"), canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()

# =========================
# Rotated
# =========================
angle = 45
M_rotate = cv2.getRotationMatrix2D(center, angle, 1.0)
rotated = cv2.warpAffine(canvas, M_rotate, (width, height))
cv2.imwrite(os.path.join(output_folder, "Mangekyou_Rotate.png"), rotated)
cv2.imshow("Mangekyou_Rotate", rotated)
cv2.waitKey(0)
cv2.destroyAllWindows()

# =========================
# Resize
# =========================
resized = cv2.resize(canvas, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
cv2.imshow("Mangekyou_Resize", resized)
cv2.imwrite(os.path.join(output_folder, "Mangekyou_Resize.png"), resized)
cv2.waitKey(0)
cv2.destroyAllWindows()

# =========================
# Crop
# =========================
y, x = 100, 100
h, w = 200, 200
cropped = canvas[y:y+h, x:x+w]
cv2.imshow("Mangekyou_Crop", cropped)
cv2.imwrite(os.path.join(output_folder, "Mangekyou_Crop.png"), cropped)
cv2.waitKey(0)
cv2.destroyAllWindows()

# =========================
# Translasi
# =========================
tx, ty = 100, 50  # geser ke kanan dan ke bawah
M_translate = np.float32([[1, 0, tx], [0, 1, ty]])
translated = cv2.warpAffine(canvas, M_translate, (width, height))
cv2.imshow("Mangekyou_Translasi", translated)
cv2.imwrite(os.path.join(output_folder, "Mangekyou_Translasi.png"), translated)
cv2.waitKey(0)
cv2.destroyAllWindows()


# =========================
# Bitwise
# =========================
bitwise_and = cv2.bitwise_and(canvas, rotated)
bitwise_or = cv2.bitwise_or(canvas, rotated)
cv2.imwrite(os.path.join(output_folder, "Mangekyou_Bitwise_And.png"), bitwise_and)
cv2.imshow("Mangekyou_Bitwise_And.", bitwise_and)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.imwrite(os.path.join(output_folder, "Mangekyou_Bitwise_Or.png"), bitwise_or)
cv2.imshow("Mangekyou_Bitwise_Or.", bitwise_or)
cv2.waitKey(0)
cv2.destroyAllWindows()


background = cv2.imread("img/anime.jpg")

# Resize agar sesuai ukuran besar
background = cv2.resize(background, (1152, 768))

# Pilih salah satu hasil (misalnya hasil rotasi)
logo = bitwise_and
logo = cv2.resize(logo, (400, 400))

# Posisi di tengah bulan
x_offset, y_offset = 380, 60
rows, cols, _ = logo.shape

# Buat mask
logo_gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
_, mask = cv2.threshold(logo_gray, 10, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)

# Ambil area ROI di background
roi = background[y_offset:y_offset+rows, x_offset:x_offset+cols]

# Gabungkan logo dan background dengan operasi bitwise
bg_part = cv2.bitwise_and(roi, roi, mask=mask_inv)
fg_part = cv2.bitwise_and(logo, logo, mask=mask)
combined = cv2.add(bg_part, fg_part)
background[y_offset:y_offset+rows, x_offset:x_offset+cols] = combined


cv2.imwrite(os.path.join(output_folder, "0_Mangekyou_Final.png"), background)
cv2.imshow("Final Background", background)
cv2.waitKey(0)
cv2.destroyAllWindows()