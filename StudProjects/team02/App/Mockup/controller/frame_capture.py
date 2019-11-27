import cv2
import pafy


class YoutubeVideoWrapper:
	def __init__(self, url):
		video = pafy.new(url)
		self._capture = cv2.VideoCapture()
		self._capture.open(video.getbest(preftype="mp4").url)

	def calculate_number_frames(self, seconds):
		fps = self._capture.get(cv2.CAP_PROP_FPS)
		return fps * seconds - 1

	def set_seconds(self, seconds):
		frames = self.calculate_number_frames(seconds)
		self._capture.set(cv2.CAP_PROP_POS_FRAMES, frames)

	def get_seconds(self):
		fps = self._capture.get(cv2.CAP_PROP_FPS)
		return self._capture.get(cv2.CAP_PROP_POS_FRAMES) // fps

	def forward(self, seconds):
		self.set_seconds(self.get_seconds() + seconds)

	def get_current_image(self):
		success, image = self._capture.read()
		if success:
			return image
		return None

	def __del__(self):
		self._capture.release()