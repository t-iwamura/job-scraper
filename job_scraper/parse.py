from typing import Dict

from bs4 import BeautifulSoup


def parse_event_info(html_content: str) -> Dict[str, Dict[str, str]]:
    """Parse all the event information in a given html

    Args:
        html_content (str): The content of a given html.

    Returns:
        Dict[str, Dict[str, str]]: The details of each event.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    all_event_info = {}
    for event_info in soup.find_all("div", class_="sc-jxFGMa mYmiW"):
        event_name = event_info.find("a", class_="sc-iMCTdq ebLJbf").text
        company_name = event_info.find("span", class_="sc-fSvWoh fPtiZG").text
        all_event_info[event_name] = {"company_name": company_name}

    return all_event_info
