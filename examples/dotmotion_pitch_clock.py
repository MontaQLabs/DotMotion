from manim import *
import dotmotion as dot
from dotmotion_pitch import DotmotionPitch
from pathlib import Path
import json

class DotmotionPitchClock(DotmotionPitch):
    def construct(self):
        with dot.PlaybackClock(self) as clock:
            super().construct()
        # Save alongside the 480p render folder; manim handles dirs
        Path('media/videos/dotmotion_pitch/480p15').mkdir(parents=True, exist_ok=True)
        Path('media/videos/dotmotion_pitch/480p15/captions_from_clock.json').write_text(json.dumps(clock.captions, indent=2), encoding='utf-8')
