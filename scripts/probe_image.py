#!/usr/bin/env python3
"""Read image width/height using only the standard library.

Used by the anime-image-restyle skill to decide the output aspect ratio
when the user asks to keep the original proportions.

Usage:  python probe_image.py <image_path>
Output: one line ->  WIDTHxHEIGHT|orientation   (orientation: landscape|portrait|square|unknown)
        or           unknown|unknown
Exit code is always 0 so it never breaks the calling workflow.
"""

import struct
import sys


def read_png(data: bytes):
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", data[16:24])
    return w, h


def read_gif(data: bytes):
    if len(data) < 10 or data[:6] not in (b"GIF87a", b"GIF89a"):
        return None
    w, h = struct.unpack("<HH", data[6:10])
    return w, h


def read_bmp(data: bytes):
    if len(data) < 26 or data[:2] != b"BM":
        return None
    w, h = struct.unpack("<ii", data[18:26])
    return abs(w), abs(h)


def read_jpeg(data: bytes):
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        return None
    i = 2
    n = len(data)
    while i < n - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        if marker == 0xD9 or marker == 0xDA:
            break
        if i + 4 > n:
            return None
        seglen = struct.unpack(">H", data[i + 2:i + 4])[0]
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            if i + 9 > n:
                return None
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        if seglen < 2:
            break
        i += 2 + seglen
        if i > n:
            return None
    return None


def read_webp(data: bytes):
    if len(data) < 30 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    fmt = data[12:16]
    if fmt == b"VP8X":
        w = 1 + int.from_bytes(data[24:27], "little")
        h = 1 + int.from_bytes(data[27:30], "little")
        return w, h
    if fmt == b"VP8 ":
        w = struct.unpack("<H", data[26:28])[0] & 0x3FFF
        h = struct.unpack("<H", data[28:30])[0] & 0x3FFF
        return w, h
    if fmt == b"VP8L":
        bits = int.from_bytes(data[21:25], "little")
        w = (bits & 0x3FFF) + 1
        h = ((bits >> 14) & 0x3FFF) + 1
        return w, h
    return None


def probe(path: str):
    try:
        with open(path, "rb") as f:
            head = f.read(64)
            if len(head) < 16:
                return None
            chunk1 = head + f.read(4096)
            for reader in (read_png, read_jpeg, read_webp, read_gif, read_bmp):
                size = reader(head) or reader(chunk1)
                if size and size[0] > 0 and size[1] > 0:
                    return size
            # JPEG may have a large Exif/ICC chain; read more once.
            chunk2 = chunk1 + f.read(28672)
            size = read_jpeg(chunk2)
            if size and size[0] > 0 and size[1] > 0:
                return size
    except OSError:
        return None
    return None


def main():
    if len(sys.argv) < 2:
        print("unknown|unknown")
        return
    size = probe(sys.argv[1])
    if not size:
        print("unknown|unknown")
        return
    w, h = size
    if w == h:
        orient = "square"
    elif w > h:
        orient = "landscape"
    else:
        orient = "portrait"
    print("%dx%d|%s" % (w, h, orient))


if __name__ == "__main__":
    main()
