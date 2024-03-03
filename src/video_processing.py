import os
import subprocess
import io
from typing import BinaryIO, List

from PIL import Image, ImageOps

from image_processing import sticker_to_bw_image

FRAME_EXTRACT_COMMAND = r'ffmpeg -loglevel quiet -vcodec libvpx-vp9 -i - -ss {0} -vframes 1 -f image2pipe -f apng -'
FRAME_COUNT_COMMAND = r'ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=nb_read_frames -of csv=p=0 -'
FRAMERATE_COMMAND = r'ffprobe -v error -select_streams v:0 -show_entries stream=r_frame_rate -of csv=p=0 -'


def _get_framerate(video_bytes: bytes):
    proc = subprocess.run(FRAMERATE_COMMAND, shell=True, input=video_bytes, capture_output=True)

    # it returns fps in 24000 / 1001 format
    f1, f2 = list(map(int, proc.stdout.decode("UTF-8").strip().split("/")))

    return f1 / f2


def _extract_frame(video_bytes: bytes, frame_n: int) -> bytes:
    proc = subprocess.run(FRAME_EXTRACT_COMMAND.format(frame_n), shell=True, input=video_bytes, capture_output=True)

    return proc.stdout


def _get_framecount(video_bytes: bytes) -> int:
    proc = subprocess.run(FRAME_COUNT_COMMAND, shell=True, input=video_bytes, capture_output=True)

    return int(proc.stdout.decode("UTF-8").strip())


def extract_frames(video: BinaryIO, video_parts: List[float]) -> List[bytes]:
    video_bytes = video.read()

    framecount = _get_framecount(video_bytes)
    framerate = _get_framerate(video_bytes)
    frames_timings = [round(x * framecount) / framerate for x in video_parts]
    frames = []
    for frame_timing in frames_timings:
        frame_bytes = _extract_frame(video_bytes, frame_timing)
        frame_io = io.BytesIO(frame_bytes)
        frame_bytes = sticker_to_bw_image(frame_io, "PNG")
        frames.append(frame_bytes)

    return frames
