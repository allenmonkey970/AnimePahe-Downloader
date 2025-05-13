# AnimePahe Downloader

AnimePahe Downloader is a Python script that helps you search for anime, extract direct download links, and batch-download episodes from [AnimePahe](https://animepahe.ru/)—all from a simple command-line interface.

## What It Does

- **Anime Search:** Find anime titles and view available episodes.
- **Episode Listings:** See episode lists along with useful metadata.
- **Download Link Extraction:** Get direct download links (choose subs/dubs and video quality).
- **Batch Downloads:** Download multiple episodes in one go, using Selenium and `undetected-chromedriver` to get around anti-bot measures.
- **Easy CLI:** A menu-driven interface guides you through every step.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/animepahe-downloader.git
cd animepahe-downloader
```

### 2. Install dependencies

It's best to use a virtual environment.

```bash
pip install -r requirements.txt
```

Main dependencies:
- `requests`
- `beautifulsoup4`
- `undetected-chromedriver`
- `selenium`

### 3. Run the script

```bash
python main.py
```

You'll see a menu like this:

```
==== AnimePahe Downloader Main ====
1. Generate download links from animepahe (search anime, get .txt)
2. Download video files from links file (.txt)
3. Exit
===================================
```

#### Option 1: Generate download links

- Search for an anime title.
- Pick subbed/dubbed and video quality (720p/1080p).
- Save download links for selected episodes into a `.txt` file.

#### Option 2: Download from links file

- Choose the `.txt` file you created earlier.
- The script opens a browser, follows the links, and automatically downloads the videos.

## Project Structure

```
animepahe-downloader/
├── main.py           # CLI entry point
├── mainSite.py       # Handles anime search and link generation
├── downloadSite.py   # Handles automated downloads
├── README.md
├── requirements.txt
├── downloads/        # (auto-created) Where downloaded video files go
└── ...
```

## Tips & Notes

- **Automation:** Uses `undetected-chromedriver` to reduce the chance of being blocked.
- **Download Location:** All videos are saved to the `downloads/` folder.
- **AnimePahe Limits:** Too many requests can get your IP temporarily blocked. Download responsibly.

## License

[MIT License](https://github.com/allenmonkey970/animepahe-scraper/blob/main/LICENSE)

---

**Disclaimer:**  
This tool is for educational use only. Don't redistribute, download anime, or use this script to break the Terms of Service of AnimePahe or any other site.
