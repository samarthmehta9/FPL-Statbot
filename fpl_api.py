import pandas as pd
from prettytable import PrettyTable
from fpl import FPL
import aiohttp
import asyncio
 
from quart import Quart, render_template, redirect, url_for, request

app = Quart(__name__)

@app.route("/")
async def index():
	return await render_template('index.html')

@app.route('/', methods=['POST'])
async def getdata():
    variable = (await request.form)["search"]
    if (variable == 'goals'):
    	await getmostgoalscored()
    #return variable

async def getplayer(name):
	session = aiohttp.ClientSession()
	fpl = FPL(session)
	df = pd.read_csv("fpl_ids.csv")
	fpl_id = df.loc[df['web_name']==name,'22-23'].values[0]
	player = await fpl.get_player(fpl_id, return_json = True )
	#print(player)
	print(player['web_name'])
	return player
	await session.close()


async def getmostgoalscored():
	session = aiohttp.ClientSession()
	fpl = FPL(session)
	players = await fpl.get_players()
	top_performers = sorted(
	players, key=lambda x: x.goals_scored, reverse=True)
	player_table = PrettyTable(["Player", "£", "Team", "G", "Total Points"])
	for player in top_performers[:10]:
		goals = player.goals_scored
		team = await fpl.get_team(player.team)
		team = str(team)
		
		player_table.add_row([player.web_name, f"£{player.now_cost / 10}",team, goals, player.total_points])

	print(player_table)
	x = player_table.get_string()
	return x
	await session.close()



#asyncio.run(getplayer('Saliba'))
#asyncio.run(getmostgoalscored())

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)



