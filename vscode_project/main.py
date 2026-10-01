"""Easy Digital Image Processing project for VS Code.
Run: python main.py
Use a real image with: python main.py --image path\n"""
import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).parent
OUT = ROOT / "outputs"
SHOW_IMAGES = True


def inspect(image):
    channels = 1 if image.ndim == 2 else image.shape[2]
    return {"width": image.shape[1], "height": image.shape[0], "channels": channels, "dtype": str(image.dtype), "bytes": image.nbytes}


def show(images, titles, filename, columns=3, heading=None, description=None):
    rows = (len(images) + columns - 1) // columns
    figure = plt.figure(figsize=(4.6 * columns, 3.5 * rows + 0.7))
    for i, (image, title) in enumerate(zip(images, titles), 1):
        plt.subplot(rows, columns, i)
        image = np.asarray(image)
        display_image = np.clip(image, 0, 255).astype(np.uint8)
        if display_image.ndim == 2:
            plt.imshow(display_image, cmap="gray", vmin=0, vmax=255)
        else:
            plt.imshow(display_image)
        plt.title(title)
        plt.axis("off")
    if heading:
        figure.suptitle(heading, fontsize=15, fontweight="bold")
    if description:
        figure.text(0.5, 0.015, description, ha="center", va="bottom", fontsize=9, wrap=True)
    figure.tight_layout(rect=(0, 0.06 if description else 0.02, 1, 0.93 if heading else 0.98))
    figure.savefig(OUT / filename, dpi=150, bbox_inches="tight")
    if SHOW_IMAGES:
        plt.show()
    plt.close(figure)


def save_histogram(image, name, title, description):
    figure, axis = plt.subplots(figsize=(7, 4.5))
    axis.hist(np.asarray(image, dtype=np.uint8).ravel(), bins=256, range=(0, 255), color="#1f2937")
    axis.set_title(title, fontweight="bold")
    axis.set_xlabel("Pixel intensity (0 = black, 255 = white)")
    axis.set_ylabel("Number of pixels")
    axis.set_xlim(0, 255)
    figure.text(0.5, 0.015, description, ha="center", va="bottom", fontsize=9, wrap=True)
    figure.tight_layout(rect=(0, 0.08, 1, 0.95))
    figure.savefig(OUT / f"histogram_{name}.png", dpi=150, bbox_inches="tight")
    if SHOW_IMAGES:
        plt.show()
    plt.close(figure)


def make_sample():
    gray = np.tile(np.linspace(0, 255, 256, dtype=np.uint8), (256, 1))
    image = Image.fromarray(gray)
    draw = ImageDraw.Draw(image)
    draw.ellipse((40, 55, 145, 160), fill=220)
    draw.rectangle((155, 75, 225, 180), fill=40)
    gray = np.array(image)
    color = np.stack([gray, np.roll(gray, 25, axis=1), np.flipud(gray)], axis=2)
    return gray, color


def classify(image):
    if image.ndim == 2:
        unique = len(np.unique(image))
        if unique <= 2:
            return "binary", f"detected {unique} unique values"
        return "grayscale", f"detected {unique} intensity values"
    return "full-color", f"detected {image.shape[2]} channels"


def neighbors(x, y, width, height):
    n4 = {(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)}
    diagonal = {(x - 1, y - 1), (x - 1, y + 1), (x + 1, y - 1), (x + 1, y + 1)}
    valid = lambda points: {(a, b) for a, b in points if 0 <= a < width and 0 <= b < height}
    n4, diagonal = valid(n4), valid(diagonal)
    return n4, diagonal, n4 | diagonal


def distances(first, second):
    dx = abs(first[0] - second[0])
    dy = abs(first[1] - second[1])
    return np.hypot(dx, dy), dx + dy, max(dx, dy)


