from typing import List, Union

class MainAbility:
    
    def __init__(self, name: str, effect: str):

        self.name= name
        self.effect= effect

class UniqueAbility:

    def __init__(self, name: str, effect: str):

        self.ability_name= name
        self.ability_effect= effect

class UniqueAbilities:

    def __init__(self, start_abilities: List[UniqueAbility], zenkai_abilities: Union[List[UniqueAbility], None]):

        self.unique_start_abilities= start_abilities
        self.unique_zenkai_abilities= zenkai_abilities

    def __dict__(self):

        if self.unique_zenkai_abilities != None:

            return {
                "start_abilities": [unique_ability.__dict__ for unique_ability in self.unique_start_abilities],
                "zenkai_abilities": [unique_zenkai_ability.__dict__ for unique_zenkai_ability in self.unique_zenkai_abilities]
            }
        
        else:

            return {
                "start_abilities": [unique_ability.__dict__ for unique_ability in self.unique_start_abilities],
                "zenkai_abilities": None
            }


class UltraAbility:

    def __init__(self, name: str, effect: str):

        self.name= name
        self.effect= effect

class Stats:

    def __init__(self, power: int, health: int, strike_atk: int, strike_def: int, blast_atk: int, blast_def: int):

        self.power= power
        self.health= health
        self.strike_atk= strike_atk
        self.strike_def= strike_def
        self.blast_atk= blast_atk
        self.blast_def= blast_def

class ZAbility:

    def __init__(self, tags: List[str], effect: str):

        self.tags= tags
        self.effect= effect

class ZAbilities:

    def __init__(self, one: ZAbility, two: ZAbility, three: ZAbility, four: ZAbility):

        self.one= one
        self.two= two
        self.three= three
        self.four= four

    def __dict__(self):

        return {
            "one": self.one.__dict__,
            "two": self.two.__dict__,
            "three": self.three.__dict__,
            "four": self.four.__dict__
        }

class SpecialMove:

    def __init__(self, name: str, effect: str):

        self.name= name
        self.effect= effect

class UltimateSkill:

    def __init__(self, name: str, effect: str):

        self.name= name
        self.effect= effect

class SpecialSkill:

    def __init__(self, name: str, effect: str):

        self.name= name
        self.effect= effect
        