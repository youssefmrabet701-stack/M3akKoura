import subprocess
from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
from json import loads
from shutil import rmtree


def extract_frame(video_path, output_folder):
    subprocess.run(["ffmpeg", "-i", video_path, "-vf", "fps=1/5", f"{output_folder}/frame_%04d.jpg"])

def describe_frame(image_path):
    with open(image_path, "rb") as f:
        encoded_image = base64.b64encode(f.read()).decode("utf-8")
    load_dotenv()
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = os.getenv("NVIDIA_API_KEY"))
    completion = client.chat.completions.create(
    model="meta/llama-3.2-11b-vision-instruct",
    messages=[
        {"role": "system", "content": "You are analyzing frames from a football (soccer) highlight video, one frame at a time. Describe only what is visibly happening — player actions, ball position, celebrations, replays, crowd reactions. Be concise, factual, and specific. If the frame shows a goal being scored or celebrated, say so explicitly."},
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}},
                {"type": "text", "text": "Describe this frame in one or two sentences, focusing on player action, ball position, and whether this looks like a goal moment, celebration, replay, or neutral gameplay."}
            ]
        }
    ],
    max_tokens=256)
    return completion.choices[0].message.content
    
def describe_all_frames(folder):
    desc = []
    files = os.listdir("media/frames/")
    for i in files:
        desc.append(describe_frame(os.path.join(folder, i)))
    return desc    

def pick_best_moments(descriptions):
    string=""
    for i,d in enumerate(descriptions):
        string += f"frame {i*5} : {d}\n"
    load_dotenv()
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = os.getenv("NVIDIA_API_KEY"))
    completion = client.chat.completions.create(
        model="moonshotai/kimi-k3",
        messages=[
            {
                "role": "system",
                "content": "You are analyzing a sequence of frame-by-frame descriptions from a football highlight video, taken every 5 seconds. Identify which frame numbers correspond to actual goal moments or celebrations worth using as a video clip. Respond with valid JSON only: a list of objects, each with 'frame' (the frame number) and 'reason' (short explanation)."
            },
            {
                "role": "user",
                "content": f"Here are the frame descriptions:\n\n{string}\n\nWhich frames show real goal moments or celebrations worth clipping?"
            }
        ]
    )

    return loads(completion.choices[0].message.content)

def clear_frames(folder):
    rmtree(folder)
    os.mkdir(folder)

def analyze_video(video_path):
    output_path= "media/frames/"
    extract_frame(video_path,output_path)
    descriptions = describe_all_frames(output_path)
    clear_frames(output_path)
    return pick_best_moments(descriptions)