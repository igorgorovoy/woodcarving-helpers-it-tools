#!/usr/bin/env python3
"""
Script to scale an image to specified physical size, split it into A4 pages, and generate a printable PDF poster template.
"""

import argparse
import math
import os
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

def mm_to_px(mm, dpi):
    return int((mm / 25.4) * dpi)

def cm_to_px(cm_val, dpi):
    return int((cm_val / 2.54) * dpi)

def split_image_to_pages(image, target_width_cm, target_height_cm, dpi=300):
    # Розрахунок цільових розмірів у пікселях
    target_width_px = cm_to_px(target_width_cm, dpi)
    target_height_px = cm_to_px(target_height_cm, dpi)

    # Масштабуємо зображення з збереженням пропорцій
    img_ratio = image.width / image.height
    target_ratio = target_width_px / target_height_px
    if img_ratio > target_ratio:
        # Зображення ширше — підганяємо по ширині
        new_width = target_width_px
        new_height = int(target_width_px / img_ratio)
    else:
        # Зображення вище — підганяємо по висоті
        new_height = target_height_px
        new_width = int(target_height_px * img_ratio)
    scaled_img = image.resize((new_width, new_height), Image.LANCZOS)

    # Створюємо білий фон потрібного розміру
    background = Image.new('RGBA' if image.mode in ('RGBA', 'LA', 'P') else 'RGB', (target_width_px, target_height_px), (255, 255, 255, 0) if image.mode in ('RGBA', 'LA', 'P') else (255, 255, 255))
    # Центруємо зображення
    offset_x = (target_width_px - new_width) // 2
    offset_y = (target_height_px - new_height) // 2
    background.paste(scaled_img, (offset_x, offset_y), scaled_img if scaled_img.mode in ('RGBA', 'LA') else None)

    # Далі як раніше: ріжемо на сторінки
    a4_width_px = cm_to_px(21.0, dpi)
    a4_height_px = cm_to_px(29.7, dpi)
    pages_x = math.ceil(target_width_px / a4_width_px)
    pages_y = math.ceil(target_height_px / a4_height_px)
    pages = []
    for y in range(pages_y):
        for x in range(pages_x):
            left = x * a4_width_px
            upper = y * a4_height_px
            right = min(left + a4_width_px, target_width_px)
            lower = min(upper + a4_height_px, target_height_px)
            crop = background.crop((left, upper, right, lower))
            pages.append(crop)
    return pages, pages_x, pages_y

def save_pages_to_pdf(pages, output_path, pages_x, pages_y, dpi=300):
    c = canvas.Canvas(output_path, pagesize=A4)
    a4_width_pt, a4_height_pt = A4
    for idx, img in enumerate(pages):
        # Зберігаємо crop у тимчасовий файл
        temp_path = f"temp_page_{idx}.jpg"
        # Convert to RGB and handle transparency (white background)
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[-1])
            img_rgb = background
        else:
            img_rgb = img.convert('RGB')
        img_rgb.save(temp_path, 'JPEG', quality=95)
        # Вставляємо на сторінку PDF
        c.drawImage(temp_path, 0, 0, width=a4_width_pt, height=a4_height_pt)
        # (Опціонально) Додаємо мітки для склеювання
        c.setStrokeColorRGB(0, 0, 0)
        c.setLineWidth(0.5)
        c.line(0, 0, 20, 0)  # Нижній лівий кут
        c.line(0, 0, 0, 20)
        c.line(a4_width_pt, 0, a4_width_pt-20, 0)
        c.line(a4_width_pt, 0, a4_width_pt, 20)
        c.line(0, a4_height_pt, 20, a4_height_pt)
        c.line(0, a4_height_pt, 0, a4_height_pt-20)
        c.line(a4_width_pt, a4_height_pt, a4_width_pt-20, a4_height_pt)
        c.line(a4_width_pt, a4_height_pt, a4_width_pt, a4_height_pt-20)
        # Додаємо координати сторінки у лівий верхній кут
        row = (idx // pages_x) + 1
        col = (idx % pages_x) + 1
        label = f"Row {row}, Col {col}"
        c.setFont("Helvetica", 12)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(20, a4_height_pt - 25, label)
        c.showPage()
        os.remove(temp_path)
    c.save()

def main():
    parser = argparse.ArgumentParser(description="Scale image to physical size, split into A4 pages, and generate PDF poster template.")
    parser.add_argument("image_path", help="Path to input image (JPG, PNG, etc.)")
    parser.add_argument("-w", "--width", type=float, required=True, help="Target width in cm")
    parser.add_argument("-t", "--height", type=float, required=True, help="Target height in cm")
    parser.add_argument("-o", "--output", help="Output PDF file (default: <image>_poster.pdf)")
    parser.add_argument("--dpi", type=int, default=300, help="DPI for scaling (default: 300)")
    args = parser.parse_args()

    if not os.path.exists(args.image_path):
        print(f"Error: File {args.image_path} not found!")
        return
    img = Image.open(args.image_path)
    print(f"Original image size: {img.size[0]} x {img.size[1]} px")
    print(f"Scaling to: {args.width} x {args.height} cm at {args.dpi} DPI")
    pages, pages_x, pages_y = split_image_to_pages(img, args.width, args.height, args.dpi)
    print(f"Pages needed: {pages_x} x {pages_y} = {len(pages)} sheets of A4")
    output_pdf = args.output if args.output else f"{os.path.splitext(args.image_path)[0]}_poster.pdf"
    save_pages_to_pdf(pages, output_pdf, pages_x, pages_y, args.dpi)
    print(f"✅ PDF poster saved as: {output_pdf}")
    print(f"Each page is A4 size. Print and assemble as a template!")

if __name__ == "__main__":
    main() 