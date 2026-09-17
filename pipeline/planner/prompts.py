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
    try:
        load_dotenv()
        client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = os.getenv("NVIDIA_API_KEY")
        )
        completion = client.chat.completions.create(
            model = "moonshotai/kimi-k3",
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
        top_p=0.95,
        max_tokens=4096,
        stream=False)
        return loads(completion.choices[0].message.content)
    except:
        return {}