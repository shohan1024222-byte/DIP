# সহজভাবে Project-এর অর্থ

এটি **Digital Image Processing** project। স্যার মূলত ছবির pixel নিয়ে ১৪ ধরনের পরীক্ষা করতে বলেছেন। নতুন কোনো ছবি না দিলেও notebook নিজে sample image বানায়, তাই সরাসরি চালানো যাবে।

## কীভাবে চালাবে

### Google Colab

1. `easy_image_processing_project.ipynb` ফাইলটি Google Colab-এ upload করো।
2. `Runtime` থেকে `Run all` চাপো।
3. প্রতিটি section-এর নিচে ছবি, সংখ্যা এবং ব্যাখ্যা দেখা যাবে।

### Jupyter Notebook

```powershell
jupyter notebook easy_image_processing_project.ipynb
```

তারপর notebook খুলে `Run All` করো।

## Input এবং Output

| অংশ | Input | Output |
|---|---|---|
| Image inspection | grayscale ও color image | width, height, channels, dtype, bytes |
| Grayscale conversion | RGB image | 1-channel grayscale image |
| Classification | যেকোনো image | binary, grayscale বা full-color এবং কারণ |
| Modalities | তৈরি করা ৫টি sample | X-ray, satellite, microscopy, ultrasound, infrared এবং application |
| Thresholding | grayscale image, threshold 64/128/192 | black-white image |
| Spatial resolution | grayscale image | 128x128, 64x64, 32x32, 16x16 image |
| False contouring | grayscale image | 128 থেকে 2 gray-level image |
| Interpolation | 64x64 image | nearest, bilinear, bicubic enlarged image |
| Histogram | dark, bright, low-contrast image | তিনটি histogram |
| Neighbors | pixel coordinate | N4, diagonal ND, N8 |
| Distance | দুই pixel coordinate | Euclidean, D4, D8 |
| Arithmetic | একই size-এর দুই image | addition, subtraction, multiplication, division |
| Change detection | সামান্য পরিবর্তিত দুই image | পরিবর্তনের জায়গা উজ্জ্বল দেখা যাবে |
| Noise averaging | ২০টি noisy image | noise কমে যাওয়া averaged image |
| Logic operations | circle ও square binary image | AND, OR, NOT, XOR |
| Geometry | image, shift/angle/scale | translation, rotation, scaling |

## নিজের image ব্যবহার

Notebook-এর real image section-এ `USE_REAL_IMAGE = False` বদলে `True` করো। Google Colab-এ cell চালালে upload option আসবে। VS Code/Jupyter-এ `IMAGE_PATH = 'my_image.jpg'`-এ নিজের file path লিখবে। তারপর বাকি cellগুলো উপর থেকে নিচে চালাবে।

একটি color photo দিলে notebook সেটির grayscale version নিজে তৈরি করবে।

প্রথম code cell-এ sample image তৈরি করা হয়েছে। নিজের file ব্যবহার করতে চাইলে Colab-এ upload করে লিখতে পারো:

```python
from PIL import Image
import numpy as np
from google.colab import files
uploaded = files.upload()
filename = list(uploaded.keys())[0]
gray = np.array(Image.open(filename).convert('L'))
color = np.array(Image.open(filename).convert('RGB'))
```

তারপর নিচের cellগুলো আবার চালাবে। Grayscale কাজের জন্য `gray`, color কাজের জন্য `color` ব্যবহার করবে।

## গুরুত্বপূর্ণ ব্যাখ্যা

- `uint8` মানে প্রতিটি pixel 0 থেকে 255 পর্যন্ত মান রাখে।
- Grayscale image-এ 1টি channel থাকে; RGB color image-এ 3টি channel থাকে।
- Threshold-এর মানের চেয়ে বড় বা সমান pixel সাদা, অন্যগুলো কালো হয়।
- Spatial resolution কমলে বড় বড় block দেখা যায়।
- Gray level কমলে smooth gradient-এর বদলে band বা false contour দেখা যায়।
- Nearest-neighbor বেশি blocky, bilinear smooth, bicubic সাধারণত সবচেয়ে smooth।
- Histogram বামদিকে হলে dark, ডানদিকে হলে bright, সরু হলে low-contrast।
- Subtraction image-এ দুই ছবির আলাদা অংশ উজ্জ্বল হয়।
- ২০টি noisy image average করলে random noise কমে যায়।
- AND মানে overlap, OR মানে union, NOT মানে উল্টো, XOR মানে শুধু non-overlap অংশ।
- Transformation-এর পরে কালো অংশ মানে সেখানে কোনো source pixel ছিল না।

কোনো requirement বাদ দেওয়া হয়নি; notebook-এর প্রতিটি section স্যারের প্রশ্নের একটি অংশ পূরণ করে।
