# Real Wallpaper DIP Generator

This folder downloads one real public wallpaper automatically and runs the complete Digital Image Processing project on it.

## Run

From the workspace root:

```powershell
python main.py
```

The first run downloads and stores `real_wallpaper.jpg`. Every later run uses the cached image. To download a fresh wallpaper again:

```powershell
python main.py --refresh
```

## Results

- The downloaded real image is saved as `real_wallpaper.jpg`.
- All processed figures are saved in `outputs/`.
- By default, each figure opens one at a time. Close the current figure to see the next operation.
- The runner reuses the verified operations from `vscode_project/main.py`.
- No image upload or manual path is required.

To save all figures without opening them:

```powershell
python main.py --no-show
```

The source wallpaper is fetched from Unsplash's public image CDN at runtime. An internet connection is required for the first download or when using `--refresh`.
