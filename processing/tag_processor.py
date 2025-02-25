import re
from config.model_config import TAG_PATTERN
from config.translations import MANUAL_TRANSLATIONS

class TagProcessor:
    def __init__(self):
        self.pattern = re.compile(TAG_PATTERN)

    def apply_manual_translations(self, text: str) -> str:
        for phrase in sorted(MANUAL_TRANSLATIONS.keys(), key=len, reverse=True):
            text = text.replace(phrase, MANUAL_TRANSLATIONS[phrase])
        return text

    def process_tags(self, line: str, translate_function) -> str:
        def replace_tag(match):
            opening, content, closing = match.groups()
            translated = translate_function(self.apply_manual_translations(content))

            return f"{opening}{translated}{closing}"

        return self.pattern.sub(replace_tag, line)