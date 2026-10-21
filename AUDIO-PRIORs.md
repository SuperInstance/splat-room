# AUDIO PRIORS — what the fleet's own sessions can say about a room, and what they cannot

**Seat:** the AUDIO seat (mcode)
**Branch:** `audio-priors`
**Measured from:** `/mnt/c/proart_capture/corpus/free_sessions` — 97 session bundles
**Device:** CPU, numpy + scipy, the repository's own `src/energy.py` envelope and `src/pitch.py` tracker
**Sources:** the communicator lanes' lens files (`docs/research/lens/*.json`), the walk-by study (`docs/research/walk_by_envelope.json`) and the arrival-null study (`docs/research/ARRIVAL-NULL.md`)

---

## 0. THE HEADLINE

**The programme says audio is the depth sense. On this corpus, audio is
the depth sense's BROTHER: it measures the room's acoustic envelope
crudely, it detects a mover's presence but not its direction, and it
knows nothing about position at all.**

Three priors were asked for. Here is what each one is actually worth,
measured:

| prior | verdict | the number |
|---|---|---|
| reflection timing (crude RT60) | **works, badly** | 0.254–0.368 s over 3 of 5 sessions, fitted over **0.10–0.12 s** of data and **19 dB** of decay, then extrapolated 3× |
| walk-by envelopes as mover tracks | **presence yes, direction no** | 574 crossings found; the envelope's direction agrees with the video's radial label **41.5 %** against a **39.2 %** chance level, AUC **0.5064** |
| known mic/camera positions as anchors | **no metric anchor exists** | the corpus's viewpoints span **5 px in x, 3 px in y**; the camera is a **fixed** ASUS webcam and the mic is a **separate** Realtek array |

And one finding that governs all three: **44 of the 97 sessions are an
end-to-end test rig**, not a room capture. Chrome's "Fake Default Audio
Input" and a static `.y4m` test pattern. That is **45.4 %** of the
corpus, and it is why the first cut of these measurements was wrong:
the synthetic test tone's peak of 18,064 made the microphone's gain
look like it varied **334×**, when the real microphone's spread is
**21.9×**.

---

## 1. THE CORPUS IS TWO POPULATIONS, AND THEY MUST NOT BE MIXED

Each session's `meta.json` names its own camera and its own microphone.
Read them and the corpus splits cleanly:

| device class | sessions | camera | microphone |
|---|---|---|---|
| **REAL** | **53** | ASUS FHD webcam (3277:0059) | Microphone Array (Realtek(R) Audio) |
| **SYNTHETIC** | **27** | `…\Temp\over_e2e\static.y4m` | Fake Default Audio Input |
| **UNKNOWN** | **17** | — | — (the probes) |

The synthetic rig is Chrome's end-to-end test harness: a static test
pattern for the camera and a generated tone for the microphone. Its
audio is **a 33–39 Hz dominated synthetic burst**, not a room. A
statistic that mixes the two populations is wrong by the synthetic
fraction, and the first cut of this study was wrong in exactly that way.

**This is the spec's first rule: the device label is a filter, and it is
read from `meta.json` rather than inferred from the signal.** The
loudest signal in the corpus is a test tone.

The 17 UNKNOWN sessions are the probe sessions — four of them carry a
`sonar-band` stimulus (a 16–22 kHz exponential sweep with a pink burst)
and the rest are silent.

---

## 2. THE MICROPHONE'S OWN NUMBERS

From the lens file, with the device split applied:

| | |
|---|---|
| sessions with a WAV | 97 |
| carrying digital silence | **56 (57.7 %)** |
| silent, on the **real** microphone | **47 of 53 (88.7 %)** |
| real microphone's loud-session peak range | **140 – 3,064** (a **21.9×** spread) |
| whole-corpus peak range (incl. synthetic) | 54 – 18,064 (334.5×) |
| capture rate | 48 kHz, resampled to 16 kHz by `src/wavio.py` with **no anti-aliasing** |
| the audio's lead over the video | **−6.3 to −92.3 ms** |

Three consequences for the priors.

**The gain is not a constant.** A 21.9× spread between the quietest and
loudest real session means any absolute threshold set from one session's
loudness is wrong for the next by up to 22×. Every prior below is
therefore computed **relative to the session's own floor**.

**The top of the band folds.** `src/wavio.py` resamples by linear
interpolation without an anti-aliasing filter. Measured: tones at and
below 8 kHz land where they were put (0.0 cents of error); a 10 kHz
tone arrives at 6 kHz (**−884.4 cents**); a 14 kHz tone arrives at
2 kHz (**−3,368.8 cents**). Anything in these sessions above 8 kHz is
not what it appears to be. The sonar probes' 16–22 kHz sweeps are
**entirely** in the folded region.

