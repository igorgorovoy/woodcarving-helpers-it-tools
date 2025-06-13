# Background Removal from Images

This script automatically removes background from images using artificial intelligence. Uses the `rembg` library for high-quality background removal.

## Installation

1. Make sure you have Python 3.7+ installed
2. Install required dependencies:

```bash
pip install rembg Pillow
```

or update `requirements.txt`:

```bash
echo "rembg" >> requirements.txt
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python remove_background.py image.jpg
```

### With Additional Parameters
```bash
# Specify output filename
python remove_background.py image.jpg -o result.png

# Use alpha matting for better quality
python remove_background.py image.jpg -a

# Combine parameters
python remove_background.py image.jpg -o result.png -a
```

### Advanced Alpha Matting Settings
```bash
python remove_background.py image.jpg -a \
    --foreground-threshold 250 \
    --background-threshold 5 \
    --erode-size 15
```

### Parameters

- `image_path` - path to image (required)
- `-o, --output` - output filename (default: adds '_no_bg.png')
- `-a, --alpha-matting` - use alpha matting for better quality
- `--foreground-threshold` - foreground threshold (default: 240)
- `--background-threshold` - background threshold (default: 10)
- `--erode-size` - erode size (default: 10)

## Supported Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- TIFF (.tiff, .tif)
- BMP (.bmp)
- and other formats supported by Pillow library

## Features

- **Automatic background removal** using artificial intelligence
- **Alpha matting** for better quality edge processing
- **PNG saving** with transparent background
- **Parameter tuning** for different image types
- **Fast processing** for simple cases

## Operation Modes

### Standard Mode
- Fast processing
- Good quality for most images
- Automatic object detection

### Alpha Matting Mode
- Slower processing
- Better quality for complex edges
- Parameter tuning for precise control

## Usage Examples

### For Wood Carving
```bash
# Remove background from carving photo
python remove_background.py carving.jpg -o carving_clean.png

# Use alpha matting for high quality
python remove_background.py carving.jpg -a -o carving_high_quality.png
```

### For Logos and Illustrations
```bash
# Quick background removal
python remove_background.py logo.png

# High quality for complex details
python remove_background.py logo.png -a --foreground-threshold 255
```

## Tips

1. **For simple objects** use standard mode
2. **For complex edges** (hair, fur, transparency) use alpha matting
3. **Result is always saved in PNG** to support transparency
4. **Experiment with alpha matting parameters** for best results

## System Requirements

- Python 3.7+
- Minimum 2GB RAM
- Internet connection for first run (model download)

## 🖤 Manual Alpha Mask Editing

1. Run background removal with the `--save-mask` option:
   ```bash
   python remove_background.py your_image.jpg -a --save-mask
   ```
2. Open the mask (`your_image_no_bg_mask.png`) in a graphics editor, fix details, and save.
3. Apply the mask to the original image:
   ```bash
   python apply_mask.py your_image.jpg your_image_no_bg_mask.png -o your_image_final.png
   ```

**The `apply_mask.py` script is included in the project!** 