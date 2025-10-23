# 🌀 Mangekyou Sharingan with OpenCV

Proyek ini menampilkan bagaimana **OpenCV (cv2)** dan **NumPy (np)** digunakan untuk membuat dan memanipulasi gambar secara programatik.  
Program menggambar pola **Mangekyou Sharingan**, melakukan berbagai **transformasi citra (rotasi, resize, crop, translasi)**,  
serta menempelkan hasilnya ke dalam **gambar latar (background anime)**.

---

## 📦 Fitur Utama

- 🎨 Membuat gambar Sharingan dari nol (tanpa file eksternal)
- 🔁 Transformasi citra: rotasi, resize, crop, dan translasi
- 🧮 Operasi bitwise antar gambar
- 🌌 Menempelkan gambar Sharingan ke background anime
- 💾 Semua hasil otomatis disimpan ke folder `output/`

---

## ⚙️ Instalasi

Pastikan kamu sudah menginstal **Python 3.x** serta library yang dibutuhkan.

```bash
pip install opencv-python numpy
```

---

## 🧠 Penjelasan Kode

### 1️⃣ Persiapan & Pembuatan Kanvas

```python
import cv2
import numpy as np
import os
```
- `cv2` → library OpenCV untuk pemrosesan gambar.
- `numpy` → untuk membuat dan memanipulasi array gambar.
- `os` → untuk membuat folder output dan menyimpan hasil.

```python
output_folder = "output"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
```
- Membuat folder `output` jika belum ada, agar semua hasil disimpan di tempat yang sama.

```python
height, width = 512, 512
canvas = np.zeros((height, width, 3), dtype=np.uint8)
center = (width // 2, height // 2)
```
- `np.zeros()` membuat kanvas kosong berwarna hitam (semua pixel bernilai 0).
- `height, width = 512` berarti ukuran kanvas 512×512 piksel.
- `dtype=np.uint8` artinya setiap nilai piksel disimpan sebagai bilangan 8-bit (0–255).
- `center` menentukan titik tengah (256, 256).

---

### 2️⃣ Membuat Pola Mangekyou Sharingan

```python
for i in range(6):
    angle = i * 60
    cv2.ellipse(canvas, center, (70, 130), angle, 0, 360, (0, 0, 0), -1)
    cv2.ellipse(canvas, center, (60, 120), angle, 0, 360, (0, 0, 255), -1)
```
- Menggambar 6 elips di pusat kanvas, masing-masing diputar 60° untuk membentuk pola melingkar.
- Elips pertama diwarnai __hitam__ (outline), lalu elips kedua diwarnai __merah__ (isi).
- Fungsi `cv2.ellipse()`:
    - Parameter `(center_x, center_y)` → posisi tengah elips.
    - `(70, 130)` → ukuran sumbu pendek dan panjang.
    - `angle` → sudut rotasi elips.
    - `(0, 0, 255)` → warna merah dalam format BGR.
    - `-1` → isi penuh (bukan garis tepi).

```python
cv2.circle(canvas, center, 200, (0, 0, 0), 10)
cv2.circle(canvas, center, 40, (0, 0, 0), -1)
```
- `cv2.circle()` menggambar lingkaran.
- Lingkaran besar (radius 200, tebal garis 10) = batas luar.
- Lingkaran kecil (radius 40, isi penuh) = pupil tengah.

---

### 3️⃣ Transformasi Gambar

#### 🔁 Rotasi
```python
M_rotate = cv2.getRotationMatrix2D(center, 45, 1.0)
rotated = cv2.warpAffine(canvas, M_rotate, (width, height))
```
- `cv2.getRotationMatrix2D()` menghasilkan matriks transformasi rotasi.
    - `center` → titik pusat rotasi.
    - `45` → sudut rotasi 45°.
    - `1.0` → skala citra (tidak diperbesar/diperkecil).
- `cv2.warpAffine()` menerapkan rotasi ke gambar menggunakan matriks tersebut.

#### ↗️ Resize
```python
resized = cv2.resize(canvas, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_LINEAR)
```
- `fx` dan `fy` → faktor skala horizontal dan vertikal.
- `1.5` artinya gambar diperbesar 150%.
- `cv2.INTER_LINEAR` → metode interpolasi untuk menjaga kualitas gambar.

