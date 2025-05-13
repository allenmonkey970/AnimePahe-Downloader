# animepahe-downloader

A Python script for automating the process of searching, extracting download links, and downloading anime episodes from [AnimePahe](https://animepahe.ru/).  
This repo combines searching, link extraction, and batch video file downloads into a simple CLI workflow.

## Features

- **Anime Search**: Search for anime titles
- **Episode Listing**: Fetch and display episode lists with metadata.
- **Download Link Extraction**: Extract direct download links (subs/dubs, quality selection) for episodes.
- **Batch Download Automation**: Download multiple episodes automatically using Selenium (undetected-chromedriver).
- **User-Friendly CLI**: Menu-driven interface for all actions.

## Usage

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/animepahe-downloader.git
cd animepahe-downloader
```

### 2. Install dependencies

It's recommended to use a virtual environment.

```bash
pip install -r requirements.txt
```

**Required dependencies:**
- `requests`
- `beautifulsoup4`
- `undetected-chromedriver`
- `selenium`

### 3. Run the CLI

```bash
python main.py
```

You'll be presented with a menu:

```
==== AnimePahe Downloader Main ====
1. Generate download links from animepahe (search anime, get .txt)
2. Download video files from links file (.txt)
3. Exit
===================================
```

#### Option 1: Generate download links

- Search for your desired anime.
- Select subbed/dubbed and quality (720p/1080p).
- Generate a `.txt` file with download links for all or specific episodes.

#### Option 2: Download from links file

- Provide the `.txt` file generated in step 1.
- The script will open a browser, follow redirect links, and auto-download the videos.

## Folder Structure

```
animepahe-downloader/
├── main.py           # The CLI entry point
├── mainSite.py       # Anime search & link generator
├── downloadSite.py   # Automated downloader script
├── README.md
├── requirements.txt
├── downloads/        # (auto-created) Downloaded video files
└── ...
```

## Notes & Tips

- **Browser Automation**: Uses `undetected-chromedriver` to avoid anti-bot detection.
- **Download Directory**: All videos are saved to the `downloads/` folder by default.
- **AnimePahe Limits**: Excessive requests may result in temporary blocks; proceed responsibly.

## License

[MIT License](https://github.com/allenmonkey970/animepahe-scraper/blob/main/LICENSE)

---

**Disclaimer:**  
This tool is intended for educational use only. Please do NOT copy or distribute downloaded anime episodes to any third party from [AnimePahe](https://animepahe.ru/) and
Do not use this tool to violate the Terms of Service of any website.
