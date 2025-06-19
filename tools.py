from typing import Dict


class Inf2Irregular:
    # mapping: Dict[int, Dict[str, str]]

    def __init__(self, path_to_data):
        self.mapping = {2: {}, 3: {}}
        self.create_map(path_to_data)


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


if __name__ == '__main__':
    i2i = Inf2Irregular('C:\\Users\\tomilov\\LightRAG\\grammar_graph_TIR\\irregular-verbs-de.csv')
    print(i2i.do_map('arise', 2))
    g =1