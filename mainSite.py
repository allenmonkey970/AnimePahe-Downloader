import requests
import undetected_chromedriver as uc
import time
from bs4 import BeautifulSoup

def get_cookies_from_selenium(url):
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    driver.get(url)
    time.sleep(10)
    cookies = driver.get_cookies()
    driver.quit()
    return {cookie['name']: cookie['value'] for cookie in cookies}

def search_anime(query, cookies):
    url = "https://animepahe.ru/api"
    params = {"m": "search", "q": query}
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://animepahe.ru/"}
    response = requests.get(url, params=params, headers=headers, cookies=cookies)
    response.raise_for_status()
    return response.json().get("data", [])

def get_episode_links(anime_session, cookies):
    ep_api_url = "https://animepahe.ru/api"
    params = {"m": "release", "id": anime_session, "sort": "episode_asc", "page": 1}
    headers = {"User-Agent": "Mozilla/5.0", "Referer": f"https://animepahe.ru/anime/{anime_session}"}
    response = requests.get(ep_api_url, params=params, headers=headers, cookies=cookies)
    response.raise_for_status()
    return response.json().get("data", [])

def extract_download_links(html):
    soup = BeautifulSoup(html, 'html.parser')
    download_menu = soup.find('div', id='pickDownload')
    if not download_menu:
        return []
    links = download_menu.find_all('a', class_='dropdown-item')
    return [(link.get_text(strip=True), link.get('href')) for link in links]

def filter_downloads(download_links, mode, quality):
    filtered = []
    for label, href in download_links:
        llabel = label.lower()
        if mode == 'sub' and 'subsplease' not in llabel:
            continue
        if mode == 'dub' and 'yameii' not in llabel:
            continue
        if quality in llabel:
            filtered.append((label, href))
    return filtered

def main():
    q = input("Enter anime name: ")
    print("Getting cookies from browser session...")
    cookies = get_cookies_from_selenium("https://animepahe.ru/")
    print("Cookies acquired, searching...")
    results = search_anime(q, cookies)
    if not results:
        print("No results found.")
        return
    print("Select an anime by number:")
    for idx, anime in enumerate(results):
        print(f"{idx+1}. {anime['title']} ({anime.get('type', 'N/A')})")
        print(f"   https://animepahe.ru/anime/{anime['session']}")
    print("-" * 60)
    choice = int(input(f"Enter number (1-{len(results)}): "))
    selected = results[choice-1]
    anime_session = selected['session']

    print("Fetching episode list...")
    episodes = get_episode_links(anime_session, cookies)
    if not episodes:
        print("No episodes found.")
        return

    print("\nWhich download type do you want?")
    print("1. Subbed (SubsPlease, 720p-1080p)")
    print("2. Dubbed (Yameii, 720p-1080p)")
    while True:
        sel = input("Enter 1 for subbed or 2 for dubbed: ").strip()
        if sel == '1':
            mode = 'sub'
            break
        elif sel == '2':
            mode = 'dub'
            break
        else:
            print("Invalid input, please try again.")

    # Get quality options (from first episode with links)
    # Open browser once
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    for ep in episodes:
        driver.get(f"https://animepahe.ru/play/{anime_session}/{ep['session']}")
        time.sleep(8)
        html = driver.page_source
        download_links = extract_download_links(html)
        filtered = []
        for label, _ in download_links:
            llabel = label.lower()
            if (mode == 'sub' and 'subsplease' in llabel) or (mode == 'dub' and 'yameii' in llabel):
                if '720p' in llabel or '1080p' in llabel:
                    filtered.append(label)
        if filtered:
            break

    qualities_available = set()
    for label in filtered:
        if '720p' in label: qualities_available.add('720p')
        if '1080p' in label: qualities_available.add('1080p')
    qualities_available = sorted(list(qualities_available), reverse=True)
    print("\nWhich quality do you want?")
    for idx, q in enumerate(qualities_available):
        print(f"{idx+1}. {q}")
    quality = qualities_available[int(input(f"Enter number for quality (1-{len(qualities_available)}): "))-1]

    print("\nDo you want download links for:")
    print("1. A specific episode")
    print("2. All episodes")
    ep_mode = input("Enter 1 for specific episode, 2 for all: ").strip()

    output_lines = []
    if ep_mode == '1':
        print("\nSelect an episode by number:")
        for idx, ep in enumerate(episodes):
            ep_num = ep.get('episode', 'N/A')
            ep_title = ep.get('title', '')
            print(f"{idx+1}. Episode {ep_num}: {ep_title}")
        ep_choice = int(input(f"Enter episode number (1-{len(episodes)}): "))
        selected_ep = episodes[ep_choice-1]
        ep_url = f"https://animepahe.ru/play/{anime_session}/{selected_ep['session']}"
        print(f"\nFetching HTML for: {ep_url}\n")
        driver.get(ep_url)
        time.sleep(8)
        html = driver.page_source
        download_links = extract_download_links(html)
        filtered_links = filter_downloads(download_links, mode, quality)
        if not filtered_links:
            output_lines.append(f"Episode {selected_ep.get('episode','')} - {selected_ep.get('title','')}")
            output_lines.append(f"Page: {ep_url}")
            output_lines.append("  No matching download links for your selection (e.g., no dub/sub, or not your quality, for this episode).")
            if download_links:
                output_lines.append("  Available download links:")
                for label, href in download_links:
                    output_lines.append(f"    {label}: {href}")
            else:
                output_lines.append("  No download links found at all for this episode.")
        else:
            output_lines.append(f"Episode {selected_ep.get('episode','')} - {selected_ep.get('title','')}")
            output_lines.append(f"Page: {ep_url}")
            for label, href in filtered_links:
                output_lines.append(f"  {label}: {href}")
    else:
        print("\nGathering download links for all episodes (this may take a while)...\n")
        for idx, ep in enumerate(episodes):
            ep_num = ep.get('episode', 'N/A')
            ep_title = ep.get('title', '')
            ep_url = f"https://animepahe.ru/play/{anime_session}/{ep['session']}"
            output_lines.append(f"Episode {ep_num}: {ep_title}")
            output_lines.append(f"Page: {ep_url}")
            driver.get(ep_url)
            time.sleep(8)
            html = driver.page_source
            download_links = extract_download_links(html)
            filtered_links = filter_downloads(download_links, mode, quality)
            if not filtered_links:
                output_lines.append("  No matching download links for your selection (e.g., no dub/sub, or not your quality, for this episode).")
                if download_links:
                    output_lines.append("  Available download links:")
                    for label, href in download_links:
                        output_lines.append(f"    {label}: {href}")
                else:
                    output_lines.append("  No download links found at all for this episode.")
            else:
                for label, href in filtered_links:
                    output_lines.append(f"  {label}: {href}")
            output_lines.append("-" * 60)
    driver.quit()

    filename = f"{selected['title'].replace(' ', '_')}_download_links.txt"
    with open(filename, "w", encoding="utf-8") as f:
        for line in output_lines:
            f.write(line + "\n")
    print(f"\nDone! Download links have been saved to: {filename}")

if __name__ == "__main__":
    main()