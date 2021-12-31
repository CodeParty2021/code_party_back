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
旧：[heroku](https://code-party-back.herokuapp.com/)
新：[heroku](https://codepartyenjoy.herokuapp.com/)
## githubのルール
1. チケットごとにブランチを作ってmainにPRを送る 
2. mainでローカルで正しく動くことをチェックする
3. publishedにmainをマージするとherokuに反映される。

## データベースのテスト
上のコマンド通りにやるとheroku上とは違うデータベース（sqlite3）でテストされます．sqlite3で十分だとは思いますが，もし本番環境と同じ環境にしたかったら以下の手順でPostgreSQLを導入してください．
1. PostgreSQLをダウンロード&インストールする
2. PostgreSQLでデータベースを立てる
    ```
    CREATE DATABASE [Database Name]
    ```
3. 環境変数に以下のように設定する
    ```
    DATABASE_URL=postgres://[User]:[Password]@localhost/[Database Name]
    ```
4. code_party_back/local_settings.pyの下らへんのコメントアウトを外す