**The audio leads the video by up to 92 ms.** A prior that aligns an
audio event to a visual one has to correct for this, or it will blame
the room for a clock error.

---

## 3. PRIOR ONE — REFLECTION TIMING (the crude RT60)

### 3.1 The method, and why it is crude

The corpus has no impulse responses and no chirps of its own — the
laptop speaker's verdict is band NONE, so there is no actuator. What
there is instead is **speech that stops**: a source offset, followed by
the room. The method takes the energy envelope after a speech offset,
fits the decay between −5 dB below the direct sound and the session's
own noise floor, and extrapolates to 60 dB.

### 3.2 What it measures, per session

| session | noise floor | speech peak | SNR | decay rate | **RT60** | dyn range used | r² | window |
|---|---|---|---|---|---|---|---|---|
| 1792560758 | −75.9 dB | −30.4 dB | 45.5 dB | −163.1 dB/s | **0.368 s** | 16.4 dB | 0.890 | **0.12 s** |
| 1792596296 | −76.7 dB | −28.8 dB | 47.9 dB | −236.3 dB/s | **0.254 s** | 19.3 dB | 0.912 | **0.10 s** |
| 1792596354 | −77.9 dB | −31.2 dB | 46.7 dB | −180.1 dB/s | **0.333 s** | 19.7 dB | 0.847 | **0.12 s** |
| 1792596369 | −72.0 dB | −27.5 dB | 44.4 dB | −43.8 dB/s | 1.370 s | 19.6 dB | **0.371** | 0.28 s |
| 1792560597 | **−180.0 dB** | −30.2 dB | — | −21.8 dB/s | 3.500 s | 24.1 dB | **0.384** | 1.03 s |

**The three good sessions agree: RT60 0.254–0.368 s, median 0.333 s**,
at a decay rate of **−163 to −236 dB/s**. That is a plausible figure for
a small carpeted office, and it is the number the spec should carry.

### 3.3 The two bad sessions are the most informative rows in the table

**1792560597 is the negative control and it is beautiful.** Its noise
floor is **−180 dB** — digital silence, so the floor never rises to
stop the fit. The decay therefore runs for **1.03 s** over **24.1 dB**
at r² = 0.384, and the extrapolated RT60 comes out **3.5 s**. It is
wrong, and it is wrong *because the room's noise floor was removed*.
The decay it measured is the source's own tail — the speaker stopping —
not the room.

**1792596369 is the near-control:** a real floor at −72 dB, but only
44.4 dB of SNR and a fit at r² = 0.371 over 0.28 s, giving RT60 1.370 s.
It is the same failure as the negative control, milder.

**So the noise floor is not a nuisance to be normalised away. It is the
thing that terminates the measurement, and it is what makes the number
a measurement rather than a guess.** The rule that falls out:

> An RT60 estimate is only as good as the floor that stopped it. If the
> floor is at −180 dB you get the source's tail and a nonsense number;
> if the fit's r² is below about 0.8, you do not have an RT60.

### 3.4 The limit, stated as a number

The fit uses **16–20 dB** of decay over **0.10–0.12 s** of audio, and
then extrapolates to 60 dB — a **3× extrapolation beyond the data**.
The room's noise floor sits **44–48 dB below the speech**, which is
exactly what caps it: a reverberant tail 20 dB down is still 25 dB
above the floor and measurable; 40 dB down it is 5 dB above the floor
and not.

**The spec must carry the decay rate and the window, not the RT60
alone.** A reader who sees "RT60 = 0.33 s" will read it as a room
property. A reader who sees "−180 dB/s over 0.12 s, 19 dB of dynamic
range, r² 0.89, floor 45 dB below the source" will read it correctly.

### 3.5 What this prior is worth to the room model

**Worth: a coarse, per-session prior on the room's acoustic damping.**
It is one scalar per room, and it is 3× extrapolated, so it constrains
a room model's *scale* rather than its shape.

**Not worth: per-wall reflection timing.** That needs an impulse
response, an actuator, and an array. The corpus has none of the three:
the laptop speaker's band verdict is NONE, the microphone is a single
channel, and the sonar probes' 16–22 kHz sweeps are in the resampler's
folded region.

**The reopen path exists and it is the phone.** A phone speaker
(PHONE-NODE) playing a chirp from a known spot, recorded by the room's
mics, is the missing instrument. Until then, this prior is a scalar and
should be used as one.

---

