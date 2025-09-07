from PIL import Image
import os
from pathlib import Path

def process_image(image_path, output_dir, target_width=1280, target_height=720, target_dpi=72):
    """
    Process an image with the following specifications:
    - Resize to 1280x720 (16:9 ratio)
    - Set DPI to 72
    - Optimize for web
    
    Args:
        image_path (str): Path to the input image
        output_dir (str): Directory to save processed images
        target_width (int): Target width in pixels
        target_height (int): Target height in pixels
        target_dpi (int): Target DPI (dots per inch)
    """
    try:
        # Open the image
        with Image.open(image_path) as img:
            # Convert to RGB if needed
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Calculate aspect ratio
            aspect_ratio = target_width / target_height
            
            # Calculate dimensions for resizing
            img_width, img_height = img.size
            current_aspect_ratio = img_width / img_height
            
            if current_aspect_ratio > aspect_ratio:
                # Image is wider than target ratio
                new_width = target_width
                new_height = int(target_width / current_aspect_ratio)
            else:
                # Image is taller than target ratio
                new_height = target_height
                new_width = int(target_height * current_aspect_ratio)
            
            # Resize image
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Create a new blank image with target dimensions
            new_img = Image.new('RGB', (target_width, target_height), 'white')
            
            # Paste the resized image in the center
            paste_x = (target_width - new_width) // 2
            paste_y = (target_height - new_height) // 2
            new_img.paste(img, (paste_x, paste_y))
            
            # Set DPI
            new_img.info['dpi'] = (target_dpi, target_dpi)
            
            # Create output filename
            input_filename = Path(image_path).name
            output_filename = f"processed_{input_filename}"
            output_path = os.path.join(output_dir, output_filename)
            
            # Save the processed image with optimization
            new_img.save(
                output_path,
                'JPEG' if input_filename.lower().endswith('.jpg') else 'PNG',
                quality=85,  # Good balance between quality and file size
                optimize=True,
                dpi=(target_dpi, target_dpi)
            )
            
            print(f"Successfully processed {input_filename} -> {output_filename}")
            
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")

def main():
    # Define paths
    base_dir = Path(__file__).parent.parent
    image_dir = base_dir / 'images'
    output_dir = base_dir / 'images' / 'processed'
    
    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)
    
    # List of project images to process
    project_images = [
        'sih.png',
        'personal_capsule.png',
        'dev_search.png',
        'RestAPI.jpg'
    ]
    
    # Process each image
    for image_name in project_images:
        image_path = image_dir / image_name
        if image_path.exists():
            process_image(str(image_path), str(output_dir))
        else:
            print(f"Image not found: {image_name}")

if __name__ == "__main__":
    main()
