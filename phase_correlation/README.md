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
* `split_phase.py` - Since blender's `sound to curve` get rids of phase information we need to manually split waveform 
into positive and negative parts in case we want to compute true phase correlation. 
This script splits stereo file into four: negative and positive phases for each channel. Use it with `phase_correlation_true.blend`. 
It requires `librosa`, `soundfile` and `numpy` Python modules. 

## Usage
If you want to use it for your sound, in both blend files you need to edit `Geometry Nodes` for `Dots` object. 
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

You also may want to edit GM's attributes in the modifier tab:

* **Amplitude** controls overall spreadness of the point cloud.
* **Side/mid ratio** sets ratio between two axes. If your track is not very wide, you may want to set this parameter higher.
* **Scale** controls dots' size.
* **Max Age** lifetime of particles. Note that you also may want to edit fadeout parameter for particle's material, since those two
parameters are not linked.
* **Sparsity** controls the frequency with which particles are generated.
* **Speed** controls the speed of particles' movement along Z axis. 

