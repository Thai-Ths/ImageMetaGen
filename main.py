import asyncio
import os
from typing import List, Tuple
from metadata_agent import MetadataAgent
from embedded import embed_metadata
from image_manager import ImageManager
import csv
from agents import trace
from dotenv import load_dotenv, set_key, find_dotenv

class ProcessingConfig:
    """Configuration settings for image processing"""
    MAX_TITLE_LENGTH = 70
    MAX_KEYWORDS = 45
    BATCH_SIZE = 3
    IMAGE_SIZE = (512, 512)
    MODEL_NAME = "gpt-4o-mini"
    use_filename = False

load_dotenv()
ENV_PATH = find_dotenv() or ".env"

def save_metadata_to_csv(metadata_list, csv_path):
    """
    Save a list of metadata objects (with .filename, .title, .keywords) to a CSV file.
    Args:
        metadata_list (list): List of metadata objects (Pydantic models or dicts).
        csv_path (str): Path to save the CSV file.
    """
    with open(csv_path, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['Filename', 'Title', 'Keywords'])
        writer.writeheader()
        for item in metadata_list:
            # Support both dict and Pydantic model
            if hasattr(item, 'dict'):
                item_dict = item.dict()
            elif hasattr(item, 'final_output') and hasattr(item.final_output, 'dict'):
                item_dict = item.final_output.dict()
            else:
                item_dict = dict(item)
            writer.writerow({
                'Filename': os.path.basename(item_dict['filename']),
                'Title': item_dict['title'],
                'Keywords': ', '.join(item_dict['keywords']) if isinstance(item_dict['keywords'], list) else item_dict['keywords']
            }) 

async def process_images(
    file_list: str,
    api_key: str = None,
    max_title_length: int = ProcessingConfig.MAX_TITLE_LENGTH,
    max_keywords: int = ProcessingConfig.MAX_KEYWORDS,
    use_filename: bool = False,
    csv_output: str = "Adobe_stock.csv"
) -> Tuple[List[Tuple[str, str]], str]:
    """
    Main function to process images: generate metadata and embed it.
    """
    print("Start Generate")

    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        # Save or update .env file
        set_key(ENV_PATH, "OPENAI_API_KEY", api_key)
    else:
        # Load from environment if no key provided
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("API Key is required but not found in environment or input")

    agent = MetadataAgent(max_title_length=max_title_length, max_keywords=max_keywords)

    # output_folder = output_folder or input_folder
    # os.makedirs(output_folder, exist_ok=True)

    all_metadata = []

    for batch in ImageManager.prepare_image_batches(
        file_list,
        max_images=ProcessingConfig.BATCH_SIZE,
        size=ProcessingConfig.IMAGE_SIZE
    ):
        tasks = [
            asyncio.create_task(agent.process_image(**item, use_filename=use_filename))
            for item in batch
        ]
        with trace("Generate Metadata"):
            batch_results = await asyncio.gather(*tasks)
        valid_results = [r for r in batch_results if r is not None]
        all_metadata.extend(valid_results)
        print(f"Processed batch of {len(valid_results)} images")

    gallery_items = []
    if all_metadata:
        save_metadata_to_csv(all_metadata, csv_output)
        print(f"Metadata saved to {csv_output}")

        print("\nEmbedding metadata into images...")
        for data in all_metadata:
            meta = data.final_output
            image_path = meta.filename
            embed_metadata(image_path, meta.title, meta.keywords)
            gallery_items.append((image_path, meta.title))

        print(f"Successfully processed {len(all_metadata)} images")
    else:
        print("No images were successfully processed")

    return gallery_items, csv_output

