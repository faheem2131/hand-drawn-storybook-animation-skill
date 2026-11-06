# 《小纸船》The Little Paper Boat — 30-second example

A 30-second watercolor picture-book short made with this skill. All of it is drawn live on one canvas by code: no image assets, no fonts or CDN beyond system fonts. The score is synthesized too.

一个用本 Skill 做的 30 秒水彩绘本短片：画面全部由代码在一张 canvas 上实时画出，没有图片素材；配乐也是程序合成的。

▶ Video: [`previews/09-little-paper-boat-30s.mp4`](../../previews/09-little-paper-boat-30s.mp4) (1280×720, 30 fps, AAC stereo)

## Story · 故事

| Time | Shot | Picture | Subtitle (EN / 中文) |
|---|---|---|---|
| 0–3.7s | Wide, blank paper | Title writes itself; the horizon line is inked; sky and sea wash in from the left | — |
| 3.8–8.6s | Push-in close-up | A sheet of paper flutters down, folds itself into a boat and lands with a splash | A sheet of paper wanted to see the sea. / 一张纸，想去看看大海。 |
| 8.6–13s | Tracking medium | The boat sails; gulls cross; the sun sets behind the horizon | It sailed until the sun fell asleep. / 它一直漂，漂到太阳都睡着了。 |
| 13–17.2s | Extreme wide pull-out | Night: moon and stars, a tiny boat on a big dark sea | Then the sea grew dark. Which way was home? / 海变黑了。家，在哪儿呢？ |
| 17.4–22.4s | Tracking, low | **Nine stars fall one by one** and bloom gold on the water, a path of light | So the stars came down to light the way. / 于是，星星落下来，为它照亮了路。 |
| 22.8–27.4s | Medium on the shore | A warm window and a child with a lantern; she leans down and lifts the boat | Someone had been waiting all along. / 原来，一直有人在等它。 |
| 27.4–30s | Close-up, then end card | Gold glow; a wet-brush wipe to fresh paper; title and red seal | — |

Light grammar: warm light (window, lantern, star blooms) belongs to whoever is waiting; the boat itself stays paper-white.

## Files · 文件

- `index.html` — the whole animation. Open it and press Play (it plays `soundtrack.m4a` from the same folder if present). `window.renderAt(t)` draws any frame, so playback, seeking and recording are deterministic.
- `render.cjs` — headless Chromium renderer: `node render.cjs frames <dir> 30` writes the PNG sequence; `node render.cjs stills <dir> 5 12.5 20` writes stills for a contact sheet.
- `soundtrack.py` — numpy synth for the score: felt piano, pad, one bell per falling star, sea noise, splash and reverb, mastered to about −16 LUFS.

## Rebuild · 重新生成

```bash
cd examples/little-paper-boat
node render.cjs frames /tmp/boat-frames 30
python3 soundtrack.py soundtrack.wav
ffmpeg -framerate 30 -i /tmp/boat-frames/f%05d.png -i soundtrack.wav \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 160k -shortest \
  -movflags +faststart ../../previews/09-little-paper-boat-30s.mp4
ffmpeg -i soundtrack.wav -c:a aac -b:a 128k soundtrack.m4a
```

Notes: there is no voice-over. Doubao TTS needs your own key, so this cut uses burned-in bilingual subtitles. The audio was checked with loudness and spectrum measurements, not by ear.

说明：没有配音（豆包 TTS 需要你自己的 Key），用的是中英双语字幕；音频只做了响度和频谱检查，没有人耳试听。
