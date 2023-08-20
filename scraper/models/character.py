from typing import List, Union
from .info import Rarity, Color
from .detail import MainAbility, UniqueAbilities, UltraAbility, Stats, ZAbilities, SpecialMove, SpecialSkill, UltimateSkill

class Character:

    def __init__(self, name: str, id: str, color: Color, rarity: Rarity, tags: List[str], main_ability: MainAbility, unique_ability: UniqueAbilities, ultra_ability: Union[UltraAbility, None], base_stats: Stats, max_stats: Stats, strike: str, shot: str, image_url: str, special_move: SpecialMove, special_skill: SpecialSkill, ultimate_skill: Union[UltimateSkill, None], z_ability: ZAbilities, is_lf: bool, is_tag: bool, has_zenkai: bool):

        self.name= name
        self.id= id= id
        self.color= color
        self.rarity= rarity
        self.tags= tags
        self.main_ability= main_ability
        self.unique_ability= unique_ability
        self.ultra_ability= ultra_ability
        self.base_stats= base_stats
        self.max_stats= max_stats
        self.strike= strike
        self.shot= shot
        self.image_url= image_url
        self.special_move= special_move
        self.special_skill= special_skill
        self.ultimate_skill= ultimate_skill
        self.z_ability= z_ability
        self.is_lf= is_lf
        self.is_tag= is_tag
        self.has_zenkai= has_zenkai

    def __dict__(self):

        if self.ultra_ability != None:

            ability= self.ultra_ability.__dict__

        else:

            ability= None

        if self.ultimate_skill != None:

            ultimate_skill= self.ultimate_skill.__dict__

        else:

            ultimate_skill= None

        return {
            "name": self.name,
            "id": self.id,
            "color": self.color,
            "rarity": self.rarity,
            "tags": self.tags,
            "main_ability": self.main_ability.__dict__,
            "unique_ability": self.unique_ability.__dict__(),
            "ultra_ability": ability,
            "base_stats": self.base_stats.__dict__,
            "max_stats": self.max_stats.__dict__,
            "strike": self.strike,
            "shot": self.shot,
            "image_url": self.image_url,
            "special_move": self.special_move.__dict__,
            "special_skill": self.special_skill.__dict__,
            "ultimate_skill": ultimate_skill,
            "z_ability": self.z_ability.__dict__(),
            "is_lf": self.is_lf,
            "is_tag": self.is_tag,
            "has_zenkai": self.has_zenkai
        }