def main():
    global SHOW_IMAGES
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="optional real image path")
    parser.add_argument("--no-show", action="store_true", help="save figures without opening image windows")
    args = parser.parse_args()
    SHOW_IMAGES = not args.no_show
    OUT.mkdir(exist_ok=True)

    if args.image:
        source = Image.open(args.image)
        gray = np.array(source.convert("L"))
        color = np.array(source.convert("RGB"))
        print("Real image loaded:", args.image)
    else:
        gray, color = make_sample()
        print("Generated sample image used")

    print("\n1. INSPECTION")
    print("Grayscale:", inspect(gray))
    print("Color:", inspect(color))
    gray_from_color = np.dot(color[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)
    print("\n2. CONVERSION")
    print("Before:", color.nbytes, "bytes; after:", gray_from_color.nbytes, "bytes")
    show(
        [color, gray_from_color],
        ["Input: RGB color", "Output: grayscale"],
        "01_conversion.png",
        2,
        "Color to Grayscale Conversion",
        "The same image is shown before and after conversion. RGB has 3 channels; grayscale has 1 channel.",
    )

    print("\n3. CLASSIFICATION")
    binary = np.where(gray >= 128, 255, 0).astype(np.uint8)
    for name, image in [("binary", binary), ("grayscale", gray), ("color", color)]:
        print(name, "=>", classify(image))

    print("\n4. MODALITIES")
    rng = np.random.default_rng(4)
    modalities = [gray, color, np.array(Image.fromarray(gray).filter(ImageFilter.GaussianBlur(2))), np.clip(gray + rng.normal(0, 22, gray.shape), 0, 255), np.stack([gray, gray // 2, gray // 5], axis=2)]
    names = ["X-ray", "Satellite", "Microscopy", "Ultrasound", "Infrared"]
    show(
        modalities,
        ["X-ray\n(synthetic)", "Satellite\n(synthetic)", "Microscopy\n(blurred)", "Ultrasound\n(noisy)", "Infrared\n(channel mix)"],
        "02_modalities.png",
        3,
        "Image Modalities",
        "These are illustrative transformations of the input grayscale image, not separate input files.",
    )
    for name in names:
        print(name, "sample created")

    print("\n5. THRESHOLDING")
    show(
        [np.where(gray >= t, 255, 0) for t in [64, 128, 192]],
        [f"Threshold = {t}" for t in [64, 128, 192]],
        "03_thresholds.png",
        heading="Thresholding",
        description="Pixels greater than or equal to the threshold become white; the remaining pixels become black.",
    )

    print("\n6. SPATIAL RESOLUTION")
    reduced = [np.array(Image.fromarray(gray).resize((size, size), Image.Resampling.NEAREST)) for size in [128, 64, 32, 16]]
    show(
        reduced,
        ["128 x 128", "64 x 64", "32 x 32", "16 x 16"],
        "04_resolution.png",
        2,
        "Spatial Resolution",
        "The image size decreases from left to right, so pixels become larger and fine details disappear.",
    )
    print("Lower resolution creates larger blocks and loss of detail.")

    print("\n7. FALSE CONTOURING")
    def reduce_levels(levels):
        return (np.floor(gray / (256 / levels)) * (256 / levels)).astype(np.uint8)
    levels = [128, 64, 32, 16, 8, 4, 2]
    show(
        [reduce_levels(level) for level in levels],
        [f"{level} gray levels" for level in levels],
        "05_gray_levels.png",
        4,
        "False Contouring",
        "Reducing gray levels creates visible bands instead of a smooth intensity gradient.",
    )
    print("Fewer gray levels create visible bands.")

    print("\n8. INTERPOLATION")
    small = np.array(Image.fromarray(gray).resize((64, 64)))
    methods = [("Nearest", Image.Resampling.NEAREST), ("Bilinear", Image.Resampling.BILINEAR), ("Bicubic", Image.Resampling.BICUBIC)]
    show(
        [np.array(Image.fromarray(small).resize((256, 256), method)) for _, method in methods],
        [f"{name} interpolation" for name, _ in methods],
        "06_interpolation.png",
        heading="Interpolation",
        description="The same 64 x 64 image is enlarged using three resampling methods.",
    )

    print("\n9. HISTOGRAMS")
    histogram_inputs = [
        ("dark", gray * 0.35, "Dark image histogram", "Most pixels move toward lower intensity values."),
        ("bright", np.clip(gray * 0.65 + 90, 0, 255), "Bright image histogram", "Most pixels move toward higher intensity values."),
        ("low_contrast", gray * 0.18 + 95, "Low-contrast image histogram", "Pixel values are concentrated in a narrow intensity range."),
    ]
    for name, image, title, description in histogram_inputs:
        save_histogram(image, name, title, description)
        print(name, "histogram created")

    print("\n10. NEIGHBORS AND DISTANCES")
    for point in [(128, 128), (0, 128), (0, 0)]: print(point, neighbors(*point, gray.shape[1], gray.shape[0]))
    print("(1,2) to (4,6): Euclidean, D4, D8 =", distances((1, 2), (4, 6)))
    print("(0,0) to (3,4): Euclidean, D4, D8 =", distances((0, 0), (3, 4)))

    print("\n11. ARITHMETIC AND CHANGE DETECTION")
    second = gray.copy()
    second[105:145, 105:145] = 255
    first_float = gray.astype(float)
    second_float = second.astype(float)
    arithmetic_results = [
        np.clip(first_float + second_float, 0, 255),
        np.abs(first_float - second_float),
        np.clip(first_float * second_float / 255, 0, 255),
        np.clip(first_float / np.maximum(second_float, 1) * 255, 0, 255),
    ]
    show(
        arithmetic_results,
        ["Addition\n(clipped at 255)", "Subtraction\n(change map)", "Multiplication", "Division"],
        "07_arithmetic.png",
        2,
        "Arithmetic Operations and Change Detection",
        "The second image contains a bright 40 x 40 changed region. The subtraction panel makes that change visible.",
    )

    print("\n12. NOISE AVERAGING")
    noisy = [np.clip(gray + rng.normal(0, 25, gray.shape), 0, 255) for _ in range(20)]
    show(
        [noisy[0], np.mean(noisy, axis=0)],
        ["Input: one noisy image", "Output: average of 20"],
        "08_noise.png",
        2,
        "Noise Averaging",
        "Averaging independent noisy copies reduces random noise while preserving the underlying image.",
    )

    print("\n13. LOGICAL OPERATIONS")
    circle = Image.new("L", (256, 256), 0); ImageDraw.Draw(circle).ellipse((35, 60, 155, 180), fill=255)
    square = Image.new("L", (256, 256), 0); ImageDraw.Draw(square).rectangle((105, 85, 220, 200), fill=255)
    a, b = np.array(circle), np.array(square)
    show(
        [a & b, a | b, 255 - a, a ^ b],
        ["AND\n(overlap)", "OR\n(union)", "NOT A\n(inverse circle)", "XOR\n(non-overlap)"],
        "09_logic.png",
        2,
        "Logical Operations",
        "Binary circle A and square B are combined pixel by pixel using Boolean logic.",
    )

    print("\n14. GEOMETRIC TRANSFORMATIONS")
    original = Image.fromarray(gray); moved = Image.new("L", original.size, 0); moved.paste(original, (25, 15))
    show(
        [gray, np.array(moved), np.array(original.rotate(25, fillcolor=0)), np.array(original.resize((int(gray.shape[1] * 1.35), int(gray.shape[0] * 1.35))))],
        ["Input: original", "Translation\n(+25, +15 pixels)", "Rotation\n(+25 degrees)", "Scaling\n(1.35 x)"],
        "10_geometry.png",
        2,
        "Geometric Transformations",
        "Translation shifts position, rotation changes angle, and scaling changes size. Black areas contain no source pixels.",
    )
    print("Complete. See the outputs folder.")


if __name__ == "__main__":
    main()
