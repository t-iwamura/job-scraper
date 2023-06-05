import json
import logging
import time
from pathlib import Path

import click
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from job_scraper.parse import parse_event_info


@click.command()
@click.option(
    "--output_filename",
    default="event_info.json",
    show_default=True,
    help="Path to output file.",
)
def main(output_filename) -> None:
    """Scrape job events from a given website"""
    logging.basicConfig(level=logging.INFO)

    # Configure browser
    options = Options()
    preference = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", preference)
    browser = Chrome(options=options)

    logging.info(" Launching web browser...")
    url = "https://gaishishukatsu.com/recruiting_info"
    browser.get(url)
    time.sleep(3)

    xpath_pattern = "//div[@class='sc-ksXiDT ijIUWW']/div[1]/div[{}]/label[{}]/input"
    job_type_list = [
        "consultant",
        "marketing",
        "sales",
        "it_engineer",
        "se",
        "data_scientist",
        "generalist",
        "corporate",
        "researcher",
        "engineer",
        "production",
        "ibd",
        "market",
        "research",
        "quants",
        "editor",
    ]
    job_type_idx = {job_type: (7, i) for i, job_type in enumerate(job_type_list, 1)}
    event_type_list = [
        "selection",
        "internship",
        "workshop",
        "union",
        "gaishi_shukatsu",
    ]
    event_type_idx = {
        event_type: (9, i) for i, event_type in enumerate(event_type_list, 1)
    }

    # Choose event information under given conditions
    job_type = "it_engineer"
    logging.info(f"     Chosen job type  : {job_type}")

    filter_by_job_type = browser.find_element(
        By.XPATH, xpath_pattern.format(*job_type_idx[job_type])
    )
    browser.execute_script("arguments[0].click();", filter_by_job_type)
    time.sleep(3)

    event_type = "internship"
    logging.info(f"     Chosen event type: {event_type}")

    filter_by_event_type = browser.find_element(
        By.XPATH, xpath_pattern.format(*event_type_idx[event_type])
    )
    browser.execute_script("arguments[0].click();", filter_by_event_type)
    time.sleep(3)

    logging.info(" Parsing event information from a web page...")
    all_event_info = parse_event_info(browser.page_source)
    logging.info(" Close web browser")
    browser.close()

    output_file_path = Path(output_filename)
    if not output_file_path.parent.exists():
        output_file_path.mkdir(parents=True)

    # Compare latest event information with existing one
    all_event_info_new = all_event_info
    if output_file_path.exists():
        with output_file_path.open("r") as f:
            all_event_info_original = json.load(f)
        all_event_info_new = all_event_info_original

        # Add additional event information only
        has_updated = False
        for event_name, details in all_event_info.items():
            if event_name not in all_event_info_original:
                has_updated = True
                all_event_info_new[event_name] = details

        logging.info(f"     Update after last check: {has_updated}")

    logging.info(" Dump event information")
    logging.info(f"     output filename: {output_filename}")

    with output_file_path.open("w", encoding="utf8") as f:
        json.dump(all_event_info_new, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
