import re

from model.loader import load_model
from processing.tag_processor import TagProcessor
from processing.file_handler import FileHandler
from config.model_config import SOURCE_LANG, TARGET_LANG, TAG_PATTERN
import torch

class Translator:
    def __init__(self):
        self.model, self.tokenizer, self.device = load_model()
        self.tag_processor = TagProcessor()
        self.pattern = re.compile(TAG_PATTERN)

    def translate_segment(self, text: str) -> str:
        if not text.strip():
            return text

        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)

        with torch.no_grad(), torch.amp.autocast(device_type='cuda', dtype=torch.float16):
            generated_tokens = self.model.generate(
                **inputs,
                forced_bos_token_id=self.tokenizer.lang_code_to_id[TARGET_LANG],
                num_beams=4,
                max_length=512
            )

        return self.tokenizer.decode(generated_tokens[0], skip_special_tokens=True)

    def process_line(self, line: str) -> str:
        self.tokenizer.src_lang = SOURCE_LANG

        segments = self.pattern.split(line)
        translated_segments = []

        for i, segment in enumerate(segments):
            if i % 4 == 0:
                if segment:
                    translated = self.tag_processor.apply_manual_translations(segment)
                    translated = self.translate_segment(translated)
                    translated_segments.append(translated)
            elif i % 4 == 2:
                translated = self.tag_processor.apply_manual_translations(segment)
                translated = self.translate_segment(translated)
                translated_segments.append(translated)
            else:
                translated_segments.append(segment)

        return ''.join(translated_segments)

if __name__ == "__main__":
    translator = Translator()
    FileHandler.process_files(translator.process_line)

    print("Translation complete")