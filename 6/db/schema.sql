-- データベースの作成
CREATE DATABASE IF NOT EXISTS simple_db;
USE simple_db;

-- プロパティを保存するテーブル
CREATE TABLE properties (
    id INT AUTO_INCREMENT PRIMARY KEY,
    property_name VARCHAR(255) NOT NULL,
    property_value VARCHAR(255) NOT NULL
);