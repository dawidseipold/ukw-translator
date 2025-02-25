INPUT_PATH = "public/input.txt"
OUTPUT_PATH = "public/output.txt"

MODEL_NAME = "facebook/mbart-large-50-many-to-many-mmt"
SOURCE_LANG = "en_XX"
TARGET_LANG = "pl_PL"

HEADER_PATTERN = r'^(\[[^\]]+\]\s*)'
TAG_PATTERN = r'(\{g\|[^}]+\})(.*?)(\{/g\})'

TRANSLATION_PARAMS = {
    'num_beams': 5,
    'max_length': 512,
    'no_repeat_ngram_size': 3,
    'early_stopping': True
}

MANUAL_TRANSLATIONS = {
    "A rolling stone gathers no moss": "Toczący się kamień mchu nie narasta",
    "wise men": "mędrcy",
    "know when to settle": "wiedzą kiedy osiąść"
}