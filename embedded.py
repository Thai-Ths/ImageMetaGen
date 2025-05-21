from PIL import Image, PngImagePlugin, JpegImagePlugin
import piexif
import os

def embed_metadata(image_path: str, title: str, keywords: list[str], output_path: str = None):
    ext = os.path.splitext(image_path)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png']:
        raise ValueError("Only .jpg, .jpeg, and .png formats are supported.")

    output_path = output_path or image_path  # overwrite by default
    keywords_str = ", ".join(keywords)

    if ext in ['.jpg', '.jpeg']:
        _embed_jpeg_metadata(image_path, title, keywords_str, output_path)
    elif ext == '.png':
        _embed_png_metadata(image_path, title, keywords_str, output_path)

def _embed_jpeg_metadata(image_path: str, title: str, keywords: str, output_path: str):
    image = Image.open(image_path)

    exif_dict = piexif.load(image.info.get('exif', b""))

    # Set title and keywords in the ImageDescription and XPKeywords
    exif_dict['0th'][piexif.ImageIFD.ImageDescription] = title.encode('utf-8')
    exif_dict['0th'][piexif.ImageIFD.XPKeywords] = keywords.encode('utf-16le')  # XPKeywords expects UTF-16LE

    exif_bytes = piexif.dump(exif_dict)
    image.save(output_path, format="jpeg", exif=exif_bytes)
    print(f"Metadata embedded in: {image_path} embedded succeed")

def _embed_png_metadata(image_path: str, title: str, keywords: str, output_path: str):
    image = Image.open(image_path)

    meta = PngImagePlugin.PngInfo()
    meta.add_text("Title", title)
    meta.add_text("Keywords", keywords)

    image.save(output_path, pnginfo=meta)
    print(f"Metadata embedded in: {image_path} embedded succeed")