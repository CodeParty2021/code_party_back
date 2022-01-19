import requests
import pprint
import os
from dotenv import load_dotenv
import json

# 認証のtestがうまく行かないのでこちらで仮テストケース
# issue: https://github.com/CodeParty2021/code_party_back/issues/19
# envのロード
load_dotenv()

# トークンはフロントエンドから頑張ってとってきてください！feature_authをpullして実行すればconsoleでprintできるはず
token = "tokenをここに"
headers = {"Authorization": "Bearer {}".format(token)}
r_get = requests.get("http://localhost:8000/users/auth", headers=headers)
print(r_get)
pprint.pprint(r_get.json())
