# Copyright (C) 2024 Brandon Namgoong
# Written for Windows Server Datacenter scheduled task
# This web-scraping script is purely for research and documentation purposes only
# This project is not affiliated in any way by the KCNA Watch database

"""
Adds chapter marks to KCTV broadcasts at the start of every program.

Attempts to use OCR to scan timestamps during the "Today's Schedule" (오늘의 순서) feature.
"""

from datetime import date
from PIL import Image
from paddleocr import PaddleOCR
import numpy as np
import ffmpeg
import io

# Manual search from set bounds
def _search_bounds(path: str) -> list[str]:
    ocr: PaddleOCR = PaddleOCR(
        rec_model_dir = "../ppocr/korean_PP-OCRv4_rec_infer",
        rec_char_dict_path = "../ppocr/kctv_times_dict.txt",
        lang = "korean"
    )
    txts: list[str] = []
    for s in range(ss, to, 1):
        img: np.ndarray = np.array(Image.open(io.BytesIO((
            ffmpeg
            .input(path, ss = s)
            .output("pipe:", vframes = "1", format = "image2", vcodec = "png")
            .run(capture_stdout = True, capture_stderr = True)
        )[0])).crop(box))
        res: list = list(ocr.ocr(img, det = False, cls = False, inv = True)[0][0])

        if res[1] >= 0.5:
            txts.append(res[0])
            if verbose: print("{}s text: {}".format(s, res))
        else:
            if verbose: print("{}s none: {}".format(s, res))
    # TODO filter and remove duplicates
    return txts

def set_bounds(start: str, end: str):
    """
    Manually specify start and end times of 'Today's Schedule', bypassing the automatic feature checker.

    Start and stop times formatted as HH:MM:SS.
    """

    a = [ int(t) for t in start.split(":") ]
    b = [ int(t) for t in end.split(":") ]

    global ss
    ss = (a[0] * 3600) + (a[1] * 60) + a[2]
    global to
    to = (b[0] * 3600) + (b[1] * 60) + b[2]
    global set
    set = True

def search(day: date) -> list[str]:
    """
    Use OCR to search for timestamp text for chapter marks
    """
    f = "../temp/dl-%s.mp4" % day.isoformat()

    if set:
        return _search_bounds(f)
    
    txts: list[str] = []
    # TODO the processing logic
    return txts

def encode_chapters(day: date, times: list[int]):
    """
    Encode downloaded broadcast with chapter mark metadata.

    Will save encode as 'enc-YYYY-MM-DD.mp4'.
    """

    pass

# Global values
ss: int = 300 # 5 minutes
to: int = None
set: bool = False
box: tuple[int] = (80, 100, 230, 160) # (30, 90, 230, 190)
verbose: bool = False

"""
if not text and failed each time 1 hour after start bound:
    end
if not text and failed each time 30 seconds after last successful check and boolean is true:
    end
check frame every 1 second, check bounding box for text
if text:
    read
    save to list
    if first encounter: set boolean true
if not text:
    add fail count
    continue
"""