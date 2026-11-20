#!/usr/bin/env python3
"""Render LOW WATER: Half a Step from individually generated ElevenLabs actor takes.
Licensed/owned performances generated for this author's fictional audio drama.
"""
import json, math, os, re, subprocess, time, urllib.request
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "manifest.json"
OUT = ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)
AUDIO = ROOT / ".raw_clips"
AUDIO.mkdir(exist_ok=True)
SR = 44100
cast = {"W":"Winnie Kask", "Y":"Yoli Pruneda", "K":"Kino Benavides", "N":"June"}
manifest = json.loads(MANIFEST.read_text())
clips = manifest["clips"]
assets = manifest["assets"]
assert len(clips) == 58 and [c["index"] for c in clips] == list(range(1, 59)), "Expected 58 ordered dialogue clips"

def download(url, target):
    if target.exists() and target.stat().st_size > 500:
        return target
    for attempt in range(3):
        try:
            req=urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0 LowWaterAudioProduction/1.0","Accept":"audio/mpeg,*/*"})
            with urllib.request.urlopen(req, timeout=45) as resp:
                b=resp.read()
            if len(b)<500:
                raise RuntimeError("Audio response was unexpectedly short")
            target.write_bytes(b)
            return target
        except Exception:
            if attempt == 2: raise
            time.sleep(2 * (attempt + 1))

def decode(path, phone=False, kino=False):
    af = "highpass=f=270,lowpass=f=3200,acompressor=threshold=0.22:ratio=2:attack=12:release=100" if phone else ("highpass=f=115,lowpass=f=8800" if kino else "highpass=f=85,lowpass=f=12000")
    cmd=["ffmpeg","-nostdin","-v","error","-i",str(path),"-af",af,"-ac","1","-ar",str(SR),"-f","f32le","pipe:1"]
    raw=subprocess.check_output(cmd)
    return np.frombuffer(raw, dtype="<f4").copy()

print("Downloading and decoding generated ElevenLabs character performances...")
voice_audio=[]
for c in clips:
    p=download(c["url"], AUDIO / f"{c['index']:02d}.mp3")
    a=decode(p,phone=c["speaker"] in ("Y","N"),kino=c["speaker"]=="K")
    # Quiet, close-miked radio voices; preserve delivery, breaths and natural dynamics.
    rms=float(np.sqrt(np.mean(a*a)+1e-10))
    desired=.125 if c["speaker"]=="W" else (.112 if c["speaker"]=="K" else .105)
    a*=min(2.3,desired/max(.001,rms))
    mx=float(np.max(np.abs(a))) if len(a) else 1
    if mx>.88: a*=.88/mx
    ns=min(len(a)//12,int(.035*SR))
    if ns>0:
        a[:ns]*=np.linspace(0,1,ns,dtype=np.float32)
        a[-ns:]*=np.linspace(1,0,ns,dtype=np.float32)
    voice_audio.append(a)

print("Downloading and decoding ElevenLabs environmental effects...")
fx={}
for name,obj in assets.items():
    if not obj.get("url"): continue
    p=download(obj["url"], AUDIO/f"ambience_{name}.mp3")
    fx[name]=decode(p)

# Natural, responsive conversational pacing. Keep radio silences where the mystery demands them.
gap_special={1:.42, 2:.72, 7:.55, 18:.75, 19:.25, 20:.45, 22:.48,
             33:.6, 39:.46, 41:.55, 43:.35, 48:.62, 49:.56,
             53:.95, 54:.48, 55:1.55, 56:1.4, 57:.45, 58:.55}
timeline=[]
cursor=.55
for c,a in zip(clips,voice_audio):
    index=c["index"]
    if index>1:
        cursor+=gap_special.get(index,.34 if c["speaker"] != clips[index-2]["speaker"] else .43)
    timeline.append((cursor,index,c,a))
    cursor+=len(a)/SR
end=cursor+4.5
n=int(end*SR)
mix=np.zeros(n,dtype=np.float32)

def add(seg,start,vol=1.0):
    off=int(start*SR)
    if off<0: seg=seg[-off:];off=0
    m=min(len(seg),n-off)
    if m>0: mix[off:off+m]+=seg[:m]*vol

for start,index,c,a in timeline: add(a,start)
times={i:start for start,i,c,a in timeline}
print("Main dialogue duration: %.2f minutes" % (cursor/60.))

def spread_loop(sound,vol):
    if sound is None or not len(sound): return
    # Separate repetitions with tiny crossfades to avoid perceptible seams.
    ss=np.copy(sound)
    mx=max(float(np.max(np.abs(ss))),.001)
    ss*=vol/mx
    period=len(ss)
    if period>SR:
        cross=min(SR//3,period//8)
        for j in range(cross):
            t=j/max(1,cross-1)
            ss[j]=ss[j]*t+ss[-cross+j]*(1-t)
        period-=cross
    for off in range(0,n,period):
        endp=min(period,n-off)
        mix[off:off+endp]+=ss[:endp]

spread_loop(fx.get("studio"),.007)
spread_loop(fx.get("flume"),.014)

# The audible legend: steady power-flume note, falling a semitone and ultimately recovering.
# Smooth frequencies ensure no click and let the listener decide what they heard.
lower=110.0*2**(-1/12)
fall_start=times.get(4,45)+2
fall_end=fall_start+3.2
rise_start=times.get(55,end-48)
rise_end=rise_start+4.5
phase=0.
step=10*SR
for start in range(0,n,step):
    endidx=min(n,start+step)
    t=np.arange(start,endidx,dtype=np.float64)/SR
    hz=np.full(len(t),110.0)
    down=(t>=fall_start)&(t<fall_end)
    hz[down]=110.0-(110.0-lower)*((t[down]-fall_start)/(fall_end-fall_start))
    stay=(t>=fall_end)&(t<rise_start)
    hz[stay]=lower
    up=(t>=rise_start)&(t<rise_end)
    hz[up]=lower+(110.0-lower)*((t[up]-rise_start)/(rise_end-rise_start))
    wavephase=phase+2*math.pi*np.cumsum(hz)/SR
    phase=float(wavephase[-1]%(2*math.pi))
    bed=(np.sin(wavephase)*.0027 + np.sin(wavephase*2+.8)*.0007).astype(np.float32)
    mix[start:endidx]+=bed

# Very quiet hiss/static at the tune-in and signal-tail, no melodramatic stingers.
rng=np.random.default_rng(91422)
for a,b,amp in [(0,.55,.009),(end-2.9,end,.0035)]:
    st=max(0,int(a*SR)); en=min(n,int(b*SR))
    if en>st:
        noise=rng.standard_normal(en-st).astype(np.float32)
        env=np.sin(np.linspace(0,math.pi,en-st))**2
        mix[st:en]+=noise*env.astype(np.float32)*amp

# The car catches while Yoli is beside the wagon, before June thanks her.
if fx.get("engine") is not None:
    eng=fx["engine"]
    mx=max(float(np.max(np.abs(eng))),.001)
    eng=(eng/mx)*.036
    # At the end of Yoli's jump start instruction, bridge to June's relieved response.
    pos=times.get(49,cursor)-min(len(eng)/SR,4.0)-.08
    add(eng,max(0,pos))

# Distant Choke foghorn twice, present as scenery, not a supernatural cue.
for t0 in [145., min(end-85,390.)]:
    if t0<0: continue
    count=int(3.4*SR)
    ts=np.arange(count,dtype=np.float32)/SR
    env=np.minimum(1.,np.minimum(ts/0.6,(3.4-ts)/.8)).clip(0)
    horn=(np.sin(2*math.pi*86*ts)+.3*np.sin(2*math.pi*172*ts))*.007*env
    add(horn.astype(np.float32),t0)

# Subtle global limiter.
mix=np.tanh(mix*1.1)
peak=max(float(np.max(np.abs(mix))),.001)
mix*=(.9/peak)
pcm=OUT/"half_a_step.pcm"
mix.astype("<f4").tofile(pcm)
mp3=OUT/"LOW_WATER_Half_a_Step_Full_Cast.mp3"
subprocess.check_call(["ffmpeg","-y","-nostdin","-v","error","-f","f32le","-ar",str(SR),"-ac","1","-i",str(pcm),"-af","loudnorm=I=-16:TP=-1.5:LRA=11","-ac","2","-ar","44100","-codec:a","libmp3lame","-b:a","192k",str(mp3)])
pcm.unlink(missing_ok=True)
transcript="# LOW WATER — Half a Step\n\nNeptune Public Radio · A fictional full-cast broadcast · 3:11 a.m.\n\n"
transcript+="**Cast:** Winnie Kask, Yoli Pruneda, Kino Benavides, June.\n\n"
for c in clips:
    clean=re.sub(r"\[[^\]]+\]\s*","",c["prompt"]).strip()
    transcript+=f"**{cast[c['speaker']]}:** {clean}\n\n"
(OUT/"LOW_WATER_Half_a_Step_Transcript.md").write_text(transcript)
print(f"RENDER_COMPLETE path={mp3} bytes={mp3.stat().st_size} duration_seconds={end:.2f}")