## 4. PRIOR TWO — WALK-BY ENVELOPES AS MOVER TRACKS

### 4.1 What was built

A crossing detector on the camera's change map, and an envelope
extractor on the microphone, graded against each other.

**The detector.** A crossing is a **connected blob of change above the
measured noise floor (3.0 luma) that holds its shape while it
translates**: at least 4 cells wide, surviving at least 5 frames, its
centroid travelling at least 3.0 grid columns in one direction. The
blob's centroid is weighted by change magnitude, because the blob's
edge is fainter than its core.

Two earlier detectors are recorded because both produced plausible
numbers. A detector looking for a **run** of consecutive changed frames
found nothing in any session (the recorder repeats frames; the
run-length histogram is `{1: 5152, 2: 8, 3: 2}`). A detector looking
for a **burst** of change events found 54 "crossings" in 80 sessions,
and every one of them was the whole session, because the change events
are dense (a third of all frames change, median gap 3 frames).

**The envelope.** The repository's own `src/energy.py:rms_series` on a
50 ms frame with a 10 ms hop, in dB.

### 4.2 The result

**574 crossings across 80 sessions**, in 35 sessions that have any. On
the **real microphone** with a live envelope, 94 crossings:

| | |
|---|---|
| crossings with a live envelope (real mic) | **94** |
| agreeing with the video's radial label | **39 (41.5 %)** |
| chance agreement from the marginals | **39.2 %** |
| AUC of the envelope's slope at the event, TOWARD vs AWAY | **0.5064** |
| envelope's peak lands on one of the session's own speech segments | **70 (74.5 %)** |

The video's radial label comes from the blob's **apparent size**: a body
walking toward the phone grows in the picture and walking away shrinks.
It is a label, not a distance — the room map says so itself: *"Nothing
here measures a distance."*

**The envelope carries the EVENT. It does not carry the DIRECTION.**

And the reason is measured rather than guessed. At **74.5 %** of the
audio-bearing crossings the envelope's peak lands on one of the
session's own speech segments. **The hump at a crossing is Casey's own
voice**, because the crossings in this corpus are Casey seated and
gesturing — the blob's centroid sits inside the room map's person zone
at **90 %** of them — not a person walking past the microphone.

### 4.3 The Doppler question, answered

Casey's framing was that Doppler at walking speed is below threshold
and the envelope is the claim to test. The Doppler half is **confirmed**:

| | cents |
|---|---|
| Doppler shift at 1.4 m/s | **7.05** |
| the pitch tracker's own frame-to-frame step, median | **14.70** (min 11.22, max 18.26) |
| the same, 90th percentile | **74.31** (max 1195.53) |

The Doppler shift is **less than half** the tracker's own median jitter.
A shift smaller than the instrument's noise is not a measurement.

### 4.4 What this prior is worth

**Worth: a mover-presence channel.** 574 crossings across 35 sessions,
each with a time interval, a lateral direction across the frame, and an
apparent-size trend. That is a legitimate occupancy signal for a room
model, and it is the one audio-ish prior this corpus actually supports
at scale.

**Not worth: a direction.** The radial direction is chance-level, and
the reason is fixable only by capture, not by algorithm.

**The fix is a capture, and it is small.** A session with a person
walking **toward / past / away** on cue, from a fixed microphone, with
the speaker muted. The tool grades the envelope against the known
label. Until that capture exists, this prior is a presence channel and
should be labelled as one.

---

## 5. PRIOR THREE — KNOWN MIC/CAMERA POSITIONS AS ANCHORS

### 5.1 What the capture knows

| | |
|---|---|
| camera | ASUS FHD webcam (3277:0059), 640×480 requested, 160×96 luma recorded |
| microphone | Microphone Array (Realtek(R) Audio) — **a separate device** |
| camera motion | **none** — fixed, per `meta.json` |
| person zone (room map) | x 7–119, y 42–95 of a 160×96 frame |
| sessions with a mapped viewpoint | 50 |
| distinct viewpoint shifts | x ∈ {−1, 0, 4}, y ∈ {−2, −1, 0, 1} |
| **total viewpoint spread** | **5 px in x, 3 px in y** |

### 5.2 The conclusion, and it is a hard one

**There is no metric anchor in this corpus, and there cannot be one.**

The camera did not move. Across 50 mapped sessions the whole corpus's
viewpoint span is **five pixels horizontally and three vertically** —
less than the width of one of the room map's grid cells. **There is no
parallax, so there is no metric geometry to recover**, from vision or
from anything else.

