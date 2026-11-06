#!/usr/bin/env python3
"""Generate the 30-second score for "The Little Paper Boat" (felt piano, warm pad,
star bells, sea ambience) as soundtrack.wav. Timings match the cues in index.html.

    python3 soundtrack.py [out.wav]
Needs numpy. Everything is synthesized; no samples.
"""
import sys
import wave

import numpy as np

SR = 44100
DUR = 30.0
N = int(SR * DUR)
rng = np.random.default_rng(7)
out_dry = np.zeros((N, 2))


def note_hz(name):
    names = {'C': -9, 'D': -7, 'E': -5, 'F': -4, 'G': -2, 'A': 0, 'B': 2}
    semis = names[name[0]] + (1 if '#' in name else 0)
    octave = int(name[-1])
    return 440.0 * 2 ** ((semis + (octave - 4) * 12) / 12)


def place(sig, t, pan=0.0, gain=1.0):
    i = int(t * SR)
    if i >= N:
        return
    sig = sig[: N - i] * gain
    out_dry[i:i + len(sig), 0] += sig * np.sqrt(0.5 * (1 - pan))
    out_dry[i:i + len(sig), 1] += sig * np.sqrt(0.5 * (1 + pan))


def piano(name, length=2.6, vel=0.5):
    """Felt piano: few soft harmonics, fast attack, long exponential release."""
    f = note_hz(name)
    t = np.arange(int(SR * length)) / SR
    s = np.zeros_like(t)
    for k, (amp, dec) in enumerate([(1, 1.1), (.38, 1.8), (.12, 2.6), (.05, 3.4)], start=1):
        s += amp * np.sin(2 * np.pi * f * k * t * (1 + .0004 * k)) * np.exp(-t * dec * (1 + f / 900))
    s *= np.minimum(1, t / .008)
    s *= np.minimum(1, (length - t) / .4)        # gentle tail fade
    thump = rng.standard_normal(len(t)) * np.exp(-t * 90) * .05
    return (s + thump) * vel * .32


def bell(name, length=3.0, vel=0.5):
    f = note_hz(name)
    t = np.arange(int(SR * length)) / SR
    s = (np.sin(2 * np.pi * f * t) * np.exp(-t * 1.4)
         + .32 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 2.8)
         + .12 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 5))
    s *= np.minimum(1, t / .003) * np.minimum(1, (length - t) / .3)
    return s * vel * .22


def pad(names, t0, t1, vel=0.5, att=1.4, rel=1.6):
    length = t1 - t0 + rel
    t = np.arange(int(SR * length)) / SR
    env = np.minimum(1, t / att) * np.clip((length - t) / rel, 0, 1)
    s = np.zeros_like(t)
    for name in names:
        f = note_hz(name)
        for det in (-.0025, .0025):
            vib = 1 + .0015 * np.sin(2 * np.pi * 4.6 * t + det * 900)
            s += np.sin(2 * np.pi * f * (1 + det) * t * vib) + .18 * np.sin(2 * np.pi * 2 * f * t)
    return s * env * vel * .03 / len(names) * 4


# ------------------------------------------------------------------ score
# title on blank paper: sparse high notes
for t, n in [(0.4, 'E5'), (1.2, 'G5'), (2.0, 'A5'), (2.8, 'G5')]:
    place(piano(n, 2.8, .4), t, pan=.2)
place(bell('C7', 2.4, .35), 1.55, pan=.4)                    # the red seal stamps in

# day: the sheet falls, folds, lands, sails
chords = [(4.0, 6.0, ['C4', 'E4', 'G4'], 'C3'), (6.0, 8.0, ['A3', 'C4', 'E4'], 'A2'),
          (8.0, 10.0, ['F3', 'A3', 'C4'], 'F2'), (10.0, 12.4, ['G3', 'B3', 'D4'], 'G2'),
          (12.4, 13.0, ['C4', 'E4', 'G4'], 'C3'),
          # night: the sea grows dark
          (13.0, 15.0, ['A3', 'C4', 'E4'], 'A2'), (15.0, 17.4, ['F3', 'A3', 'D4'], 'D2'),
          # stars fall: warmth returns
          (17.4, 19.4, ['C4', 'E4', 'G4'], 'C3'), (19.4, 21.4, ['F3', 'A3', 'C4'], 'F2'),
          (21.4, 22.6, ['G3', 'B3', 'D4'], 'G2'),
          # the shore, someone waiting
          (22.6, 24.6, ['F3', 'A3', 'C4'], 'F2'), (24.6, 26.4, ['G3', 'B3', 'D4'], 'G2'),
          (26.4, 30.0, ['C4', 'E4', 'G4', 'C5'], 'C3')]
for t0, t1, names, bass in chords:
    place(pad(names, t0, t1, .55 if t0 < 13 or t0 >= 17.4 else .42), t0)
    place(piano(bass, 3.0, .38), t0 + .02, pan=-.25)

