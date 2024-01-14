from selectolax.lexbor import LexborHTMLParser
from models import *

import json, asyncio, httpx

class Scraper:

    def __init__(self):

        self.timeout= httpx.Timeout(connect= None, read= None, write= None, pool= None)
        self.session= httpx.AsyncClient(timeout= self.timeout)
        #self.session= aiohttp.ClientSession()

    async def get_html(self, path):

        params= {"User-Agent": "Mozilla/5.0 (U; Linux x86_64) Gecko/20130401 Firefox/58.3"}

        while True:

            #async with self.session.get(f"https://legends.dbz.space{path}", params= params) as response:
                
            response= await self.session.get(f"https://legends.dbz.space{path}", headers= params)

            if response.status_code == 200:

                return response.text
            
            elif response.status_code == 403:

                await asyncio.sleep(5)
        
    async def close_session(self):

        await self.session.aclose()

    def fetch_links(self, html):

        parser= LexborHTMLParser(html)

        links= map(self.fetch_hrefs, parser.css_first("div.chara.list").css("a"))

        return list(links)
    
    def fetch_hrefs(self, tag):

        return tag.attributes["href"]
    
    def extract_tags(self, html, selector):

        parser= LexborHTMLParser(html)

        tags= list(set(tag.text() for tag in parser.css_first(selector).css("a")))
        effect= parser.css_first(selector).text()

        return tags, effect
    
    def remove_tabs_spaces(self, text: str):

        return text.strip().replace("\n", " ")

    def fetch_data(self, html, selector, type):

        parser= LexborHTMLParser(html)

        if type == "single":

            return self.remove_tabs_spaces(parser.css_first(selector).text())
        
        else:

            return parser.css(selector)

    def to_object(self, data: Character):

        return data.__dict__()

    def get_characters(self, html):

        name= self.fetch_data(html, "div.head.name.large.img_back h1", "single")

        id= self.fetch_data(html, "div.head.name.id-right.small.img_back", "single")

        color= Color[self.fetch_data(html, "div.element", "single")].value

        rarity= Rarity[self.fetch_data(html, "div.rarity", "single")].value

        tags= list(map(self.remove_tabs_spaces, [nodes.text() for nodes in self.fetch_data(html, "span.ability.medium a", "multiple")]))

        main_ability_name= self.fetch_data(html, "div.frm.form0 span.ability.medium", "single")
        main_ability_effect= self.fetch_data(html, "div.frm.form0 div.ability_text.small", "single")

        main_ability= MainAbility(main_ability_name, main_ability_effect)

        try:

            ultra_ability_name= self.fetch_data(html, "a#charaultra + div.ability_text div.frm.form0 span.ability.medium", "single")
            ultra_ability_effect= self.fetch_data(html, "a#charaultra + div.ability_text div.frm.form0 div.ability_text.small", "single")

            ultra_ability= UltraAbility(ultra_ability_name, ultra_ability_effect)

        except:

            ultra_ability= None

        unique_abilities_list= [UniqueAbility(self.remove_tabs_spaces(node.css_first("span.ability.medium").text()), self.remove_tabs_spaces(node.css_first("div.ability_text.small").text())) for node in self.fetch_data(html, "a#charaunique + div.ability_text div.frm.form0", "multiple")]

        unique_zenkai_abilities_list= [UniqueAbility(self.remove_tabs_spaces(node.css_first("span.ability.medium").text()), self.remove_tabs_spaces(node.css_first("div.ability_text.small").text())) for node in self.fetch_data(html, "a#charaunique + div.ability_text div.frm.form1", "multiple")]

        if unique_zenkai_abilities_list == []:

            unique_zenkai_abilities_list= None

            has_zenkai= False

        else:

            has_zenkai= True            

        unique_abilities= UniqueAbilities(unique_abilities_list, unique_zenkai_abilities_list)

        base_stats_list= [int(node.css_first("div.val").attributes["raw"]) for node in self.fetch_data(html, "div.row.lvlbreak.lvb1 div.col", "multiple")]

        max_stats_list= [int(node.css_first("div.val").attributes["raw"]) for node in self.fetch_data(html, "div.row.lvlbreak.lvb5000 div.col", "multiple")]

        base_stats= Stats(*base_stats_list)
        max_stats= Stats(*max_stats_list)

        image_url= LexborHTMLParser(html).css_first("img.cutin.trs0.form0").attributes["src"]

        strike_info= self.fetch_data(html, "a#charastrike + div.ability_text.arts div.frm.form0 div.ability_text.small", "single")
        shot_info= self.fetch_data(html, "a#charashot + div.ability_text.arts div.frm.form0 div.ability_text.small", "single")

        specialmove_name= self.fetch_data(html, "a#charaspecial_move + div.ability_text.arts div.frm.form0 span.ability.medium", "single")
        specialmove_effect= self.fetch_data(html, "a#charaspecial_move + div.ability_text.arts div.frm.form0 div.ability_text.small", "single")

        special_move= SpecialMove(specialmove_name, specialmove_effect)

        specialskill_name= self.fetch_data(html, "a#charaspecial_skill + div.ability_text.arts div.frm.form0 span.ability.medium", "single")
        specialskill_effect= self.fetch_data(html, "a#charaspecial_skill + div.ability_text.arts div.frm.form0 div.ability_text.small", "single")

        special_skill= SpecialSkill(specialskill_name, specialskill_effect)

        try:

            ultimateskill_name= self.fetch_data(html, "a#charaultimate_skill + div.ability_text.arts div.frm.form0 span.ability.medium", "single")
            ultimateskill_effect= self.fetch_data(html, "a#charaultimate_skill + div.ability_text.arts div.frm.form0 div.ability_text.small", "single")

            ultimate_skill= UltimateSkill(ultimateskill_name, ultimateskill_effect)

        except:

            ultimate_skill= None

        z1= self.extract_tags(html, "div.zability.zI div.ability_text.medium")
        z2= self.extract_tags(html, "div.zability.zII div.ability_text.medium")
        z3= self.extract_tags(html, "div.zability.zIII div.ability_text.medium")
        z4= self.extract_tags(html, "div.zability.zIV div.ability_text.medium")

        is_lf= True if LexborHTMLParser(html).css_first("img.legends-limited") else False

        zabilities= ZAbilities(ZAbility(*z1), ZAbility(*z2), ZAbility(*z3), ZAbility(*z4))

        character= Character(name, id, color, rarity, tags, main_ability, unique_abilities, ultra_ability, base_stats, max_stats, strike_info, shot_info, image_url, special_move, special_skill, ultimate_skill, zabilities, is_lf, False, has_zenkai)

        return character
    
    def generate_json(self, characters):

        characters= list(map(self.to_object, characters))

        with open("characters.json", "w") as file:

            json.dump(characters, file, indent= 4)