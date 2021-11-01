# CodePartyバックエンド


## 環境構築
1. pipenvをインストール
    ```
    #mac
    brew install pipenv
    #win
    pip install pipenv
    ```
2. pipfile.lockのライブラリを一括でダウンロード(pycharmなら2と3は自動的にやってくれるっぽい)
    ```
    pipenv install
    ```
3. shellに入る。
    ```
    pipenv shell
    ```
4. dbのマイグレーション
    ```
    python manage.py migrate
    ```
5. 起動
    ```
    python manage.py runserver
    ```

## デプロイ先 
[heroku](https://code-party-back.herokuapp.com/)

## githubのルール
1. チケットごとにブランチを作ってmainにPRを送る 
2. mainでローカルで正しく動くトトをチェックする
3. publishedにmainをマージするとherokuに反映される。
