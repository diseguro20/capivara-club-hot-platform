import av
import os
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

input_path = "videos-tutoriais/tutorial-08.mp4"
output_path = "videos-tutoriais/tutorial-08-h264.mp4"

print(f"Reading {input_path}...")
in_container = av.open(input_path)
in_video = in_container.streams.video[0]
in_audio = in_container.streams.audio[0] if in_container.streams.audio else None

print(f"Input video: codec={in_video.codec_context.name}, {in_video.width}x{in_video.height}, {float(in_video.average_rate)} fps")
print(f"Input audio: codec={in_audio.codec_context.name if in_audio else 'None'}")

# Prepare output container
out_container = av.open(output_path, 'w', format='mp4', options={'movflags': 'faststart'})

# Choose encoder: prefer h264_nvenc if supported, else libx264
encoder_name = 'h264_nvenc'
try:
    test_stream = out_container.add_stream('h264_nvenc', rate=in_video.average_rate)
    test_stream.width = in_video.width
    test_stream.height = in_video.height
    test_stream.pix_fmt = 'yuv420p'
    test_stream.options = {'preset': 'p4', 'cq': '22'}
    out_video = test_stream
    print("Using NVIDIA NVENC hardware encoder (h264_nvenc)")
except Exception as e:
    encoder_name = 'libx264'
    print(f"NVENC failed ({e}), falling back to libx264...")
    out_video = out_container.add_stream('libx264', rate=in_video.average_rate)
    out_video.width = in_video.width
    out_video.height = in_video.height
    out_video.pix_fmt = 'yuv420p'
    out_video.options = {'preset': 'fast', 'crf': '22'}

out_video.time_base = in_video.time_base

# Add audio stream - copy AAC from template
out_audio = None
if in_audio:
    out_audio = out_container.add_stream_from_template(in_audio)

print("Starting transcode to universal H.264...")
t0 = time.time()
frame_count = 0
audio_pkt_count = 0

for packet in in_container.demux():
    if packet.stream == in_video:
        for frame in packet.decode():
            frame_count += 1
            # Send frame to out_video encoder
            for out_packet in out_video.encode(frame):
                out_container.mux(out_packet)
            if frame_count % 1000 == 0:
                elapsed = time.time() - t0
                fps = frame_count / max(0.1, elapsed)
                print(f"  Processed {frame_count} frames ({elapsed:.1f}s, {fps:.1f} fps)...", flush=True)
    elif packet.stream == in_audio and out_audio:
        if packet.dts is not None:
            packet.stream = out_audio
            out_container.mux(packet)
            audio_pkt_count += 1

# Flush video encoder
for out_packet in out_video.encode():
    out_container.mux(out_packet)

out_container.close()
in_container.close()

elapsed = time.time() - t0
size_mb = os.path.getsize(output_path) / (1024 * 1024)
print(f"\nTranscode completed in {elapsed:.1f}s!")
print(f"Output file: {output_path} ({size_mb:.1f} MB, {frame_count} frames, {audio_pkt_count} audio packets)")
