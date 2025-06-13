#!/usr/bin/env python3
"""
Script for converting images to PDF with exact print size of 14 cm.
"""

import argparse
import sys
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.pagesizes import A4

def convert_image_to_pdf(image_path, output_path=None, target_size_cm=14):
    """
    Converts image to PDF with specified print size.
    
    Args:
        image_path (str): Path to input image
        output_path (str): Path to output PDF file (optional)
        target_size_cm (float): Target size of largest side in cm
    """
    
    # Check if file exists
    if not os.path.exists(image_path):
        print(f"Error: File {image_path} not found!")
        return False
    
    try:
        # Open image
        image = Image.open(image_path)
        print(f"Opened image: {image_path}")
        print(f"Original size: {image.size[0]} x {image.size[1]} pixels")
        
        # Convert to RGB if needed, and handle transparency
        if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            # Create white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[-1])
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Determine output file
        if output_path is None:
            base_name = os.path.splitext(image_path)[0]
            output_path = f"{base_name}_{target_size_cm}cm.pdf"
        
        # Create PDF
        c = canvas.Canvas(output_path, pagesize=A4)
        
        # Calculate dimensions
        original_width, original_height = image.size
        aspect_ratio = original_width / original_height
        
        # Determine dimensions in cm, preserving proportions
        if original_width >= original_height:
            # Horizontal or square image
            width_cm = target_size_cm
            height_cm = target_size_cm / aspect_ratio
        else:
            # Vertical image
            height_cm = target_size_cm
            width_cm = target_size_cm * aspect_ratio
        
        # Convert cm to points for reportlab
        width_points = width_cm * cm
        height_points = height_cm * cm
        
        print(f"Size in PDF: {width_cm:.2f} x {height_cm:.2f} cm")
        
        # Center image on A4 page
        page_width, page_height = A4
        x = (page_width - width_points) / 2
        y = (page_height - height_points) / 2
        
        # Save image as temporary file for reportlab
        temp_image_path = "temp_image_for_pdf.jpg"
        image.save(temp_image_path, "JPEG", quality=95)
        
        # Add image to PDF
        c.drawImage(temp_image_path, x, y, width=width_points, height=height_points)
        
        # Save PDF
        c.save()
        
        # Remove temporary file
        os.remove(temp_image_path)
        
        print(f"PDF successfully created: {output_path}")
        print(f"Print size: {width_cm:.2f} x {height_cm:.2f} cm")
        
        return True
        
    except Exception as e:
        print(f"Error during processing: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Converts image to PDF with exact print size"
    )
    parser.add_argument(
        "image_path", 
        help="Path to image (supports JPG, PNG, TIFF, BMP, etc.)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Path to output PDF file (optional)"
    )
    parser.add_argument(
        "-s", "--size",
        type=float,
        default=14,
        help="Size of largest side in cm (default: 14)"
    )
    
    args = parser.parse_args()
    
    print("=" * 50)
    print("Image to PDF Converter")
    print("=" * 50)
    
    success = convert_image_to_pdf(
        image_path=args.image_path,
        output_path=args.output,
        target_size_cm=args.size
    )
    
    if success:
        print("\n✅ Conversion completed successfully!")
    else:
        print("\n❌ An error occurred during conversion!")
        sys.exit(1)

if __name__ == "__main__":
    main() 