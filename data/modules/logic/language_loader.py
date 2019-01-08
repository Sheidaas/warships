import json

class LanguageLoader:

    def __init__(self, path: str, language: str):
        self.language = {}
        self.file_destination = path + '/data/languages/' + language

    def load_language(self):
        files_to_load = [
            ('gui', '/gui.json'),
        ]

        for file_to_load in files_to_load:
            with open(self.file_destination + file_to_load[1], 'r') as file:
                data = file.read()
                self.language[file_to_load[0]] = json.loads(data)

    def return_language(self):
        self.load_language()
        language = Language()
        for string in self.language.keys():
            language.texts[string] = self.language[string]
        return language


class Language:

    def __init__(self):
        self.texts = {}
