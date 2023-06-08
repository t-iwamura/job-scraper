import time
from typing import Dict

from bs4 import BeautifulSoup
from bs4.element import Tag
from selenium.webdriver.chrome.webdriver import WebDriver


def parse_table_element(table: Tag, field: str, unneeded_str: str = "all") -> str:
    """Parse the value in the given field from a table

    Args:
        table (Tag): Table object found by BeautifulSoup.
        field (str): A field name where a value is.
        unneeded_str (str, optional): A string to be deleted. Defaults to "all".

    Returns:
        str: The value in the given field.
    """
    value = table.find("th", text=field).find_next().text
    if unneeded_str == "all":
        return value.strip()
    else:
        return value.replace(unneeded_str, "")


def parse_company_info(company_url: str, browser: WebDriver) -> str:
    """Parse company information within the given website

    Args:
        company_url (str): The url of a website.
        browser (WebDriver): Browser object.

    Returns:
        str: Comma seperated company information.
    """
    browser.get(company_url)
    time.sleep(5)

    soup = BeautifulSoup(browser.page_source, "lxml")
    try:
        company_name = soup.find("h1", class_="company-header-title-companyName").text
        company_name = company_name.replace(",", "")
    except AttributeError:
        company_info_list = [company_url] + ["-"] * 3
        return ",".join(company_info_list)

    company_data_header = soup.find("h2", id="company-data")
    if company_data_header is None:
        company_info_list = [company_name] + ["-"] * 3
        return ",".join(company_info_list)

    company_data_table = company_data_header.find_next()
    company_capital = parse_table_element(
        company_data_table, field="資本金", unneeded_str=","
    )
    employee_number = parse_table_element(
        company_data_table, field="従業員数", unneeded_str=","
    )
    official_website = parse_table_element(
        company_data_table, field="URL", unneeded_str="all"
    )
    company_info_string = ",".join(
        [
            company_name,
            employee_number,
            company_capital,
            official_website,
        ]
    )

    return company_info_string.replace("\n", "")


def parse_event_info(html_content: str) -> Dict[str, Dict[str, str]]:
    """Parse all the event information in a given html

    Args:
        html_content (str): The content of a given html.

    Returns:
        Dict[str, Dict[str, str]]: The details of each event.
    """
    soup = BeautifulSoup(html_content, "lxml")

    all_event_info = {}
    for event_info in soup.find_all("div", class_="sc-jxFGMa mYmiW"):
        event_name = event_info.find("a", class_="sc-iMCTdq ebLJbf").text
        company_name = event_info.find("span", class_="sc-fSvWoh fPtiZG").text
        all_event_info[event_name] = {"company_name": company_name}

    return all_event_info
