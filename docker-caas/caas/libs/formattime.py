import time

class FormatTime(object):
	def __init__(self):
		pass

	@classmethod
	def localtimeToFormattime(cls, localTime):
		'''localtime format formattime.'''

		time_obj = time.localtime(localTime)
		str_time = time.strftime('%Y-%m-%d %H:%M:%S', time_obj)
		return str_time


if __name__ == "__main__":
	print(FormatTime.localtimeToFormattime(1443429788))