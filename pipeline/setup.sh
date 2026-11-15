#!/usr/bin/env bash
# Prepare a fresh cloud workspace. Safe to run twice.
set -e
pip install --break-system-packages -q kokoro-onnx soundfile skia-python numpy 2>&1 | grep -v WARNING || true
D=/home/claude/.cache/kokoro; mkdir -p $D
[ -s $D/kokoro.onnx ] || curl -sSL -o $D/kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
[ -s $D/voices.bin ] || curl -sSL -o $D/voices.bin https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
for f in "Lora" "Inter" "Courier 10 Pitch" "TeX Gyre Pagella"; do fc-list | grep -qi "$f" || echo "MISSING FONT: $f"; done
which ffmpeg >/dev/null || echo "MISSING ffmpeg"
echo setup ok
