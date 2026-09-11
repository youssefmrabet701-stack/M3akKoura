from pipeline.planner.prompts import plan
from ffmpeg import input
from os import makedirs
from datetime import datetime
from pipeline.research.topic import research,score


#cut source video into segments
def cut(topic,source_video):
    #make directory if it doesnt exist
    makedirs("./media/segments", exist_ok=True)
    with open("seg.txt",'w') as f:
        st = ""
        edit_plan=plan(topic,source_video)
        for i,clip in enumerate(edit_plan['clip_order']):
            print(clip)
            output_path = f"./media/segments/{i}.mov"
            start=clip['start']
            end = clip['end']
            clip_num = int(clip['clip'].split('_')[1]) - 1
            clip_duration = source_video[clip_num]['duration']
            if end > clip_duration:
                print(f"Skipping {clip['clip']} — end {end} exceeds duration {clip_duration}")
                continue
            st+="file "+output_path+"\n"
            input(source_video[clip_num]['path'], ss=start, to=end).output(output_path).run()
        f.write(st[:-1])
        f.close()
    
#concatenate segments
def concat():
    #make directory if it doesnt exist
    makedirs("./media/concatenation", exist_ok=True)
    output_path="./media/concatenation/"+datetime.now().strftime("%Y%m%d_%H%M%S")+".mp4"
    with open("seg.txt",'r') as f:
        input('seg.txt', format='concat', safe=0).output(output_path).run()
        f.close()
    
    
    

r = research("research/keywords.txt")
topic = score(r)
source_video = [
    {
        "path": "./media/clips/2.mov",
        "description": "Cristiano Ronaldo attacking sequence against Bayern Munich, carrying the ball toward the penalty area before finishing the move near goal",
        "duration": 6.79
    },
    {
        "path": "./media/clips/3.mov",
        "description": "Cristiano Ronaldo and Real Madrid players during the aftermath of the attacking play, with Bayern Munich players nearby; close-up of the players",
        "duration": 3.44
    },
    {
        "path": "./media/clips/4.mov",
        "description": "Real Madrid attacking Bayern Munich from midfield, progressing the ball toward the penalty area in a wide match view",
        "duration": 7.76
    },
    {
        "path": "./media/clips/5.mov",
        "description": "Real Madrid attacking near Bayern Munich's penalty area, ending with Cristiano Ronaldo visible celebrating after the scoring action",
        "duration": 8.34
    },
    {
        "path": "./media/clips/6.mov",
        "description": "Close-up of Cristiano Ronaldo celebrating on the pitch, smiling and reacting to the successful play; strong reaction shot suitable for an ending",
        "duration": 11.52
    },
    {
    "path": "./media/clips/1.mov",
    "description": "Cristiano Ronaldo and Real Madrid attacking Bayern Munich on a fast counterattack, carrying the ball from midfield toward the penalty area before creating a dangerous scoring opportunity near goal",
    "duration": 7.32
    }
]

cut(topic,source_video)
concat()
