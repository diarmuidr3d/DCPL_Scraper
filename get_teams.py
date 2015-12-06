from lxml import html
import requests


def get_team_info(tree):
    team_name = str(tree.xpath("/html/body/div/div[3]/h2/text()")[0]).replace(" Fixtures & Profile", "")
    if len(team_name) > 1:
        division = tree.xpath("/html/body/div/div[3]/div[2]/table/tr[2]/td/text()")[0]
        results = get_results(tree)
        players = get_players(tree)
        print(team_name, "-", division, results, players)


def get_results(tree):
    results = tree.xpath("/html/body/div/div[3]/div[1]/table/tr")
    ret = []
    for row in results:
        team1 = row.xpath("td[2]//text()")
        if len(team1) > 0:
            date = row.xpath("td[1]/a/text()")[0]
            team1 = team1[0]
            score = row.xpath("td[3]//text()")[0]
            score1 = str(score[:score.index("-")]).strip()
            score2 = str(score[score.index("-")+1:]).strip()
            team2 = row.xpath("td[4]//text()")[0]
            ret.append({"team1": {"name": team1, "score": score1}, "team2": {"name": team2, "score": score2}})
    return ret


def get_players(tree):
    players = tree.xpath("/html/body/div/div[3]/div[5]/table/tr/td[2]/text()")
    numbers = tree.xpath("/html/body/div/div[3]/div[5]/table/tr/td[1]/text()")
    team = []
    thing = list(map(lambda name, num: team.append({"name": name, "num": num}), players, numbers))
    return team

url = "http://dublincanoepolo.ie/profile.php?teamid="

i = 0
while i < 1500:
    this_url = url + str(i)
    print(this_url)
    page = requests.get(this_url)
    tree = html.fromstring(page.content)
    get_team_info(tree)
    i += 1