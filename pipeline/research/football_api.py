import requests
import os
from dotenv import load_dotenv
from openai import OpenAI
from json import loads
from pipeline.research.topic import research,score


def extract_teams(wiki_text):
    load_dotenv()
    client = OpenAI(
        base_url = "https://integrate.api.nvidia.com/v1",
        api_key = os.getenv("NVIDIA_API_KEY"))
    completion = client.chat.completions.create(
        model = "moonshotai/kimi-k3",
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


def confirm_team(player,teams_id):
    url1 = "https://v3.football.api-sports.io/players"
    load_dotenv()
    headers = {
        "x-apisports-key": os.getenv('x-apisports-key') 
    }
    confirmed=[]
    for i in teams_id:
        response = requests.get(url1, headers=headers, params={"team": i,"search": player})
        data = response.json()
        if data["results"] !=0:
            confirmed.append(i)
    return confirmed




if __name__ == "__main__":
    keywords="config/keywords.txt"
    player = score(research(keywords))  
    
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
    print(get_team_id(teams))
    print(confirm_team(player,get_team_id(teams)))
    