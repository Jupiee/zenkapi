import json
from pathlib import Path

def filter_characters(filters: dict):
    
    path= Path(__file__).parent.parent / "scraper" / "characters.json"
    file= open(path)
    characters= json.load(file)
    
    filtered_results= []

    if filters["color"] and "," in filters["color"]:

        filters["color"]= filters["color"].split(",")

    if filters["rarity"] and "," in filters["rarity"]:

        filters["rarity"]= filters["rarity"].split(",")

    if filters["tags"] and "," in filters["tags"]:

        filters["tags"]= filters["tags"].split(",")

    for character in characters:
        
        if (
            (filters["name"] is None or character["name"].lower() == filters["name"].lower())
            and (filters["contains"] is None or filters["contains"].lower() in character["name"].lower())
            and (filters["has_zenkai"] is None or character["has_zenkai"] == filters["has_zenkai"])
            and (filters["is_lf"] is None or character["is_lf"] == filters["is_lf"])
            and (filters["is_tag"] is None or character["is_tag"] == filters["is_tag"])
            and (filters["id"] is None or character["id"] == filters["id"])
            and (filters["color"] is None or character["color"] in filters["color"])
            and (filters["rarity"] is None or character["rarity"] in filters["rarity"])
            and (
                filters["tags"] is None
                or (
                    isinstance(filters["tags"], str) and filters["tags"].lower() in [c_tag.lower() for c_tag in character["tags"]]
                )
                or (
                    isinstance(filters["tags"], list) and all(tag.lower() in [c_tag.lower() for c_tag in character["tags"]] for tag in filters["tags"])
                )
            ) 
        ):

            filtered_results.append(character)

    return filtered_results