The camera and the microphone are **separate devices** (an ASUS webcam
and a Realtek array), so their relative geometry is **not recorded** by
the capture. That is a fact worth knowing before anyone writes a
mic-to-camera extrinsic matrix from these sessions: the corpus does not
contain the information, and a capture that did not record it cannot
have it back-filled.

### 5.3 What the capture DOES anchor

Three things, and they are real:

1. **A person zone in image space** — x 7–119, y 42–95. The camera
   knows where the person is allowed to be, and the blob analysis finds
   them there at 90 % of crossings. That is an occupancy prior.
2. **A sound-source zone in image space** — the microphone is fixed and
   the person is fixed, so the region that produces sound is fixed.
   A room model can attribute an acoustic event to the person zone
   rather than to the walls.
3. **The clock** — `timestamps.json`, and it is the one anchor that is
   exact. The audio's lead over the video is a measured **−6.3 to
   −92.3 ms**, and correcting for it is what makes any audio↔visual
   alignment honest.

### 5.4 What this prior is worth

**Worth: an image-space anchor and a clock.** Two fixed zones and one
exact time spine.

**Not worth: a metric position.** No parallax, no recorded extrinsic.

**The unblock is the phone.** A phone that moves (PHONE-NODE) creates
parallax by moving; a phone that plays a chirp (PHONE-NODE) creates a
sound source with a known position. Those are the same phone and the
same walk, which is why the phone is the standing answer to three
different unblocks in this spec.

### 5.5 WHAT A SECOND DEVICE WOULD BUY, AND IT IS MORE THAN METRES

**This section was written before the arrival-time estimator was
measured, and the measurement changes the answer.** The companion study
(`SuperInstance/communicator`, `docs/research/ARRIVAL-NULL.md`) built
the estimator and measured it:

| | |
|---|---|
| the delay between two arrivals is measured by | the band-limited **envelope** cross-correlation, 300–3400 Hz |
| the null's bias (a signal against a gain-shifted copy of itself) | **0.0002 ms** |
| the delay-recovery error, injected delays 0–80 ms | **0.004 ms** max, **0.001 ms** median |
| **so the range resolution** | **0.0014 m** |

**And the part that matters for this spec's geometry problem: the
estimator needs NO clock relationship between the two devices.** The
delay is found by comparing the two signals *to each other*, so the
offset between their clocks cancels exactly. Measured directly: two
signals with no clock relationship and 7.3 ms between them come back as
7.0 ms, and the same pair on their own drifting clocks (0.03 % and
0.07 % fast) come back as 8.0 ms against a true 7.3 ms.

**So a second device would not need the fleet's clock doctrine fixed
first — which reverses the phone-node brief's stated order.** The
phone-node brief says the first build should be "the two-device time
base, and nothing else", because the second clock is what makes the
geometry possible. **The measurement says the time base is necessary but
not sufficient, and that the *precision* was never the problem.** What
a second device adds is:

1. **A range along one axis**, from the delay, at **0.0014 m**
   resolution — two orders of magnitude finer than the room.
2. **A metric position, if there is a second independent delay.** One
   delay gives range along one axis. *Place* needs either a third
   arrival or a prior on where the source is. This is the geometry the
   splat field actually needs, and one delay does not give it.
3. **A device-to-device latency bias**, which is a *constant* and is
   calibrated once per device pair by putting both devices at one point.

**The honest correction to this spec's §5.2:** the blocker is not
"there is no metric anchor in the corpus". It is "the corpus has one
device, so there is no delay to measure, and one delay would give range
but not place." **The second device is worth more than this spec said,
and it is worth more for the ROOM MODEL than for the acoustic prior.**

---

## 6. WHAT THE SPEC ASSUMES, AND WHAT IT MUST NOT ASSUME

**It assumes** (each with a number):

- the device label in `meta.json` is read before any statistic is
  computed — 44 of 97 sessions are a test rig (45.4 %);
- the level is relative to the session's own floor, because the real
  microphone's gain varies **21.9×**;
- the envelope is the repository's own, on the 50 ms / 10 ms grid, and
  the analysis frame's time is its **centre** (a 25 ms shift that is a
  quarter of a walking hump's width);
- the audio's lead over the video is corrected (−6.3 to −92.3 ms);
- the resampler's fold is respected, so nothing above 8 kHz is used;
- the crossing detector's noise floor is 3.0 luma, which is 2.6× the
  non-zero median change of 1.152 and ≈5× the room's motion-noise σ of
  0.61.

**It must not assume**:

- that the envelope carries a radial direction — it does not
  (41.5 % against 39.2 % chance);
