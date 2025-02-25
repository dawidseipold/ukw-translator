from model.loader import load_model
from processing.line_processor import LineProcessor
from processing.file_handler import FileHandler
from config.index import *
import torch


class Translator:
    def __init__(self):
        self.model, self.tokenizer, self.device = load_model()
        self.processor = LineProcessor()
        self.tokenizer.src_lang = SOURCE_LANG

    def translate_segment(self, text: str) -> str:
        if not text.strip():
            return text

        text = self.processor.apply_manual_translations(text)
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)

        with torch.no_grad(), torch.amp.autocast(device_type='cuda', dtype=torch.float16):
            generated_tokens = self.model.generate(
                **inputs,
                forced_bos_token_id=self.tokenizer.lang_code_to_id[TARGET_LANG],
                **TRANSLATION_PARAMS
            )

        return self.tokenizer.decode(generated_tokens[0], skip_special_tokens=True)

    def process_line(self, line: str) -> str:
        header, content = self.processor.split_header(line)
        processed_content = self.processor.process_tags(content, self.translate_segment)

        return f"{header}{processed_content}"


if __name__ == "__main__":
    translator = Translator()
    FileHandler.process_files(translator.process_line)

    print("Tłumaczenie zakończone pomyślnie!")