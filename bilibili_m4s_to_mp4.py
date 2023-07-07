import glob
import subprocess
import json
import os

# 函数源代码来源 https://www.bilibili.com/video/BV1gv4y1M7yn
def fix_m4s(
    target_path: str, output_path: str, bufsize: int = 256 * 1024 * 1024
) -> None:
    assert bufsize > 0
    with open(target_path, "rb") as target_file:
        header = target_file.read(32)
        new_header = header.replace(b"000000000", b"")
        new_header = new_header.replace(b"$", b" ")
        new_header = new_header.replace(b"avc1", b"")
        with open(output_path, "wb") as output_file:
            output_file.write(new_header)
            i = target_file.read(bufsize)
            while i:
                output_file.write(i)
                i = target_file.read(bufsize)


for root, dirs, files in os.walk("."):
    if root != ".":
        m4s_files = glob.glob("*.m4s", root_dir=root)
        mp4_file_list = []

        for m4s_file in m4s_files:
            target_path = os.path.join(root, m4s_file)
            output_path = target_path.rsplit(".", 1)[0] + ".mp4"
            fix_m4s(target_path, output_path)
            mp4_file_list.append(output_path)

        # print(mp4_file_list)

        with open(os.path.join(root, ".videoinfo"), "rb") as f:
            videoinfo = f.read()
            videoinfo = str(videoinfo, "utf-8")
            json_videoinfo = json.loads(videoinfo)
            output = json_videoinfo["title"] + ".mp4"

        subprocess.run(
            f'ffmpeg.exe -i {mp4_file_list[0]} -i {mp4_file_list[1]} -c copy "{output}"'
        )

        os.remove(mp4_file_list[0])
        os.remove(mp4_file_list[1])
