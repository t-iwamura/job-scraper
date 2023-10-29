import json
import logging
import time
from pathlib import Path

import click
from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from tqdm import tqdm

from job_scraper.parse import parse_company_info, parse_event_info

MAX_WAIT_SEC = 10
INDUSTRY_LIST = [
    "consultant",
    "gaishi_finance",
    "nikkei_finance",
    "gaishi_maker_service",
    "trading",
    "civil_servant",
    "it_service",
    "nikkei_maker",
    "media",
    "construction",
]
INDUSTRY_IDS = {industry: i for i, industry in enumerate(INDUSTRY_LIST)}


@click.group()
def main() -> None:
    """Python package for scraping information about Japanese companies"""
    pass


@main.command()
@click.option(
    "--industry",
    type=click.Choice(INDUSTRY_LIST, case_sensitive=False),
    required=True,
    help="Industry which you are interested in.",
)
@click.option(
    "--output_filename",
    default="company_info.csv",
    show_default=True,
    help="Path to output file.",
)
@click.option("--login/--no-login", help="Whether to login to the website or not.")
@click.option("--gui/--no-gui", help="Whether to display a browser or not.")
def company(industry, output_filename, login, gui) -> None:
    """Scrape company information from a website, https://gaishishukatsu.com/"""
    logging.basicConfig(level=logging.INFO)

    # Configure browser
    options = Options()
    preference = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", preference)
    if not gui:
        options.add_argument("--headless=new")
    browser = Chrome(options=options)

    logging.info(" Launching web browser...")
    url = "https://gaishishukatsu.com/company"
    browser.get(url)
    time.sleep(1)

    if login:
        # Visit login page
        link_to_login_page = browser.find_element(By.XPATH, "//a[@href='/login']")
        browser.execute_script("arguments[0].click();", link_to_login_page)

        email_address = input("Enter email address: ")
        password = input("Enter password: ")

        # Perform login
        email_address_field = browser.find_element(By.NAME, "data[GsUser][email]")
        email_address_field.send_keys(email_address)
        password_field = browser.find_element(By.NAME, "data[GsUser][password]")
        password_field.send_keys(password)
        login_button = browser.find_element(
            By.CLASS_NAME, "_btn._btn-orange._btn-lg.login-button"
        )
        browser.execute_script("arguments[0].click();", login_button)
        time.sleep(1)

    # Choose companies in the given industry
    industry_checkbox_block = browser.find_elements(
        By.CSS_SELECTOR, "div.sc-EhVdS.louMgR"
    )[INDUSTRY_IDS[industry]]
    industry_checkbox = industry_checkbox_block.find_element(By.TAG_NAME, "input")
    _ = WebDriverWait(browser, MAX_WAIT_SEC).until(
        expected_conditions.element_to_be_clickable(industry_checkbox)
    )
    browser.execute_script("arguments[0].click();", industry_checkbox)
    time.sleep(1)

    # Display all the companies in the given industry
    while True:
        try:
            show_more_button = browser.find_element(By.CLASS_NAME, "sc-gGuQiZ.fAXLLe")
            browser.execute_script("arguments[0].click();", show_more_button)
            time.sleep(1)
        except NoSuchElementException:
            break

    # Create a list of URLs about the found companies
    soup = BeautifulSoup(browser.page_source, "lxml")
    company_links = []
    company_links += soup.find_all("a", class_="sc-biHcdI fydcZg")
    company_links += soup.find_all("a", class_="sc-hJFzDP fusNkn")
    company_links += soup.find_all("a", class_="sc-bA-DUxO fLGPcp")
    company_links += soup.find_all("a", class_="sc-gJjCBC jDxjuk")
    company_urls = [
        "".join(["https://gaishishukatsu.com", link["href"]]) for link in company_links
    ]

    logging.info(" Parsing information about companies in the chosen industry...")
    all_company_info = ["Company Name,Employee Number,Capital,Official Website"]
    all_company_info += [parse_company_info(url, browser) for url in tqdm(company_urls)]

    logging.info(" Close web browser")
    browser.close()

    output_file_path = Path(output_filename)
    if not output_file_path.parent.exists():
        output_file_path.parent.mkdir(parents=True)

    logging.info(" Dump company information")
    logging.info(f"     output filename: {output_filename}")

    with output_file_path.open("w") as f:
        f.write("\n".join(all_company_info))


@main.command()
@click.option(
    "--output_filename",
    default="event_info.json",
    show_default=True,
    help="Path to output file.",
)
@click.option("--gui/--no-gui", help="Whether to display a browser or not.")
def intern(output_filename, gui) -> None:
    """Scrape job events from a website, https://gaishishukatsu.com/"""
    logging.basicConfig(level=logging.INFO)

    # Configure browser
    options = Options()
    preference = {"profile.default_content_setting_values.notifications": 2}
    options.add_experimental_option("prefs", preference)
    if not gui:
        options.add_argument("--headless=new")
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
    job_type_ids = {job_type: (7, i) for i, job_type in enumerate(job_type_list, 1)}
    event_type_list = [
        "selection",
        "internship",
        "workshop",
        "union",
        "gaishi_shukatsu",
    ]
    event_type_ids = {
        event_type: (9, i) for i, event_type in enumerate(event_type_list, 1)
    }

    # Choose event information under given conditions
    job_type = "it_engineer"
    logging.info(f"     Chosen job type  : {job_type}")

    filter_by_job_type = browser.find_element(
        By.XPATH, xpath_pattern.format(*job_type_ids[job_type])
    )
    browser.execute_script("arguments[0].click();", filter_by_job_type)
    time.sleep(3)

    event_type = "internship"
    logging.info(f"     Chosen event type: {event_type}")

    filter_by_event_type = browser.find_element(
        By.XPATH, xpath_pattern.format(*event_type_ids[event_type])
    )
    browser.execute_script("arguments[0].click();", filter_by_event_type)
    time.sleep(3)

    logging.info(" Parsing event information from a web page...")
    all_event_info = parse_event_info(browser.page_source)
    logging.info(" Close web browser")
    browser.close()

    output_file_path = Path(output_filename)
    if not output_file_path.parent.exists():
        output_file_path.parent.mkdir(parents=True)

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
