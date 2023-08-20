from DBLscraper import Scraper
from tqdm import tqdm
import asyncio

async def main():

    url= "/characters/"
    scraper= Scraper()
    characters= []

    html= await scraper.get_html(url)

    if html == None:
    
        print("request not sent")
        await scraper.close_session()
        return

    extracted_links= scraper.fetch_links(html)

    for link in tqdm(extracted_links, desc= "collecting data", unit= "character"):

        response= await scraper.get_html(link)

        character= scraper.get_characters(response)

        characters.append(character)

    await scraper.close_session()

    scraper.generate_json(characters)

    print("\ndone")

if __name__ == "__main__":

    asyncio.run(main())