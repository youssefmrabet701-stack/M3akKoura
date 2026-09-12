from pytrends.request import TrendReq

pytrends = TrendReq(hl='en-US', tz=360)

def research(keywords):
    with open(keywords,'r') as file:
        kw_list =  [line.strip("\n") for line in file.readlines()]
        kw_list = kw_list[:5]
        pytrends.build_payload(kw_list, cat=0, timeframe='today 5-y', geo='', gprop='')
        return pytrends.interest_over_time()
    

def score(df):
    scores={}
    df = df.drop(columns=['isPartial'])
    for i in df.columns:
        E = df[i].iloc[-1]
        previous_avg = df[i].iloc[:-1].mean()
        G = E/previous_avg if previous_avg !=0 else 0
        score = 0.6 * G + 0.4 * E
        scores[i] = score
    return max(scores, key=scores.get)


def get_player():
    keywords="config/keywords.txt"
    return score(research(keywords))
