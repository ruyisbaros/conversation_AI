from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor
import torch

# Define model path or name
# Can be a Hugging Face Hub model or local path
model_name_or_path = "openai/whisper-large-v3"

# Load model with float16
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_name_or_path,
    torch_dtype=torch.float16,  # Use float16 precision
    low_cpu_mem_usage=True,  # Optimize memory during loading
    use_safetensors=True
)

# Move the model to the GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Load processor (unchanged)
processor = AutoProcessor.from_pretrained(model_name_or_path)
