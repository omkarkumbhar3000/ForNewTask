# The two programs tools/optimize_media.py needs, in a throw-away image, so nothing is installed on the
# machine: ffmpeg (lossless MP4 remux) and Pillow (JPEG, PNG, WebP and AVIF). Development only; never shipped.
#
#   docker build -f tools/mediatool.Dockerfile -t cc-mediatool .
#   docker run --rm -v "${PWD}:/work" -w /work cc-mediatool python tools/optimize_media.py [--dry-run]
FROM python:3.12-slim
COPY --from=mwader/static-ffmpeg:7.1 /ffmpeg /ffprobe /usr/local/bin/
RUN pip install --no-cache-dir "pillow==11.3.0"
