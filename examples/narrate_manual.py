from pathlib import Path
import json
import dotmotion as dot


def main():
    # Input base video (rendered with Manim separately)
    video_in = 'media/videos/dotmotion_pitch/480p15/DotmotionPitch.mp4'

    # Option 1: Load JSON captions
    json_caps = 'examples/captions_template.json'
    captions = dot.load_captions_from_json(json_caps)

    # Narration only
    out_narr = 'media/videos/dotmotion_pitch/480p15/DotmotionPitch_manual_narrated.mp4'
    dot.narrate_from_captions(video_in, captions, out_narr, burn_subtitles=False)
    print('Wrote', out_narr)

    # Narration + BGM (ensure BGM exists)
    music = Path('assets/bgm.mp3')
    if not music.exists():
        home = Path.home()
        for cand in ['rescue me.mp3', 'rescue_me.mp3', 'rescue.mp3', 'Rescue Me.mp3']:
            p = home / 'Downloads' / cand
            if p.exists():
                music = p
                break

    if music.exists():
        out_mix = 'media/videos/dotmotion_pitch/480p15/DotmotionPitch_manual_narrated_bgm.mp4'
        dot.narrate_with_bgm(video_in, captions, str(music), out_mix, burn_subtitles=False, music_db=-22.0)
        print('Wrote', out_mix)
    else:
        print('No BGM found; skipped mix.')


if __name__ == '__main__':
    main()



