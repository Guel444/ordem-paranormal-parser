export interface Creature {
  name: string;
  category?: string;
  vd?: number; // VD (Valor de Desafio)
  hp?: string;
  defenses?: {
    passive?: number;
    dodge?: number;
    block?: number;
  };
  resistances?: string[];
  immunities?: string[];
  vulnerabilities?: string[];
  attributes?: {
    agility?: number;
    strength?: number;
    intellect?: number;
    presence?: number;
    vigor?: number;
  };
  skills?: Record<string, number>;
  attacks?: Array<{
    name: string;
    type?: string;
    damage?: string;
    description?: string;
  }>;
  abilities?: Array<{
    name: string;
    description: string;
  }>;
  description?: string;
  rawText?: string;
}

export interface Ritual {
  name: string;
  circle: number;
  execution: string;
  range: string;
  target: string;
  duration: string;
  resistance?: string;
  description: string;
  rawText?: string;
}

export interface Ability {
  name: string;
  type?: string;
  requirement?: string;
  description: string;
  rawText?: string;
}

export type ExtractedData = {
  creatures?: Creature[];
  rituals?: Ritual[];
  abilities?: Ability[];
};
