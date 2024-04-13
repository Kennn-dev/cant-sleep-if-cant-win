import os
import subprocess
import time

import psutil
from lcu_driver import Connector

connector = None

data = None


def checkEndGame():
    global connector

    if connector == None:
        connector = Connector()

    @connector.ready
    async def connect(connection):
        print('LCU API is ready to be used.')
        global data
        while data == None:
            lobby = await connection.request('get', '/lol-end-of-game/v1/eog-stats-block')
            if lobby.status == 200:
                result = await lobby.json()
                isWin = False
                for team in result["teams"]:
                    if team["isWinningTeam"] == True and team["isPlayerTeam"] == True:
                        isWin = True
                if isWin:
                    print("Time to sleep !!!!!")
                    data = True
                    # return
                    # continue
                    subprocess.call(
                        "TASKKILL /F /IM LeagueClient.exe", shell=True)
                time.sleep(3)
            else:
                print("Game doesn't ended yet...")
                time.sleep(2)
                # continue

    connector.start()


# count = 0
while True:
    for p in psutil.process_iter():
        if p.name() == 'LeagueClient.exe':
            checkEndGame()
    print("No game found, waiting ...")
    time.sleep(2)
    continue
