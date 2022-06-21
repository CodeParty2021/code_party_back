# CodeParty バックエンド

## 環境構築

1. pipenv をインストール
   ```
   #mac
   brew install pipenv
   #win
   pip install pipenv
   ```
2. pipfile.lock のライブラリを一括でダウンロード(pycharm なら 2 と 3 は自動的にやってくれるっぽい)
   ```
   pipenv install
   ```
3. shell に入る。
   ```
   pipenv shell
   ```
4. env ファイルの作成。中身は[こちら](https://www.notion.so/ea4344dedbb444818cb1aad0f7b6b612?p=750a8dca400848d1a0ee8c8b1613d343)

   ```
   vi .env
   ```

5. db のマイグレーション

   ```
   python manage.py migrate
   ```

6. db に初期データの追加
   ```
   python manage.py loaddata post_initial.json
   ```
7. イベントデータの追加（任意）
   ```
   python manage.py loaddata event.json
   ```
8. 起動
   ```
   python manage.py runserver
   ```

## フォーマッター

black を使っています。push 前にテストを回しましょう。
PyCharm ユーザは[設定](https://www.notion.so/ea4344dedbb444818cb1aad0f7b6b612?p=98997f2292984e3ab4511f02f97cd21d) すればオートフォーマットしてくれます。

```
black .
```

## テスト

詳細は[こちら](https://www.notion.so/ea4344dedbb444818cb1aad0f7b6b612?p=6f0af3fa3f53409ab0f4feb14adb3038)

```
coverage run --source='.' manage.py test
```

## デプロイ先

新：[heroku](https://codepartyenjoy.herokuapp.com/)

## 手動デプロイ

事前に heroku CLI をインストールしておく

[codeparty](https://www.notion.so/e9be2d0a144c453d9c89ebb8cbdc6752)アカウントで heroku ログイン

```
heroku login
```

リモートに追加

```
heroku git:remote -a codepartyenjoy
```

特定のブランチから push

```
git push heroku <ブランチ名>:master
```

もしリモート名を変更するときは

```
git remote rename heroku heroku-prod
```

## github のルール

1. チケットごとにブランチを作って main に PR を送る
2. main でローカルで正しく動くことをチェックする
3. published に main をマージすると heroku に反映される。

## データベースのテスト

上のコマンド通りにやると heroku 上とは違うデータベース（sqlite3）でテストされます．sqlite3 で十分だとは思いますが，もし本番環境と同じ環境にしたかったら以下の手順で PostgreSQL を導入してください．

1. PostgreSQL をダウンロード&インストールする
2. PostgreSQL でデータベースを立てる
   ```
   CREATE DATABASE [Database Name]
   ```
3. 環境変数に以下のように設定する
   ```
   DATABASE_URL=postgres://[User]:[Password]@localhost/[Database Name]
   ```
4. code_party_back/local_settings.py の下らへんのコメントアウトを外す

## ユーザ認証のテスト

ユーザ認証テストは自動化出来なかったのでコマンドでテストできるようにしました．以下のコマンドを実行することで，ローカル及び本番環境でユーザ認証のテストが出来ます．※テストを実行すると，テストユーザーがデータベースに追加されます．

```
python manage.py auth_test
```

## Swaggerによるエンドポイントの詳細の確認
Swaggerでエンドポイントについてを確認できます。
確認方法は以下となります。
1. コマンドでサーバーを起動する。
   ```
   python manage.py runserver
   ```
2. Swaggerを導入したことで追加されたエンドポイント ```/Swagger/```　に接続する。

そのほかの詳細については[こちら](https://www.notion.so/ea4344dedbb444818cb1aad0f7b6b612?p=0caa224d7c63453eb5b1253aab224ac0)

