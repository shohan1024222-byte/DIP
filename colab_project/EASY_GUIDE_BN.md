# Google Colab Auto-Generated Image Guide

এই guide অনুসরণ করলে কোনো বাইরের image না দিয়েই পুরো Digital Image Processing project চালানো যাবে। Notebook নিজে থেকে sample grayscale ও color image তৈরি করবে।

## Project কী করে

Generated sample image নিয়ে notebook এটি করবে:

1. Image-এর width, height, channel, data type এবং byte size দেখাবে।
2. Color image-কে grayscale করবে।
3. Image binary, grayscale নাকি full-color তা বলবে।
4. Threshold দিয়ে black-white image বানাবে।
5. Resolution কমিয়ে blocky effect দেখাবে।
6. Gray level কমিয়ে false contouring দেখাবে।
7. Nearest, bilinear এবং bicubic interpolation তুলনা করবে।
8. Dark, bright এবং low-contrast histogram দেখাবে।
9. Pixel neighbors এবং distance হিসাব করবে।
10. Addition, subtraction, multiplication এবং division করবে।
11. দুই ছবির change detection দেখাবে।
12. ২০টি noisy image average করে noise কমাবে।
13. AND, OR, NOT এবং XOR দেখাবে।
14. Translation, rotation এবং scaling দেখাবে।

## আগে যা লাগবে

- Google account
- `colab_project/easy_image_processing_project.ipynb`

## Google Colab চালানোর সম্পূর্ণ নিয়ম

### ধাপ ১: Notebook upload

1. [Google Colab](https://colab.research.google.com/) খুলবে।
2. `File` মেনু থেকে `Upload notebook` চাপবে।
3. এই folder-এর `easy_image_processing_project.ipynb` select করবে।
4. Notebook খুললে সব code cell দেখা যাবে।

### ধাপ ২: সব cell উপর থেকে নিচে চালানো

প্রথমে menu থেকে `Runtime > Run all` চাপবে। Notebook একে একে cell চালাবে। প্রথমবার package বা permission চাইলে অনুমতি দেবে।

### ধাপ ৩: generated image নিশ্চিত করা

প্রথম code cell-এ `Sample images created: (256, 256) (256, 256, 3)` দেখা যাবে। এটিই প্রমাণ যে notebook নিজে input তৈরি করেছে। কোনো file chooser, upload box বা image path আসবে না।

## কোন generated image কোন কাজে যাবে

- Generated color image: inspection, color-to-grayscale এবং color classification-এর জন্য।
- Generated gray image: thresholding, resolution, false contouring এবং histogram-এর জন্য।
- Notebook প্রথম cell-এই color ও grayscale array তৈরি করে; কোনো আলাদা image file দরকার নেই।
- Modality section-এর X-ray, satellite, microscopy, ultrasound ও infrared image-ও generated gray/color array থেকে তৈরি হয়।

## Output কীভাবে বুঝবে

| Section | Input | কী output দেখবে |
|---|---|---|
| Inspection | generated gray/color image | width, height, channel, dtype, bytes |
| Conversion | color image | original ও grayscale পাশাপাশি |
| Classification | binary/gray/color | category এবং unique value/channel-এর কারণ |
| Modalities | পাঁচটি educational sample | X-ray, satellite, microscopy, ultrasound, infrared |
| Thresholding | gray image | threshold 64, 128, 192-এর black-white ফল |
| Spatial resolution | gray image | 128, 64, 32, 16-এর blocky ফল |
| False contouring | gray image | 128, 64, 32, 16, 8, 4, 2 gray-level ফল |
| Interpolation | 64x64 version | nearest, bilinear, bicubic enlargement |
| Histogram | dark/bright/low contrast versions | তিনটি histogram এবং interpretation |
| Neighbors | middle, edge, corner pixel | N4, diagonal ND, N8 |
| Distance | দুই coordinate | Euclidean, D4, D8 |
| Arithmetic | দুই same-size image | add, subtract, multiply, divide |
| Change detection | সামান্য পরিবর্তিত image pair | পরিবর্তিত অংশ উজ্জ্বল |
| Noise averaging | ২০টি noisy copy | noisy copy বনাম average |
| Logic | circle এবং square | AND, OR, NOT, XOR |
| Geometry | generated gray image | translation, rotation, scaling |

## Assignment জমা দেওয়ার জন্য

1. প্রতিটি section-এর output-এর screenshot নাও।
2. Inspection output-এ width, height, channels এবং bytes লিখে রাখো।
3. Thresholding-এর তিনটি result compare করো।
4. Resolution কমলে block বড় হয়, এই observation লিখো।
5. Gray level কমলে band বা false contour দেখা যায়, এটি লিখো।
6. Histogram-এর নিচে dark/bright/low-contrast ব্যাখ্যা লিখো।
7. Distance অংশে hand calculation দাও: `dx=3, dy=4`, তাই Euclidean `5`, D4 `7`, D8 `4`।
8. শেষে সব screenshot ও explanation একসঙ্গে report-এ রাখো।

## Common error এবং সমাধান

### `NameError: plt is not defined`

প্রথম setup cell চালানো হয়নি। `Runtime > Restart session`, তারপর `Runtime > Run all` করো।

### Sample image তৈরি হচ্ছে না

প্রথম setup code cell চালানো হয়েছে কি না দেখো। `Runtime > Restart session`, তারপর `Runtime > Run all` করো।

### Image দেখা যাচ্ছে না

Cell-এর নিচে output পর্যন্ত scroll করো। প্রতিটি figure notebook-এর cell-এর নিচে দেখা যায়।

### Image খুব বড় বা ছোট

সমস্যা নয়। Code নিজে image-এর actual width এবং height ব্যবহার করে।

## Team checklist

- [ ] প্রথম cell-এ `Sample images created` দেখা গেছে
- [ ] `Run all` সম্পূর্ণ হয়েছে
- [ ] কোনো error নেই
- [ ] সব figure-এর screenshot নেওয়া হয়েছে
- [ ] threshold comparison লেখা হয়েছে
- [ ] checkerboard/block effect লেখা হয়েছে
- [ ] false contouring লেখা হয়েছে
- [ ] histogram interpretation লেখা হয়েছে
- [ ] distance hand calculation লেখা হয়েছে
- [ ] modality ও application sentence লেখা হয়েছে

এই notebook-এর সব image-processing অংশ automatically generated sample image দিয়ে চলে। কোনো real image, external file, upload বা path প্রয়োজন নেই।
