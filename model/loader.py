import torch
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
from config.index import MODEL_NAME

def load_model():
    assert torch.cuda.is_available()
    device = torch.device("cuda")
    torch.backends.cudnn.benchmark = True

    model = MBartForConditionalGeneration.from_pretrained(
        MODEL_NAME,
        torch_dtype = torch.float16,
        device_map = "auto"
    ).eval()

    tokenizer = MBart50TokenizerFast.from_pretrained(MODEL_NAME)

    return model, tokenizer, device