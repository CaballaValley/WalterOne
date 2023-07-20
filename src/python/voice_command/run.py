import os
import sounddevice as sd
from scipy.io.wavfile import write

HERE = os.path.dirname(os.path.abspath(__file__))


def get_default_device(devices):
    for id, device in devices.items():
        if device['name'] == 'default':
            return id, device


def set_device(devices, device_index):
    if device_index not in devices:
        raise ValueError(f"Device index {device_index} not found")
    sd.default.device = devices[device_index]["name"]  # XXX: -1 is a hack


def select_device():

    devices_dict = {i: dev for i, dev in enumerate(sd.query_devices())}
    devices_msg = '\n'.join([
        f"[{i}]: {device['name']}" for i, device in devices_dict.items()
    ])
    default_id, default_device = get_default_device(devices_dict)

    print(f"Available devices: {devices_msg}'")
    print(f"Default device {default_device['name']}, id: {default_id}")

    device_index = int(
        input(f"Select device: ({default_id})") or default_id
    )
    set_device(devices_dict, device_index)

    sd.default.device = device_index


def handle():
    fs = 44100
    duration = 5  # seconds

    wav_file_name = os.path.join(HERE, 'output.wav')

    if not os.path.exists(wav_file_name):
        # os.remove(wav_file_name)
        select_device()

        recording = sd.rec(
            duration * fs, samplerate=fs, channels=2, dtype='float32'
        )
        print("Recording Audio")
        sd.wait()

        print("Audio recording complete , Play Audio")
        sd.play(recording, fs)
        sd.wait()

        write(wav_file_name, fs, recording)  # Save as WAV file
        print("Play Audio Complete")
    else:
        print(f"File {wav_file_name} already exists")


if __name__ == "__main__":
    handle()