#### ✂️ Crop
```python
cropped = canvas[100:300, 100:300]
```
- Memotong bagian dari koordinat `(100,100)` dengan tinggi dan lebar 200 piksel.
- Operasi ini menggunakan konsep __slicing array NumPy__.

#### ↔️ Translasi
```python
tx, ty = 100, 50
M_translate = np.float32([[1, 0, tx], [0, 1, ty]])
translated = cv2.warpAffine(canvas, M_translate, (width, height))
```
- `tx`, `ty` = jarak pergeseran (kanan dan bawah).
- Matriks translasi memindahkan posisi gambar di kanvas.
- `cv2.warpAffine()` menerapkan translasi ke seluruh piksel.

---

### 4️⃣ Operasi Bitwise

```python
bitwise_and = cv2.bitwise_and(canvas, rotated)
bitwise_or = cv2.bitwise_or(canvas, rotated)
```
- `bitwise_and` → hanya mempertahankan bagian gambar yang sama-sama tidak hitam di canvas dan rotated.
- `bitwise_or` → menggabungkan dua gambar, mempertahankan semua area berwarna dari keduanya.
- Berguna untuk efek pencampuran atau mask.

---

### 5️⃣ Menambahkan Background

```python
background = cv2.imread("img/anime.jpg")
background = cv2.resize(background, (1152, 768))
```
- Membaca gambar latar belakang anime dan menyesuaikan ukurannya.

```python
logo = bitwise_and
logo = cv2.resize(logo, (400, 400))
x_offset, y_offset = 380, 60
rows, cols, _ = logo.shape
```
- Gunakan hasil transformasi (misal `rotated`) sebagai logo yang akan ditempelkan.
- Tentukan ukuran dan posisi (`x_offset`, `y_offset`) di mana logo akan ditempel di background.

#### Membuat Mask dan Gabungkan
```python
logo_gray = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
_, mask = cv2.threshold(logo_gray, 10, 255, cv2.THRESH_BINARY)
mask_inv = cv2.bitwise_not(mask)

roi = background[y_offset:y_offset+rows, x_offset:x_offset+cols]
bg_part = cv2.bitwise_and(roi, roi, mask=mask_inv)
fg_part = cv2.bitwise_and(logo, logo, mask=mask)
combined = cv2.add(bg_part, fg_part)
background[y_offset:y_offset+rows, x_offset:x_offset+cols] = combined
```
- `mask` mendeteksi area tidak hitam dari logo.  
- `mask_inv` digunakan untuk menjaga latar belakang tetap terlihat.  
- `bitwise_and` dipakai untuk menempelkan logo tanpa kotak hitam.
- `cv2.add()` menumpuk keduanya untuk menghasilkan hasil akhir.

---

### 6️⃣ Menyimpan Hasil
```python
cv2.imwrite(os.path.join(output_folder, "0_Mangekyou_Final.png"), background)
cv2.imshow("Final Background", background)
```
- `cv2.imwrite` untuk menyimpan output
- `cv2.imshow` untuk menampilkan output

Semua hasil disimpan ke dalam folder `output/`, termasuk:

| Nama File | Deskripsi |
|------------|------------|
| `Mangekyou.png` | Gambar dasar Sharingan |
| `Mangekyou_Rotate.png` | Hasil rotasi 45° |
| `Mangekyou_Resize.png` | Hasil resize |
| `Mangekyou_Crop.png` | Hasil crop |
| `Mangekyou_Translasi.png` | Hasil translasi |
| `Mangekyou_Bitwise_And.png` | Operasi bitwise AND |
| `Mangekyou_Bitwise_Or.png` | Operasi bitwise OR |
| `0_Mangekyou_Final.png` | Hasil akhir di background anime |

---


## 💡 Catatan

- Jalankan di editor seperti VS Code, Jupyter, atau terminal Python biasa.  
- Pastikan jalur `anime.jpg` benar sesuai lokasi file di sistemmu.  
- Tekan **`ESC` atau tombol apa pun** saat jendela OpenCV terbuka untuk menutup hasil tampilan.

---

## 🧑‍💻 Penulis

**Mu’adz Al Barki**  
📅 Tahun: 2025  
🧠 Proyek UTS Computer Vision dan Grafika Digital menggunakan OpenCV Teknologi Informasi UIN Salatiga

