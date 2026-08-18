import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from factory.models import FactoryVideo
from factory.video_utils import convert_video_to_h264

videos = FactoryVideo.objects.exclude(video_file='')
print(f'Found {videos.count()} videos to convert...')

for v in videos:
    if v.video_file:
        path = v.video_file.path
        print(f'Converting: {path}')
        result = convert_video_to_h264(path)
        status = 'OK' if result else 'FAILED'
        print(f'  -> {status}')

print('Done.')