- that an RT60 fitted over 19 dB is a room property — it is a 3×
  extrapolation, and without a floor to stop it the same fit returns
  3.5 s on a negative control;
- that a session's camera and microphone are co-located — they are
  separate devices and their geometry is not recorded;
- that any metric position can be recovered — the camera did not move
  by more than 5 pixels in the whole corpus;
- that the speaker's voice is not the mover — at 74.5 % of the
  audio-bearing crossings it is.

---

## 7. THE FIRST BUILD

**One calculator: `audio_prior(session) -> {rt60_s, rt60_rate_db_s,
rt60_window_s, rt60_r2, rt60_dynamic_range_db, noise_floor_db, snr_db,
mover_crossings[], clock_lead_ms}`.**

It reads one session bundle, applies the device filter, and returns
numbers. It does not fit a room and it does not make a judgement. Every
field is either a measurement or the name of the measurement's limit.

**Acceptance, as numbers:**

- it returns `rt60_s = None` (not a number) when the floor is absent
  or the fit's r² is below 0.8 — the negative control 1792560597 must
  come back `None`, not 3.5;
- it returns `rt60_window_s` and `rt60_dynamic_range_db` on every
  non-null RT60, so the extrapolation is never invisible;
- it reports the mover crossings with their *video* radial label and
  never with an audio radial label, because the audio one is not
  supported;
- it reports the device class, and refuses the synthetic sessions'
  numbers as room facts.

**The ledger row it earns.** One row per session per capture, with the
six numbers above, so the room model's acoustic prior is a *fitted
quantity with a stated uncertainty*, not a constant someone typed.

---

## 8. WHAT KILLS THIS PRIOR SET

Stated plainly, because a prior that cannot be killed is a belief.

1. **The room's sound floor kills the RT60** whenever a session's SNR
   drops below about 40 dB. The corpus's own two worst sessions show
   exactly that failure, one of them at 3.5 s. If the fleet's capture
   keeps landing on 44 dB SNR, the reflection prior stays a scalar.
2. **The speaker's own voice kills the mover-direction prior** until
   the capture mutes the speaker or moves the person. 74.5 % is not a
   margin.
3. **The fixed camera kills the metric-anchor prior** — no parallax, so
   no metric geometry from vision. **But a second AUDIO device repairs
   it**, at 0.0014 m of range resolution and with no clock relationship
   required (§5.5). The kill is on *vision alone*, not on the room.
3b. **One delay gives range, not place.** A single arrival-time
   difference gives distance along one axis. The room model needs a
   position, which needs a second independent delay — a third device,
   or a prior on where the source is. **A phone node alone does not give
   a position.** That is the strongest form of this kill and it is new.
4. **The synthetic rig kills any statistic that does not filter by
   device**, and it is 45.4 % of the corpus. This one has already
   happened once, in this document's own first draft.
5. **The absent actuator kills the impulse-response line.** The laptop
   speaker's band verdict is NONE and the corpus has no chirp of its
   own. The phone reopen is the only path, and it is not yet captured.
6. **The marker's identity kills the ultrasonic beacon.** The arrival
   survives the resampler's fold — a 12 kHz tone that aliased to 4 kHz
   was still timed to 0.1 ms — but the *identity* does not: the
   receiver cannot tell a 20 kHz sweep from a 4 kHz one. So the beacon
   is a voice-band **voxel**, and the chain must carry it honestly.

---

## 9. WHAT THE SPLAT-ROOM PIPELINE GETS, STAGE BY STAGE

| stage | what the audio priors contribute | strength |
|---|---|---|
| 0 — capture | the device label, the clock, the measured lead | **exact** |
| 1 — ASCII/edge middle | nothing | — |
| 2 — splat field (guided by ASCII + audio priors) | one acoustic damping scalar per room; a mover-presence channel | **weak but real** |
| 3 — room model | an image-space person zone; an acoustic residual to compare against a predicted RT60 | **the residual is the point** |
| 4 — Blender render | nothing | — |

**The highest-value contribution is at stage 3, and it is a residual, not
a prior.** Oracle's steal 3 — the RIR self-check, the room model must
predict its own acoustics — is the shape this takes without an
actuator: the model predicts a decay rate, the capture measures one,
and the difference is a ledger row. It is a teacher-free quality
calculator on the audio axis, which is the programme's own discipline.

---

*Measured 2026-10-21 from the corpus as it stood: 97 bundles, 53 on the
real microphone, 27 synthetic, 17 probes. The corpus is live; every
number here is a snapshot and the session list is in the results file.*

*Filed on `audio-priors` for the programme; not merged.*