melody = [(4.2, 'E5'), (4.8, 'G5'), (5.4, 'A5'), (6.3, 'C6'), (7.0, 'A5'), (7.6, 'G5'),
          (8.2, 'E5'), (9.0, 'D5'), (9.6, 'E5'), (10.2, 'G5'), (10.8, 'E5'), (11.6, 'D5'), (12.4, 'C5'),
          (13.6, 'A4'), (14.4, 'C5'), (15.2, 'E5'), (16.2, 'D5'),
          (22.9, 'E5'), (23.5, 'G5'), (24.1, 'A5'), (25.0, 'G5'), (25.6, 'E5'), (26.4, 'D5'),
          (27.2, 'C5'), (27.2, 'E5'), (27.2, 'G5'), (28.6, 'C6')]
for t, n in melody:
    place(piano(n, 3.0, .5), t, pan=.15)
place(piano('G4', 3.0, .3), 6.3, pan=.15)                   # the boat touches the water

# falling stars: one bell per impact, rising pentatonic, mirrored an octave below on piano
STARS_T0 = 17.4
for i, n in enumerate(['G5', 'A5', 'C6', 'D6', 'E6', 'G6', 'A6', 'C7', 'D7']):
    t = STARS_T0 + i * .5
    pan = -.6 + 1.2 * i / 8
    place(bell(n, 3.2, .55), t, pan=pan)
    place(piano(n[:-1] + str(int(n[-1]) - 1), 2.4, .25), t, pan=pan)
place(bell('E6', 3.0, .4), 29.0, pan=.3)                     # seal on the end card
place(bell('G6', 3.0, .3), 29.05, pan=-.3)

# ------------------------------------------------------------------ reverb
def reverb(x, seconds=2.8, mix=.32):
    n_ir = int(SR * seconds)
    t = np.arange(n_ir) / SR
    out = np.zeros_like(x)
    for ch in range(2):
        ir = rng.standard_normal(n_ir) * np.exp(-t * 3.2 / seconds * 2.2)
        ir[: int(.012 * SR)] = 0
        ir /= np.sqrt(np.sum(ir ** 2))
        L = len(x) + n_ir
        nfft = 1 << (L - 1).bit_length()
        wet = np.fft.irfft(np.fft.rfft(x[:, ch], nfft) * np.fft.rfft(ir, nfft), nfft)[: len(x)]
        out[:, ch] = x[:, ch] * (1 - mix) + wet * mix * 1.6
    return out


music = reverb(out_dry)

# ------------------------------------------------------------------ sea
def lowpass(x, cutoff):
    """One-pole low-pass (scipy if present, plain loop otherwise)."""
    a = np.exp(-2 * np.pi * cutoff / SR)
    try:
        from scipy.signal import lfilter
        return lfilter([1 - a], [1, -a], x)
    except ImportError:
        y = np.empty_like(x)
        acc = 0.0
        for i, v in enumerate(x):
            acc = (1 - a) * v + a * acc
            y[i] = acc
        return y


t = np.arange(N) / SR
sea = np.zeros((N, 2))
for ch in range(2):
    noise = rng.standard_normal(N)
    surf = lowpass(lowpass(noise, 520), 900)
    swell = .55 + .45 * np.sin(2 * np.pi * t / (6.5 + ch * .7) + ch * 1.3)
    sea[:, ch] = surf * swell
sea /= np.max(np.abs(sea))
sea_level = (np.interp(t, [0, 2, 4, 13, 16, 17.4, 22, 27.6, 29.5, 30], [0, .02, .10, .10, .14, .09, .08, .07, .02, 0]))
sea *= sea_level[:, None]

# splash when the boat lands
sp_len = int(SR * .9)
spt = np.arange(sp_len) / SR
splash = lowpass(rng.standard_normal(sp_len), 2500) * np.exp(-spt * 6) * np.minimum(1, spt / .01)
i0 = int(6.3 * SR)
sea[i0:i0 + sp_len] += (splash / np.max(np.abs(splash)) * .12)[:, None]

mix = music + sea

# ------------------------------------------------------------------ master
fade = np.clip((DUR - t) / .5, 0, 1) * np.clip(t / .05, 0, 1)
mix *= fade[:, None]
rms = np.sqrt(np.mean(mix ** 2))
mix *= 10 ** (-19 / 20) / rms                              # ≈ -16 LUFS after AAC, roughly
peak = np.max(np.abs(mix))
if peak > .89:
    mix = np.tanh(mix / .89) * .89                          # soft-limit the stray peaks

path = sys.argv[1] if len(sys.argv) > 1 else 'soundtrack.wav'
with wave.open(path, 'wb') as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())
print('wrote', path, f'{DUR:.1f}s')
