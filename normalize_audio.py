from ffmpeg_normalize import FFmpegNormalize
from glob import glob

norm = FFmpegNormalize()

mp3_files = glob('test_audios/*.mp3')

for mp3_file in mp3_files:
    norm.add_media_file(mp3_file, f'{mp3_file[:-4]}-output.wav')

norm.run_normalization()
