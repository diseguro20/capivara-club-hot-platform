import os
import subprocess
import sys
import time

files = [
    "videos-tutoriais/tutorial-01.mp4",
    "videos-tutoriais/tutorial-02.mp4",
    "videos-tutoriais/tutorial-03.mp4",
    "videos-tutoriais/tutorial-04.mp4",
    "videos-tutoriais/tutorial-05.mp4",
    "videos-tutoriais/tutorial-06.mp4",
    "videos-tutoriais/tutorial-07.mp4",
    "videos-tutoriais/tutorial-08.mp4",
]

tag = "v1.0.0-videos"

print(f"Starting upload of {len(files)} tutorial videos to GitHub Release {tag}...")

for idx, fpath in enumerate(files, 1):
    if not os.path.exists(fpath):
        print(f"[{idx}/{len(files)}] File not found: {fpath}, skipping.")
        continue
    size_mb = os.path.getsize(fpath) / (1024 * 1024)
    print(f"\n[{idx}/{len(files)}] Uploading {fpath} ({size_mb:.1f} MB)...", flush=True)
    t0 = time.time()
    cmd = ["gh", "release", "upload", tag, fpath, "--clobber"]
    ret = subprocess.run(cmd, capture_output=True, text=True)
    if ret.returncode == 0:
        elapsed = time.time() - t0
        speed = size_mb / max(0.1, elapsed)
        print(f"[{idx}/{len(files)}] Done in {elapsed:.1f}s ({speed:.2f} MB/s)!", flush=True)
    else:
        print(f"[{idx}/{len(files)}] Upload failed: {ret.stderr}", flush=True)

print("\nAll tutorial videos upload process completed!")
