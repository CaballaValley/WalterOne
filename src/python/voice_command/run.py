import os
import logging
from pprint import pformat
import sounddevice as sd
from scipy.io.wavfile import write
import whisper


logging.basicConfig(level=logging.INFO)

HERE = os.path.dirname(os.path.abspath(__file__))


def get_default_device(devices):
    for id, device in devices.items():
        if device['name'] == 'default':
            return id, device


def set_device(devices, device_index):
    if device_index not in devices:
        raise ValueError(f"Device index {device_index} not found")
    sd.default.device = devices[device_index]["name"]


def select_device():

    devices_dict = {i: dev for i, dev in enumerate(sd.query_devices())}
    devices_msg = '\n'.join([
        f"[{i}]: {device['name']}" for i, device in devices_dict.items()
    ])
    default_id, default_device = get_default_device(devices_dict)

    logging.info(f"Available devices: {devices_msg}'")
    logging.info(f"Default device {default_device['name']}, id: {default_id}")

    device_index = int(
        input(f"Select device: ({default_id})") or default_id
    )
    set_device(devices_dict, device_index)

    sd.default.device = device_index


def record_voice_command(audio_file, duration=5):
    fs = 44100

    wav_file_name = os.path.join(HERE, audio_file)

    if os.path.exists(wav_file_name):
        os.remove(wav_file_name)

    select_device()

    recording = sd.rec(
        duration * fs, samplerate=fs, channels=2, dtype='float32'
    )
    logging.info("Recording Audio")
    sd.wait()

    logging.info("Audio recording complete , Play Audio")
    sd.play(recording, fs)
    sd.wait()
    logging.info("Play Audio Complete")
    logging.info(f"Saving Audio {wav_file_name}")
    write(wav_file_name, fs, recording)


def transcribe(audio_file, model_size="medium"):
    logging.info(f"Transcribing {audio_file} with model {model_size}")
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_file,
                              language="es")
    logging.debug(f"Model loaded: {pformat(result)}")
    return result["text"]


def handle():

    audio_file = 'output.wav'
    audio_file_path = os.path.join(HERE, audio_file)
    record_voice_command(audio_file_path, 7)
    order_text = transcribe(audio_file_path)
    logging.info(f"Order text transcript from {audio_file_path}:\n{order_text}")


if __name__ == "__main__":
    handle()
