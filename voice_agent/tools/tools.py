"""Tools for scraping content from website"""
import requests
from bs4 import BeautifulSoup
import asyncio 
import functools
from concurrent.futures import ThreadPoolExecutor
from .utils import function_tool

HEADERS_TO_IGNORE = {"chevrolet of stevens creek", "contact us", "more info", "no results"}

BASE_URL = "https://www.stevenscreekchevy.com/"
SALES_SPECIALS_PATH = "newspecials.html"
SERVICE_SPECIALS_PATH = "service-parts-specials.html"
SERVICE_REQUEST_PATH = "service-department-san-jose-ca"
EV_INCENTIVES_PATH = "ev-incentives"
EV_INVENTORY_PATH = "electric-vehicles"
GAS_INVENTORY_PATH = "trucks-for-sale"

async def scrape_site_to_md(url: str): 
    md_lines = []
    is_h1_encountered = False
    loop = asyncio.get_running_loop() 
    executor = ThreadPoolExecutor()
    try: 
        response = await loop.run_in_executor(
            executor,
            functools.partial(requests.get, url, timeout=10)  # timeout as kwarg
        ) 
        if response.status_code != 200: 
            return f"Error: Received status code {response.status_code}", False 
        soup = BeautifulSoup(response.content, 'html.parser')
        # Find all the tags we need in the order they appear
        content_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'span'])

        for tag in content_tags:
            tag_text = tag.get_text(strip=True)

            # Skip empty and unwanted tags
            if not tag_text or tag_text.lower() in HEADERS_TO_IGNORE:
                continue
            if tag_text == "×":
                break
            
            if tag.name == 'h1':
                is_h1_encountered = True
            if not is_h1_encountered:
                continue
            # Check the tag name and format the output accordingly
            if tag.name == 'h1':
                md_lines.append(f"# {tag_text}")
                md_lines.append("")
            elif tag.name == 'h2':
                md_lines.append("")
                md_lines.append(f"## {tag_text}")
            elif tag.name == 'h3':
                md_lines.append(f"### {tag_text}")
            elif tag.name == 'h4':
                md_lines.append(f"#### {tag_text}")
            elif tag.name in ['p', 'span']:
                md_lines.append(f"- {tag_text}")
        
        markdown_content = "\n".join(md_lines).strip()
        return markdown_content, True
    except Exception as e: 
        return f"An error occurred: {e}", False 
    
async def fetch_with_cache(url: str):
    """
    Fetches site content from cache if available
    or within TTL, else scrapes again and saves to cache
    """
    content, status = await scrape_site_to_md(url)
    return content, status


# @function_tool
async def get_sales_specials():
    """Get special or promotionals sales from the website"""
    url_to_scrape = BASE_URL + SALES_SPECIALS_PATH
    scrape_content, status = await fetch_with_cache(url=url_to_scrape)
    if not status:
        return "Unable to get information at this moment. Please try again later"
    return scrape_content


@function_tool
async def get_service_specials():
    """Get specials or offers on services and parts"""
    url_to_scrape = BASE_URL + SERVICE_SPECIALS_PATH
    scrape_content, status = await fetch_with_cache(url=url_to_scrape)
    if not status:
        return "Unable to get information at this moment. Please try again later"
    return scrape_content


@function_tool
async def get_service_content():
    """Get info on services offered and steps to request service appointments"""
    url_to_scrape = BASE_URL + SERVICE_REQUEST_PATH
    scrape_content, status = await fetch_with_cache(url=url_to_scrape)
    if not status:
        return "Unable to get information at this moment. Please try again later"
    return scrape_content


@function_tool
async def get_ev_incentives():
    """Get info on incentives offered for EV purchase"""
    url_to_scrape = BASE_URL + EV_INCENTIVES_PATH
    scrape_content, status = await fetch_with_cache(url=url_to_scrape)
    if not status:
        return "Unable to get information at this moment. Please try again later"
    return scrape_content

@function_tool
async def get_vehicle_inventory_electric():
    """Get inventory info for electric vehicles"""
    url_to_scrape = BASE_URL + EV_INVENTORY_PATH
    scrape_content, status = await fetch_with_cache(url=url_to_scrape)
    if not status:
        return "Unable to get information at this moment. Please try again later"
    return scrape_content

@function_tool
async def get_vehicle_inventory_gas():
    """Get inventory info for gas vehicles"""
    url_to_scrape = BASE_URL + GAS_INVENTORY_PATH
    scrape_content, status = await fetch_with_cache(url=url_to_scrape)
    if not status:
        return "Unable to get information at this moment. Please try again later"
    return scrape_content
