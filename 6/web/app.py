import logging
import os

import mysql.connector
from flask import Flask, jsonify, request

app = Flask(__name__)

# ログ設定
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    # タイムスタンプ、ログレベル、ログの内容
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# データベース接続関数
def get_db_connection():
    return mysql.connector.connect(
        # データベースの情報を環境変数から取得
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DB"),
    )


# データ新規登録エンドポイント
# URLと関数を紐づけるデコレータ。flaskの基本的なシンタックス
@app.route("/property", methods=["POST"])
def add_property():
    """
    リクエスト:

        curl -X POST http://localhost:5000/property \
             -H "Content-Type: application/json" \
             -d '{"property_name":"color","property_value":"blue"}'
             

        ここで、
            - -X POST: HTTPメソッドの指定。
            - -H "": HTTPヘッダをJSONに設定。
            - -d '{}': リクエストボディ。JSONでKeyとValueを指定して追加する。

    レスポンス:
        成功時: {"message": "Property added successfully"}
        失敗時: クライアントエラーの400またはそれ以外の任意のエラー500
    """
    try:
        data = request.get_json()
        # 未定義の場合も含んだ参照
        property_name = data.get("property_name")
        property_value = data.get("property_value")

        if not property_name or not property_value:
            # 400: クライアントエラー。リクエストの不備
            return jsonify({"error": "Property name and value are required"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO properties (property_name, property_value) VALUES (%s, %s)"
        cursor.execute(query, (property_name, property_value))

        # 確定
        conn.commit()
        # コネクションをクローズしてリソースを開放する
        cursor.close()
        conn.close()

        # 成功した場合なのでINFOレベルのログ追加
        logging.info(f"Added property: {property_name} = {property_value}")
        return jsonify({"message": "Property added successfully"}), 201

    # 任意のエラー
    except Exception as e:
        logging.error(f"Error adding property: {str(e)}")
        return jsonify({"error": str(e)}), 500


# データ取得エンドポイント
# 特定のプロパティアクセス時に実行
@app.route("/property/<name>", methods=["GET"])
def get_property(name):
    """
    リクエスト:

        curl http://localhost:5000/property/<name>

    レスポンス:

        成功時: {"property_name": <name>, "property_value": <value>}
        失敗時: プロパティが見つからない404または任意のエラー500
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = "SELECT property_value FROM properties WHERE property_name = %s"
        cursor.execute(query, (name,))
        result = cursor.fetchone()

        cursor.close()
        conn.close()

        # result: プロパティが存在するかどうか
        if result:
            logging.info(f"Retrieved property: {name} = {result[0]}")
            return jsonify({"property_name": name, "property_value": result[0]}), 200
        else:
            logging.warning(f"Property not found: {name}")
            return jsonify({"error": "Property not found"}), 404

    except Exception as e:
        logging.error(f"Error getting property: {str(e)}")
        return jsonify({"error": str(e)}), 500


# プロパティ一覧を取得するエンドポイント
@app.route("/properties", methods=["GET"])
def get_all_properties():
    """
    リクエスト:

        curl http://localhost:5000/properties
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM properties"
        cursor.execute(query)
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        logging.info("Retrieved all properties")
        return jsonify(results), 200

    except Exception as e:
        logging.error(f"Error getting all properties: {str(e)}")
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
