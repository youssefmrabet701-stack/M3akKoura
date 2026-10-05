from pipeline.planner.prompts import plan
import ffmpeg
from os import makedirs
from datetime import datetime
from pipeline.research.topic import research, score
import os


def cut(topic, source_video):
    makedirs("./media/segments", exist_ok=True)
    with open("media/seg.txt", "w") as f:
        st = ""
        edit_plan = plan(topic, source_video)
        if not edit_plan:
            print(
                f"plan() returned empty for topic '{topic}' — skipping cut, no segments to write"
            )
            return
        for i, clip in enumerate(edit_plan["clip_order"]):
            print(clip)
            output_path = f"./media/segments/{i}.mov"
            start = clip["start"]
            end = clip["end"]
            clip_num = int(clip["clip"].split("_")[1]) - 1
            clip_duration = source_video[clip_num]["duration"]
            if end > clip_duration:
                print(
                    f"Skipping {clip['clip']} — end {end} exceeds duration {clip_duration}"
                )
                continue
            st += "file " + output_path + "\n"
            ffmpeg.input(source_video[clip_num]["path"], ss=start, to=end).output(
                output_path
            ).run()
        if st != "":
            f.write(st[:-1])
        else:
            print("No clips written — every clip exceeded its source video's duration")


def concat():
    makedirs("./media/concatenation", exist_ok=True)
    output_path = (
        "./media/concatenation/" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".mp4"
    )
    path = "media/seg.txt"
    if not os.path.exists(path):
        print(f"{path} not found — no segments cut from video")
        return
    ffmpeg.input(path, format="concat", safe=0).output(output_path).run()
    os.remove(path)


def cut_moment(video_path, moment):
    makedirs("./media/clips", exist_ok=True)
    root, ext = os.path.splitext(os.path.basename(video_path))
    start = max(0, moment["frame"] - 2)
    end = moment["frame"] + 2
    output_path = f"./media/clips/{root}_{moment['frame']}.mov"
    ffmpeg.input(video_path, ss=start, to=end).output(output_path).run()
    return {
        "path": output_path,
        "description": moment["reason"],
        "start": start,
        "end": end,
        "duration": end - start,
    }


def organize_clips(vids_moments):
    l = []
    for video_path in vids_moments:
        for i in vids_moments[video_path]:
            l.append(cut_moment(video_path, i))
    return l
