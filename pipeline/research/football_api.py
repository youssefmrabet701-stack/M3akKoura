import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
from json import loads


def extract_teams(wiki_text):
    try:
        load_dotenv()
        client = OpenAI(
            base_url = "https://integrate.api.nvidia.com/v1",
            api_key = os.getenv("NVIDIA_API_KEY"))
        completion = client.chat.completions.create(
            model = "moonshotai/kimi-k3",
            messages=[
            {"role": "system", "content": "You extract structured data from Wikipedia text. Given an article about a football player, identify every club team they have played for during their career. Respond with valid JSON only, no extra text — a plain JSON array of team name strings, e.g. [\"Ajax\", \"Barcelona\", \"PSG\"]."},
            {"role": "user", "content": f"Extract the list of senior football clubs this player played for, starting from their professional/senior debut. Exclude youth academies, school teams, and reserve/B-teams. Only include a club if the text indicates a genuine first-team career there — not a brief trial, loan with no minutes, or single cameo appearance. If the text gives an appearance count for a club and it's below 30, exclude that club. If no appearance count is mentioned for a club, use context (multiple seasons, described as a 'key player,' major trophies won there, etc.) to judge whether it was a real senior career stop — do not fabricate a specific number.:\n\n{wiki_text}"}
            ]   
        )
        return loads(completion.choices[0].message.content)
    except:
        print("error extracting teams")
        return []


def get_player_teams(player):
    url2 ="https://en.wikipedia.org/w/api.php"
    headers_wiki = {"User-Agent": "M3akKoura/1.0 (youssefmrabet701@gmail.com)"}
    response2 = requests.get(url2 , headers=headers_wiki ,params = {
        "action": "query",
        "titles": player,
        "prop": "extracts",
        "explaintext": True,
        "redirects": 1,
        "format": "json"
    })
    page = list(response2.json()["query"]["pages"].values())[0]
    wiki_text = page["extract"]
    teams = extract_teams(wiki_text)
    return teams


