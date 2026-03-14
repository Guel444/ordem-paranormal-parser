from typing import Optional, List, Dict
from pydantic import BaseModel


class Attack(BaseModel):
    name: str
    type: Optional[str] = None
    damage: Optional[str] = None
    description: Optional[str] = None


class Ability(BaseModel):
    name: str
    description: str


class Defenses(BaseModel):
    passive: Optional[int] = None
    dodge: Optional[int] = None
    block: Optional[int] = None


class Attributes(BaseModel):
    agility: Optional[int] = None
    strength: Optional[int] = None
    intellect: Optional[int] = None
    presence: Optional[int] = None
    vigor: Optional[int] = None


class Creature(BaseModel):
    name: str
    category: Optional[str] = None
    vd: Optional[int] = None
    hp: Optional[str] = None
    defenses: Optional[Defenses] = None
    resistances: Optional[List[str]] = None
    immunities: Optional[List[str]] = None
    vulnerabilities: Optional[List[str]] = None
    attributes: Optional[Attributes] = None
    skills: Optional[Dict[str, int]] = None
    attacks: Optional[List[Attack]] = None
    abilities: Optional[List[Ability]] = None
    description: Optional[str] = None
    raw_text: Optional[str] = None


class Ritual(BaseModel):
    name: str
    circle: int
    execution: str
    range: str
    target: str
    duration: str
    resistance: Optional[str] = None
    description: str
    raw_text: Optional[str] = None


class ExtractedData(BaseModel):
    creatures: Optional[List[Creature]] = None
    rituals: Optional[List[Ritual]] = None
