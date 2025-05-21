import os
import base64
from PIL import Image
from io import BytesIO
from typing import List, Dict, Generator, Tuple


class ImageManager:
    """
    A class to manage image processing operations for Adobe Stock images.
    
    Attributes:
        VALID_IMAGE_EXTENSIONS (tuple): Supported image file extensions
        DEFAULT_IMAGE_SIZE (tuple): Default size for image resizing
        DEFAULT_MAX_IMAGES (int): Default maximum number of images per batch
    """
    
    VALID_IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp')
    DEFAULT_IMAGE_SIZE = (512, 512)
    DEFAULT_MAX_IMAGES = 5

    @classmethod
    def list_images(cls, folder_path: str) -> List[str]:
        """
        List all valid images in the specified folder.
        
        Args:
            folder_path (str): Path to the folder containing images
            
        Returns:
            List[str]: List of valid image filenames
        """
        return [
            f for f in os.listdir(folder_path)
            if f.lower().endswith(cls.VALID_IMAGE_EXTENSIONS)
        ]

    @classmethod
    def open_and_resize_image(cls, image_path: str, size: Tuple[int, int] = DEFAULT_IMAGE_SIZE) -> str:
        """
        Open, resize, and convert an image to base64 string.
        
        Args:
            image_path (str): Path to the image file
            size (tuple): Target size for the image (width, height)
            
        Returns:
            str: Base64 encoded string of the processed image
            
        Raises:
            PIL.UnidentifiedImageError: If the image format is not supported
            FileNotFoundError: If the image file doesn't exist
        """
        with Image.open(image_path) as img:
            img = img.convert("RGB")  # Ensure consistent format
            img = img.resize(size)
            buffer = BytesIO()
            img.save(buffer, format="JPEG")  # Save to buffer
            base64_img = base64.b64encode(buffer.getvalue()).decode("utf-8")
            return base64_img

    @classmethod
    def prepare_image_batches(
        cls,
        file_list: str,
        max_images: int = DEFAULT_MAX_IMAGES,
        size: Tuple[int, int] = DEFAULT_IMAGE_SIZE
    ) -> Generator[List[Dict[str, str]], None, None]:
        """
        Process images in a folder and yield them in batches.
        
        Args:
            folder_path (str): Path to the folder containing images
            max_images (int): Maximum number of images per batch
            size (tuple): Target size for the images (width, height)
            
        Yields:
            List[Dict[str, str]]: Batch of processed images with their filenames
        """
        image_filenames = [
            f for f in file_list
            if f.lower().endswith(cls.VALID_IMAGE_EXTENSIONS)
        ]
        batch = []
        
        for filename in image_filenames:
            full_path = os.path.join(filename)
            try:
                image_b64 = cls.open_and_resize_image(full_path, size=size)
                batch.append({
                    "filename": filename,
                    "image_b64": image_b64
                })
            except Exception as e:
                print(f"Failed to process {filename}: {e}")
            
            if len(batch) == max_images:
                yield batch
                batch = []

        # Yield remaining images
        if batch:
            yield batch

    @classmethod
    def process_single_image(
        cls,
        image_path: str,
        size: Tuple[int, int] = DEFAULT_IMAGE_SIZE
    ) -> Dict[str, str]:
        """
        Process a single image file.
        
        Args:
            image_path (str): Path to the image file
            size (tuple): Target size for the image (width, height)
            
        Returns:
            Dict[str, str]: Processed image data with filename and base64 content
        """
        image_b64 = cls.open_and_resize_image(image_path, size=size)
        return {
            "filename": os.path.basename(image_path),
            "image_b64": image_b64
        }