import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
from transformers import WhisperProcessor, WhisperForConditionalGeneration
import torch
import os
import librosa
device = "cuda:0" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16
torch.cuda.empty_cache()

os.environ['CUDA_LAUNCH_BLOCKING'] = "1"
os.environ['TORCH_USE_CUDA_DSA'] = "1"
audio, sr = librosa.load("../ht.wav", sr=16000)  # Loads at 16 kHz

generate_kwargs = {
    "max_new_tokens": 444,
    "num_beams": 1,
    "condition_on_prev_tokens": False,
    # zlib compression ratio threshold (in token space)
    "compression_ratio_threshold": 1.35,
    "temperature": (0.0, 0.2, 0.4, 0.6, 0.8, 1.0),
    "logprob_threshold": -1.0,
    "no_speech_threshold": 0.6,
    "return_timestamps": True,
    "language": "<|en|>",
    "task": "transcribe"
}


class LazyWhisperModel:
    def __init__(self, model_name="openai/whisper-large-v3"):
        self.model_name = model_name
        self._model = None
        self._processor = None

    @property
    def model(self):
        if self._model is None:
            print("Loading Whisper model...")
            self._model = WhisperForConditionalGeneration.from_pretrained(
                self.model_name,
                torch_dtype="auto",
                device_map="auto",
                use_safetensors=True,
                cache_dir="/home/ahmet/.cache/huggingface/hub/models--openai--whisper-large-v3"
            )
        return self._model

    @property
    def processor(self):
        if self._processor is None:
            print("Loading Whisper processor...")
            self._processor = WhisperProcessor.from_pretrained(self.model_name)
        return self._processor


lazy_model = LazyWhisperModel()

""" pipe = pipeline(
    "automatic-speech-recognition",
    model=lazy_model,
    tokenizer=lazy_model.processor.tokenizer,
    feature_extractor=lazy_model.processor.feature_extractor,
    torch_dtype=torch.float16,
    device=device,
) """


def transcribe_audio(file_path):
    audio_input = lazy_model.processor(
        file_path, sampling_rate=16000, return_tensors="pt").input_features.to("cuda", dtype=torch.float16)
    with torch.no_grad():
        generated_tokens = lazy_model.model.generate(audio_input)
    transcription = lazy_model.processor.batch_decode(
        generated_tokens, skip_special_tokens=True)[0]
    return transcription


if __name__ == "__main__":
    audio_file = "path_to_audio_file.mp3"  # Replace with your audio file path
    print("Transcription:", transcribe_audio(audio))
