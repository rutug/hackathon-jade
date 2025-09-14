"""
Image processing utilities for the Document Analysis Agent
"""

import os
import shutil
from typing import List, Dict
import base64
from PIL import Image, ImageFile
from utils.logger_util import logger

# Ensure PIL can handle truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True

def process_image_file(image_path: str, output_folder: str) -> List[str]:
    """
    Process an image file (copy to output folder)
    
    Args:
        image_path: Path to the image file
        output_folder: Directory to save the processed image
        
    Returns:
        List containing the path to the processed image
    """
    logger.info(f"Processing image file: {image_path}")
    
    # Ensure output directory exists
    os.makedirs(output_folder, exist_ok=True)
    logger.debug(f"Ensured output directory exists: {output_folder}")
    
    # Get base filename
    base_filename = os.path.basename(image_path)
    
    # Define output path
    output_path = os.path.join(output_folder, base_filename)
    
    try:
        # Copy the image
        shutil.copy2(image_path, output_path)
        logger.info(f"Successfully copied image to: {output_path}")
        return [output_path]
    except Exception as e:
        logger.error(f"Error copying image {image_path} to {output_path}: {str(e)}", exc_info=True)


def optimize_image_for_api(image_path: str, max_size_mb: float = 4.0) -> str:
    """
    Optimize an image for API submission by resizing if needed
    
    Args:
        image_path: Path to the image file
        max_size_mb: Maximum size in MB
        
    Returns:
        Path to the optimized image (same as input if no changes made)
    """
    logger.debug(f"Checking if image needs optimization: {image_path}")
    
    # Check current file size
    file_size_mb = os.path.getsize(image_path) / (1024 * 1024)
    
    if file_size_mb <= max_size_mb:
        logger.debug(f"Image already within size limit ({file_size_mb:.2f}MB <= {max_size_mb}MB): {image_path}")
        return image_path
    
    # Need to resize
    logger.info(f"Image exceeds size limit ({file_size_mb:.2f}MB > {max_size_mb}MB), optimizing: {image_path}")
    
    try:
        img = Image.open(image_path)
        
        # Log original dimensions
        logger.debug(f"Original image dimensions: {img.width}x{img.height}, format: {img.format}")
        
        # Calculate new size to roughly meet the target file size
        # This is approximate and may need multiple passes for precision
        scale_factor = (max_size_mb / file_size_mb) ** 0.5
        new_width = int(img.width * scale_factor)
        new_height = int(img.height * scale_factor)
        
        logger.debug(f"Resizing image to {new_width}x{new_height} (scale factor: {scale_factor:.2f})")
        
        # Resize the image
        resized_img = img.resize((new_width, new_height), Image.LANCZOS)
        
        # Create a new filename
        filename, ext = os.path.splitext(image_path)
        optimized_path = f"{filename}_optimized{ext}"
        
        # Save with reduced quality for JPEGs
        if ext.lower() in ['.jpg', '.jpeg']:
            resized_img.save(optimized_path, quality=85, optimize=True)
            logger.debug(f"Saved optimized JPEG with 85% quality: {optimized_path}")
        else:
            resized_img.save(optimized_path, optimize=True)
            logger.debug(f"Saved optimized image: {optimized_path}")
        
        # Log new size
        new_size_mb = os.path.getsize(optimized_path) / (1024 * 1024)
        logger.info(f"Optimized image size: {new_size_mb:.2f}MB (reduced from {file_size_mb:.2f}MB)")
        
        return optimized_path
    
    except Exception as e:
        logger.error(f"Error optimizing image {image_path}: {str(e)}", exc_info=True)
        logger.warning(f"Using original unoptimized image: {image_path}")
        return image_path


def encode_image_to_base64(image_path: str) -> str:
    """
    Encode an image file to base64 string
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Base64 encoded string
    """
    logger.debug(f"Encoding image to base64: {image_path}")
    
    try:
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode('utf-8')
            logger.debug(f"Successfully encoded image, base64 length: {len(encoded)}")
            return encoded
    except Exception as e:
        logger.error(f"Error encoding image {image_path} to base64: {str(e)}", exc_info=True)
        raise


def get_image_dimensions(image_path: str) -> tuple:
    """
    Get the dimensions of an image
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Tuple of (width, height)
    """
    logger.debug(f"Getting image dimensions: {image_path}")
    
    try:
        with Image.open(image_path) as img:
            dimensions = img.size
            logger.debug(f"Image dimensions: {dimensions[0]}x{dimensions[1]}")
            return dimensions
    except Exception as e:
        logger.error(f"Error getting image dimensions for {image_path}: {str(e)}", exc_info=True)
        raise