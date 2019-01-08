from .language_loader import LanguageLoader
from .scoreboard_loader import ScoreLoader


class Database:

    def __init__(self, path, language):
        self.language = LanguageLoader(path, language).return_language()
        self.scoreboard = ScoreLoader(path).return_scoreboard()