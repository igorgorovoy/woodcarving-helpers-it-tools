#!/usr/bin/env python3
"""
Script for removing background from images.
Uses the rembg library for automatic background removal.
"""

import argparse
import sys
import os
from rembg import remove
from PIL import Image
import io

def remove_background_from_image(input_path, output_path=None, alpha_matting=False, alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=10, alpha_matting_erode_size=10):
    """
    Removes background from an image.
    
    Args:
        input_path (str): Path to input image
        output_path (str): Path to output file (optional)
        alpha_matting (bool): Use alpha matting for better quality
        alpha_matting_foreground_threshold (int): Foreground threshold
        alpha_matting_background_threshold (int): Background threshold
        alpha_matting_erode_size (int): Erode size
    """
    
    # Check if file exists
    if not os.path.exists(input_path):
        print(f"Error: File {input_path} not found!")
        return False
    
    try:
        # Open image
        with open(input_path, 'rb') as input_file:
            input_data = input_file.read()
        
        print(f"Processing image: {input_path}")
        
        # Remove background
        if alpha_matting:
            print("Using alpha matting for better quality...")
            output_data = remove(
                input_data,
                alpha_matting=True,
                alpha_matting_foreground_threshold=alpha_matting_foreground_threshold,
                alpha_matting_background_threshold=alpha_matting_background_threshold,
                alpha_matting_erode_size=alpha_matting_erode_size
            )
        else:
            print("Using standard background removal...")
            output_data = remove(input_data)
        
        # Determine output file
        if output_path is None:
            base_name = os.path.splitext(input_path)[0]
            output_path = f"{base_name}_no_bg.png"
        
        # Save result
        with open(output_path, 'wb') as output_file:
            output_file.write(output_data)
        
        # Show result information
        result_image = Image.open(io.BytesIO(output_data))
        print(f"✅ Background successfully removed!")
        print(f"📁 Result saved: {output_path}")
        print(f"📏 Result size: {result_image.size[0]} x {result_image.size[1]} pixels")
        print(f"🎨 Format: PNG with transparent background")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during processing: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Removes background from image using artificial intelligence"
    )
    parser.add_argument(
        "image_path", 
        help="Path to image (supports JPG, PNG, TIFF, BMP, etc.)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to output file (default: adds '_no_bg.png')"
    )
    parser.add_argument(
        "-a", "--alpha-matting",
        action="store_true",
        help="Use alpha matting for better quality (slower but better)"
    )
    parser.add_argument(
        "--foreground-threshold",
        type=int,
        default=240,
        help="Foreground threshold for alpha matting (default: 240)"
    )
    parser.add_argument(
        "--background-threshold",
        type=int,
        default=10,
        help="Background threshold for alpha matting (default: 10)"
    )
    parser.add_argument(
        "--erode-size",
        type=int,
        default=10,
        help="Erode size for alpha matting (default: 10)"
    )
    parser.add_argument(
        "--save-mask",
        action="store_true",
        help="Save alpha mask as a separate PNG file for manual editing"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🖼️  Background Removal from Image")
    print("=" * 60)
    
    success = remove_background_from_image(
        input_path=args.image_path,
        output_path=args.output,
        alpha_matting=args.alpha_matting,
        alpha_matting_foreground_threshold=args.foreground_threshold,
        alpha_matting_background_threshold=args.background_threshold,
        alpha_matting_erode_size=args.erode_size
    )
    
    # Save mask if requested
    if success and args.save_mask:
        try:
            with open(args.output if args.output else f"{os.path.splitext(args.image_path)[0]}_no_bg.png", 'rb') as f:
                img = Image.open(f).convert('RGBA')
                alpha = img.split()[-1]
                mask_path = (args.output if args.output else f"{os.path.splitext(args.image_path)[0]}_no_bg.png").replace('.png', '_mask.png')
                alpha.save(mask_path)
                print(f"🖤 Alpha mask saved as: {mask_path}")
        except Exception as e:
            print(f"⚠️ Could not save mask: {e}")
    
    if success:
        print("\n🎉 Processing completed successfully!")
        print("💡 Tip: Result is saved in PNG format with transparent background")
    else:
        print("\n💥 An error occurred during processing!")
        sys.exit(1)

if __name__ == "__main__":
    main() 