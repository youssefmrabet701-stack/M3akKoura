import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
from json import loads


def extract_teams(wiki_text):
    load_dotenv()
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = os.getenv("NVIDIA_API_KEY"))
    completion = client.chat.completions.create(
        model = "meta/llama-3.2-11b-vision-instruct",
        messages=[
        {"role": "system", "content": "You extract structured data from Wikipedia text. Given an article about a football player, identify every club team they have played for during their career. Respond with valid JSON only, no extra text — a plain JSON array of team name strings, e.g. [\"Ajax\", \"Barcelona\", \"PSG\"]."},
        {"role": "user", "content": f"Extract the list of football clubs this player played for from this text:\n\n{wiki_text}"}
        ]   
        )
    return loads(completion.choices[0].message.content)


def get_team_id(teams):
    url1 = "https://v3.football.api-sports.io/teams"
    load_dotenv()
    result = {}
    headers = {
        "x-apisports-key": os.getenv('x-apisports-key') 
    }
    for i in teams:
        response = requests.get(url1, headers=headers, params={"name": i})
        data = response.json()
        if data["results"] !=0:
            result[i]=data["response"][0]["team"]["id"]
    return result









if __name__ == "__main__":
    url2 ="https://en.wikipedia.org/w/api.php"
    headers_wiki = {"User-Agent": "M3akKoura/1.0 (youssefmrabet701@gmail.com)"}
    response2 = requests.get(url2 , headers=headers_wiki ,params = {
        "action": "query",
        "titles": "Zlatan Ibrahimovic",
        "prop": "extracts",
        "explaintext": True,
        "redirects": 1,
        "format": "json"
    })
    page = list(response2.json()["query"]["pages"].values())[0]
    wiki_text = page["extract"]
    teams = extract_teams(wiki_text)
    print(get_team_id(teams))