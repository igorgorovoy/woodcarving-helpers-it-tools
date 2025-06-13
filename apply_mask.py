#!/usr/bin/env python3
"""
Script to apply a manually edited alpha mask to the original image.
"""

import argparse
import os
from PIL import Image

def apply_mask(image_path, mask_path, output_path=None):
    """
    Applies a mask (grayscale or 1-channel PNG) as alpha channel to the original image.
    Args:
        image_path (str): Path to the original image
        mask_path (str): Path to the mask image (should be same size)
        output_path (str): Path to save the result (optional)
    """
    if not os.path.exists(image_path):
        print(f"Error: File {image_path} not found!")
        return False
    if not os.path.exists(mask_path):
        print(f"Error: File {mask_path} not found!")
        return False
    try:
        img = Image.open(image_path).convert('RGBA')
        mask = Image.open(mask_path).convert('L')
        if img.size != mask.size:
            print(f"Error: Image and mask sizes do not match! {img.size} vs {mask.size}")
            return False
        img.putalpha(mask)
        if output_path is None:
            base = os.path.splitext(image_path)[0]
            output_path = f"{base}_masked.png"
        img.save(output_path)
        print(f"✅ Mask applied and saved as: {output_path}")
        return True
    except Exception as e:
        print(f"❌ Error during processing: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Apply alpha mask to original image.")
    parser.add_argument("image_path", help="Path to the original image (JPG, PNG, etc.)")
    parser.add_argument("mask_path", help="Path to the mask image (PNG, grayscale or 1-channel)")
    parser.add_argument("-o", "--output", help="Path to save the result (optional)")
    args = parser.parse_args()
    print("="*60)
    print("🖤 Applying mask to image")
    print("="*60)
    apply_mask(args.image_path, args.mask_path, args.output)

if __name__ == "__main__":
    main() 