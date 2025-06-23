from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import os
import time

YEARS = range(2000, 2026)
BASE_URL = "https://www.baseball-almanac.com/yearly/yr{year}a.shtml"
CSV_PATH = "data/player_stats_2000_2025.csv"


def create_driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-download-protection")  
    options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "profile.default_content_setting_values.automatic_downloads": 2
    })
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    )
    return webdriver.Chrome(options=options)


def extract_stats(driver, year, keyword):
    """Generic extractor for tables with specific heading text."""
    url = BASE_URL.format(year=year)
    driver.get(url)
    time.sleep(2)
    results = []

    tbodies = driver.find_elements(By.TAG_NAME, "tbody")
    for tbody in tbodies:
        header_cells = tbody.find_elements(By.CSS_SELECTOR, "td.header[colspan='5']")
        if not header_cells:
            continue

        h2_elements = header_cells[0].find_elements(By.TAG_NAME, "h2")
        if not h2_elements:
            continue

        title = h2_elements[0].text.strip()
        if str(year) in title and keyword in title:
            for row in tbody.find_elements(By.TAG_NAME, "tr"):
                if row.find_elements(By.CSS_SELECTOR, "td.banner, td.headerBlue, td.header"):
                    continue

                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 4:
                    category = cells[0].text.strip()
                    player = cells[1].text.strip()
                    team = cells[2].text.strip()
                    value = cells[3].text.strip()

                    if category and player and team and value:
                        results.append({
                            "Year": year,
                            "Category": category,
                            "Player": player,
                            "Team": team,
                            "Value": value,
                            "Source": keyword
                        })
            break
    return results


def main():
    os.makedirs("data", exist_ok=True)
    driver = create_driver()
    all_data = []

    for year in YEARS:
        try:
            print(f"\n year {year}")
            player_stats = extract_stats(driver, year, "Player Review")
            pitcher_stats = extract_stats(driver, year, "Pitcher Review")
            if player_stats:
                print(f"  Players: {len(player_stats)}")
                all_data.extend(player_stats)
            if pitcher_stats:
                print(f"  Pitchers: {len(pitcher_stats)}")
                all_data.extend(pitcher_stats)
        except Exception as e:
            print(f"  error: {e}")
        time.sleep(1.2)

    driver.quit()

    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["Year", "Category", "Player", "Team", "Value", "Source"])
        writer.writeheader()
        writer.writerows(all_data)

    print(f"\n {len(all_data)} in {CSV_PATH}")


if __name__ == "__main__":
    main()
