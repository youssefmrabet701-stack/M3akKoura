import os
from openai import OpenAI
from dotenv import load_dotenv
from json import loads

def clip_descriptor(clips):
    res = ""
    for idx,i in enumerate(clips):
        res+= f"clip_{idx+1}: max_duration: {i['duration']} description: {i['description']} \n"
    return res

def plan(topic,clips):
    load_dotenv()

    client = OpenAI(
    base_url = "https://integrate.api.nvidia.com/v1",
    api_key = os.getenv("NVIDIA_API_KEY")
    )
    completion = client.chat.completions.create(
        model="meta/llama-3.2-11b-vision-instruct",
        messages=[{"role":"system","content":"You are an expert short-form football video editor specializing in TikTok reels. You create precise, beat-driven edit plans. You only use clips provided to you — never invent clip names. Always respond with valid JSON only, no extra text."},{"role" : "user","content": f"""Create a detailed edit plan for a football reel about: {topic}

        Available clips:
        {clip_descriptor(clips)}

        The plan must include: clip order, source timestamps for each clip, video timeline timestamps, cut points, transition types, caption text and timing, hook, ending, total duration (max 60s), and pacing style. Always return JSON with exactly this structure:
{{
  "clip_order": [
    {{"clip": "clip_1", "start": 0, "end": 3.5}}
  ],
  "total_duration": 30
}} 
source timestamps for each clip must not exceed that clip's max_duration.
For each clip, start and end must be between 0 and that clip's max_duration. These are timestamps within the clip itself, not the global timeline."""}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=False)
    return loads(completion.choices[0].message.content)
if __name__ == "__main__":
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
    topic="Ronaldo vs Bayern 2017"
    print(plan(topic,source_video))