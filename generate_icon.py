# generate_icon.py
"""
Generate a professional icon for Strava API application.
Run this script to create your app icon.
"""

from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_strava_analytics_icon(size=512, output_path="strava_app_icon.png"):
    """
    Create a professional icon for Strava Analytics app.
    
    Parameters:
    -----------
    size : int
        Icon size in pixels (512x512 recommended)
    output_path : str
        Where to save the icon
    """
    # Create image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Colors (Strava-inspired palette)
    strava_orange = (252, 76, 2)      # Strava's signature orange
    dark_gray = (34, 34, 34)          # Dark gray for contrast
    accent_blue = (43, 140, 255)      # Data analytics blue
    white = (255, 255, 255)
    
    # Draw rounded rectangle background
    corner_radius = size // 8
    draw.rounded_rectangle(
        [(0, 0), (size, size)],
        radius=corner_radius,
        fill=dark_gray
    )
    
    # Draw gradient-like overlay (simple approximation)
    for i in range(size):
        alpha = int(50 * (1 - i / size))
        overlay = Image.new('RGBA', (size, size), (strava_orange[0], strava_orange[1], strava_orange[2], alpha))
        img = Image.alpha_composite(img, overlay)
        draw = ImageDraw.Draw(img)
    
    # Draw central chart/activity symbol
    center = size // 2
    bar_width = size // 8
    bar_spacing = size // 16
    
    # Bar chart (analytics theme)
    heights = [size * 0.3, size * 0.6, size * 0.45, size * 0.75, size * 0.5]
    colors = [accent_blue, strava_orange, accent_blue, strava_orange, accent_blue]
    
    for i, (height, color) in enumerate(zip(heights, colors)):
        x0 = center - (len(heights) * bar_width + (len(heights)-1) * bar_spacing) // 2 + i * (bar_width + bar_spacing)
        y0 = size - int(height)
        x1 = x0 + bar_width
        y1 = size
        draw.rectangle([(x0, y0), (x1, y1)], fill=color, outline=None)
    
    # Draw runner/activity silhouette (simplified)
    runner_color = white
    
    # Head (circle)
    head_radius = size // 16
    head_center = (center, int(size * 0.35))
    draw.ellipse(
        [(head_center[0] - head_radius, head_center[1] - head_radius),
         (head_center[0] + head_radius, head_center[1] + head_radius)],
        fill=runner_color
    )
    
    # Body (line)
    body_start = (center, int(size * 0.42))
    body_end = (center, int(size * 0.58))
    draw.line([body_start, body_end], fill=runner_color, width=size // 32)
    
    # Arms (angled lines for running motion)
    left_arm_start = (center, int(size * 0.48))
    left_arm_end = (int(center - size * 0.12), int(size * 0.52))
    right_arm_start = (center, int(size * 0.48))
    right_arm_end = (int(center + size * 0.12), int(size * 0.52))
    draw.line([left_arm_start, left_arm_end], fill=runner_color, width=size // 32)
    draw.line([right_arm_start, right_arm_end], fill=runner_color, width=size // 32)
    
    # Legs (running stride)
    left_leg_start = (center, int(size * 0.58))
    left_leg_end = (int(center - size * 0.1), int(size * 0.68))
    right_leg_start = (center, int(size * 0.58))
    right_leg_end = (int(center + size * 0.1), int(size * 0.68))
    draw.line([left_leg_start, left_leg_end], fill=runner_color, width=size // 32)
    draw.line([right_leg_start, right_leg_end], fill=runner_color, width=size // 32)
    
    # Add "SEA" text (Strava Elite Analytics)
    try:
        # Try to use a bold font
        font = ImageFont.truetype("arial.ttf", size // 10)
    except:
        font = ImageFont.load_default()
    
    text = "SEA"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (size - text_width) // 2
    text_y = int(size * 0.85)
    draw.text((text_x, text_y), text, fill=strava_orange, font=font)
    
    # Save the icon
    img.save(output_path, "PNG")
    print(f"✅ Icon saved to {output_path}")
    print(f"📏 Size: {size}x{size} pixels")
    
    return img

def create_simple_icon(size=512, output_path="strava_app_icon.png"):
    """
    Create a simpler icon (if the complex one fails).
    """
    img = Image.new('RGBA', (size, size), (252, 76, 2))
    draw = ImageDraw.Draw(img)
    
    # White rounded rectangle inner
    margin = size // 10
    draw.rounded_rectangle(
        [(margin, margin), (size - margin, size - margin)],
        radius=size // 8,
        fill=(255, 255, 255)
    )
    
    # Orange accent line
    line_width = size // 20
    line_y = size // 2
    draw.line(
        [(margin * 2, line_y), (size - margin * 2, line_y)],
        fill=(252, 76, 2),
        width=line_width
    )
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", size // 6)
    except:
        font = ImageFont.load_default()
    
    text = "SEA"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_x = (size - text_width) // 2
    text_y = size // 3
    draw.text((text_x, text_y), text, fill=(252, 76, 2), font=font)
    
    img.save(output_path, "PNG")
    print(f"✅ Simple icon saved to {output_path}")
    
    return img

if __name__ == "__main__":
    # Install required library if needed
    # pip install Pillow
    
    try:
        img = create_strava_analytics_icon(512, "strava_app_icon.png")
        print("\n📸 Icon created successfully!")
        print("Upload this file to your Strava API application settings.")
    except Exception as e:
        print(f"Error creating complex icon: {e}")
        print("Creating simple icon instead...")
        create_simple_icon(512, "strava_app_icon.png")