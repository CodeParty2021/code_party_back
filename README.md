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
4. envファイルの作成。中身は[こちら](https://www.notion.so/ea4344dedbb444818cb1aad0f7b6b612?p=750a8dca400848d1a0ee8c8b1613d343)
    ```
   vi .env
   ```
    


4. dbのマイグレーション
    ```
    python manage.py migrate
    ```
5. 起動
    ```
    python manage.py runserver
    ```

## フォーマッター
blackを使っています。push前にテストを回しましょう。 
PyCharmユーザは[設定](https://www.notion.so/ea4344dedbb444818cb1aad0f7b6b612?p=98997f2292984e3ab4511f02f97cd21d) すればオートフォーマットしてくれます。
```
black .
```

## テスト
詳細は[こちら](https://www.notion.so/ea4344dedbb444818cb1aad0f7b6b612?p=6f0af3fa3f53409ab0f4feb14adb3038)

```
coverage run --source='.' manage.py test
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

## ユーザ認証のテスト
ユーザ認証テストは自動化出来なかったのでコマンドでテストできるようにしました．以下のコマンドを実行することで，ローカル及び本番環境でユーザ認証のテストが出来ます．※テストを実行すると，テストユーザーがデータベースに追加されます．

```
python manage.py auth_test
```