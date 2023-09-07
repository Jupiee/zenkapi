from DBLscraper import Scraper
from tqdm import tqdm
import asyncio, time

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

    start_time= time.time()

    for link in tqdm(extracted_links, desc= "collecting data", unit= "character"):

        response= await scraper.get_html(link)

        character= scraper.get_characters(response)

        characters.append(character)

    end_time= time.time()

    await scraper.close_session()

    scraper.generate_json(characters)

    print(f"\ndone in {(end_time - start_time) * 1000 : .2f} ms")

if __name__ == "__main__":

    asyncio.run(main())