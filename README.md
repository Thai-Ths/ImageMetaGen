# Metadata-Generate
![image](https://github.com/user-attachments/assets/60e79742-ce71-4f20-a9c6-8c8fe2e16dd9)

# 🏷️ Adobe Stock Metadata Generator

A Python-powered automation tool that generates SEO-optimized metadata (titles + keywords) for stock images using OpenAI's GPT models. It also embeds the generated metadata directly into image files and exports a summary to CSV.

---

## 📦 Features

* ✅ Auto-generates **SEO-friendly titles** and **visually relevant keywords**
* ✅ Uses **OpenAI GPT-4o-mini** for high-quality metadata
* ✅ Describe image title with filename
* ✅ Embeds metadata back into images using EXIF/IPTC
* ✅ Supports **multi processing** and **single image mode**
* ✅ Exports metadata to CSV for bulk uploads (e.g., Adobe Stock)
* ✅ Modular and extensible architecture

---

## 📁 Folder Structure

```
project/
│
├── app.py                   # Gradio app
├── metadata_agent.py        # Logic for metadata generation using LLM
├── image_manager.py         # Utilities for image loading, resizing, base64 encoding
├── embedded.py              # Embeds metadata into image files
├── main.py                  # CLI entry point for batch/single image processing
├── .env                     # Stores OpenAI API key
├── requirements.txt         # Python dependencies
└── README.md                # You're reading it!
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/adobe-metadata-generator.git
cd adobe-metadata-generator
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up API Key

Create a `.env` file in the project root:

```bash
echo OPENAI_API_KEY=your_openai_api_key_here > .env
```

Or pass it as a CLI argument during execution.

---

## ⚙️ How It Works

1. Loads and resizes images (512×512 by default)
2. Sends image data (optionally with filename) to GPT-4o-mini
3. LLM returns:

   * `title`: up to 70 characters
   * `keywords`: 45 single words in visual relevance order
4. Embeds metadata back into the image file
5. Saves all metadata to a CSV

---

## 🛠️ Usage

### Batch Mode

Processes multiple images in batches (default: 3 per batch):

```bash
python app.py
```

You can customize max title leangth, max keywords, etc., via `Gradio Interface`.

---

## 🧪 Example Output

```
Filename: cityscape_sunset.jpg
Title: Majestic Urban Skyline with Vibrant Sunset Glow
Keywords: skyline, sunset, city, buildings, urban, dusk, clouds, architecture, lights, sky, glowing, warm, horizon, tower, highrise, panorama, orange, dramatic, metropolis, scenery
```

