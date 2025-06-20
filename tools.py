from typing import Dict, List

all_actual_tools = [
    'Inf2Irregular',
    'GrammarHelper'
]


class Inf2Irregular:
    # mapping: Dict[int, Dict[str, str]]

    def __init__(self, path_to_data='irregular-verbs-de.csv'):
        self.mapping = {2: {}, 3: {}}
        self.create_map(path_to_data)

    def description(self):
        description = {
            "name": "check_regularity",
            "description": "Проверка правильности глагола",
            "parameters": {
                "type": "object",
                "properties": {
                    "verb": {
                        "type": "string",
                        "description": "Инфинитив глагола для проверки"
                    },
                    "format": {
                        "type": "bool",
                        "description": "Регулярный глагол или нет"
                    },
                },
                "required": [
                    "verb",
                ]
            }
        }
        return description

    def create_map(self, path_to_data: str) -> None:
        with open(path_to_data, 'r') as f:
            file = f.readlines()
        for verbs in file:
            inf, snd_f, thrd_f, de = verbs.replace('\n', '').split('","')
            self.mapping[2][inf.replace('"', '')] = snd_f.replace('"', '')
            self.mapping[3][inf.replace('"', '')] = thrd_f.replace('"', '')
        g = 1

    def is_irregular(self, infinitive: str):
        if infinitive in self.mapping[2]:
            return True
        return False

    def do_map(self, infinitive: str, form: int) -> str:
        assert form in [2, 3], f'Inappropriate form {form}'
        return self.mapping[form].get(infinitive, infinitive)

class GrammarHelper:
    singular_nouns_with_s = {
        "measles", "mumps", "aerobics", "gymnastics", "darts",
        "mathematics", "politics", "news", "thanks", "happiness"
    }

    plural_measurements = {"metres", "hours", "miles", "minutes", "seconds", "pounds"}

    always_plural_nouns = {
        "goods", "whereabouts", "remains", "stairs", "proceeds"
    }

    two_part_objects = {
        "glasses", "jeans", "pyjamas", "scales",
        "scissors", "spectacles", "trousers"
    }

    def description(self):
        description = {
        "name": "explain_noun",
        "description": "Объясняет правила согласования глагольной формы для данного существительного",
        "parameters": {
            "type": "object",
            "properties": {
                "noun": {
                    "type": "string",
                    "description": "Существительное для анализа"
                },
            "required": ["noun"
            ]
        }
    }
        return description

    def get_verb_number(self, noun: str) -> str:
        noun = noun.lower()
        if noun in self.singular_nouns_with_s:
            return "singular"
        elif noun in self.always_plural_nouns or noun in self.two_part_objects:
            return "plural"
        elif any(noun.endswith(m) for m in self.plural_measurements):
            return "singular"
        return "unknown"

    def explain_noun(self, noun: str) -> str:
        number = self.get_verb_number(noun)
        if number == "singular":
            return f"The noun '{noun}' ends in -s but takes a singular verb due to its category (illness, abstract, etc.)."
        elif number == "plural":
            return f"The noun '{noun}' is treated as plural and takes a plural verb."
        else:
            return f"No special grammar rule found for '{noun}'. Context is needed."


if __name__ == '__main__':
    i2i = Inf2Irregular('C:\\Users\\tomilov\\LightRAG\\grammar_graph_TIR\\irregular-verbs-de.csv')
    print(i2i.do_map('arise', 2))
    g =1

    gn = GrammarHelper()
    print(gn.get_verb_number("scissors"))  # plural
    print(gn.explain_noun("politics"))     # explanation