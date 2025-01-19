# Phase correlation visualiser 
This visualiser is inspired by the [Calf Analyser's](https://calf-studio-gear.org/doc/Analyzer.html) phase correlation diagram. 
It uses either volume or phase of left and right channels as coordinates to set position for a 
particle emitter in two-dimensional space. There are also some moving reflective surfaces to make the scene more interesting.

<p float="left">
  <img title="Calf" src="assets/calf_render.gif" width="32%"/>
  <img src="assets/phase_approx.gif" width="32%" /> 
  <img src="assets/phase_true.gif" width="32%" />
  <figcaption>Figure 1. The same audio visualised by Calf's phase correlation, volume correlation and phase correlation in Blender. </figcaption>
</p>

## Files
* `phase_correlation_approx.blend` - left/right channel volume correlation (middle picture in Fig.1). 
* `phase_correlation_true.blend` - left/right phase correlation (right picture in Fig.1). 
* `split_audio_channels.sh` - uses `ffmpeg` to split stereo audio-file into two mono files. Use it with `phase_correlation_approx.blend`.
* `split_phase.py` - since Blender's `Sound to Curve` method get rids of phase information we need to manually split waveform 
into positive and negative parts in case we want to compute true phase correlation. 
This script splits stereo file into four: negative and positive phases for each channel. Use it with `phase_correlation_true.blend`. 
It requires `librosa`, `soundfile` and `numpy` Python modules. 

## Usage
If you want to use it for your sound, in both blend files you need to edit `Geometry Nodes` of `Dots` object. 
<p float="left">
  <img align="middle" src="assets/nodes_true.png" width="32%"/>
  <img align="middle" src="assets/params_true.png" width="67%"/>

  <figcaption>Figure 2. Visualiser's nodes to edit and parameters. </figcaption>
</p>

Red nodes labelled as `left_p`, `left_n`, `right_p`, `right_n` (or `left`, `right` in `phase_correlation_approx.blend`) 
should be animated using Blender's feature `Channel`->`Sound to Samples` in [Graph Editor](https://docs.blender.org/manual/en/latest/editors/graph_editor/channels/editing.html).
Use corresponding files 
produced by `split_phase.py` as sound source. 
To get the most interesting result, 
I recommend to use the least attack and release for envelope parameters when importing audio file.

You also may want to edit GM's attributes in the modifier tab (see Fig. 2):

* **Amplitude** controls overall spreadness of the point cloud.
* **Side/mid ratio** sets ratio between two axes. If your track is not very wide, you may want to set this parameter higher.
* **Scale** controls dots' size.
* **Max Age** lifetime of particles. Note that you also may want to edit fadeout parameter for particle's material, since those two
parameters are not linked.
* **Sparsity** controls the frequency with which particles are generated.
* **Speed** controls the speed of particles' movement along Z axis.

Also note that the simulation is hungry for RAM (I haven't found a way to optimize it), so you may want to render it in chunks. 

# Understanding computations using Python

In `phase_correlation_true.blend` geometry nodes compute positions of the particle emitter according to the following formulas written in Python:

```python
import matplotlib.pyplot as plt
import librosa as rs
w, sr = rs.load('stereo.wav', mono=False)
mid = w[0, :] + w[1, :]
side = w[0, :] - w[1, :]
pos = sr * 10  # 10 seconds from start
window = 500
plt.scatter(side[pos - window: pos + window], mid[pos - window: pos + window])
```

<p float="left">
  <img align="middle" src="assets/phase_corr.png" width="49%"/>
  <figcaption>Figure 3. Phase correlation. </figcaption>
</p>

That is, we first transform stereo signal into **mid/side** then plot 2D points with corresponding values as coordinates. I.e. if left and right phases coincide, we will get zero on **side** axis, such points will be positioned vertically. In contrast, more stereo signal should be vaster spread horizontally, since **side** signal is less likely to be zero in that case.

The problem with that approach is that Blender's `Sound to Curve` doesn't preserve phase information. So, initially, it led me to another method in `phase_correlation_approx.blend`:

```python
import numpy as np
v = np.abs(w)  # get rid of phase information
mid = v[0, :] + v[1, :]
side = v[0, :] - v[1, :]

# moving average
sliding_window = 100
kernel = np.ones(sliding_window)/sliding_window
mid_mean = np.convolve(mid, kernel, mode='same')
side_mean = np.convolve(side, kernel, mode='same')

mid_c = mid - mid_mean
side_c = side - side_mean
plt.scatter(
	side_c[pos - window: pos + window], 
	mid_c[pos - window: pos + window]
)
```
<p float="left">
  <img align="middle" src="assets/volume_corr.png" width="49%"/>
  <figcaption>Figure 4. Volume correlation. </figcaption>
</p>

That is, instead of phase information we measure deviation of the volume from its sliding average. So, basically, we plot volume [covariance](https://en.wikipedia.org/wiki/Correlation) instead in 2D. Sliding average is quite tricky to compute in Geometry Nodes, so, actually, I just approximate it with [exponential](https://en.wikipedia.org/wiki/Moving_average) average.

Obviously, the results look differently (see Fig. 3 and Fig. 4), but I found that they both have its own aesthetics, so I preserved both variants. 

# Anknowledgents
Thanks to **sadko4u** from [Linux Musicians](https://linuxmusicians.com/viewtopic.php?t=27889) forum for helping me to understand Calf Analyser's inner workings.