import os

import cv2
import youtube_dl

from torch.nn import Identity


QUALITY = "360p"

#TODO: research faster VideoReaders
# https://towardsdatascience.com/lightning-fast-video-reading-in-python-c1438771c4e6
# - VidGear https://pypi.org/project/vidgear/
# - torchvision.io.VideoReader


class VideoReader:
  def __init__(
    self,
    preprocess=Identity(),
    take_every_nth=1,
  ):

    self.preprocess = preprocess
    self.take_every_nth = take_every_nth

  def generate_frames(self, vid):

    video_frames = []

    if not vid.endswith(".mp4"):  # youtube link
        ydl_opts = {}
        ydl = youtube_dl.YoutubeDL(ydl_opts)
        info = ydl.extract_info(vid, download=False)
        formats = info.get("formats", None)
        f = None
        for f in formats:
            if f.get("format_note", None) != QUALITY:
                continue
            break

        cv2_vid = f.get("url", None)

        dst_name = info.get("id") + ".npy"
        # dst = dst_name if self.dest is None else os.path.join(self.dest, dst_name)
    else:
        cv2_vid = vid
        dst_name = vid[:-4].split("/")[-1] + ".npy"
        # dst = vid[:-4] + ".npy" if self.dest is None else os.path.join(self.dest, dst_name)

    cap = cv2.VideoCapture(cv2_vid)  # pylint: disable=I1101
    if not cap.isOpened():
        print(f"Error: {vid} not opened")
        # continue
        return video_frames, dst_name

    ret = True
    ind = 0
    while ret:
        ret, frame = cap.read()

        if ret and (ind % self.take_every_nth == 0):
            video_frames.append(self.preprocess(frame))
        ind += 1

    return video_frames, dst_name
