import pandas as pd
from sqlalchemy import create_engine
import pymysql
import glob
import os

# 数据库连接字符串（请根据实际情况修改）
database_url = 'mysql+pymysql://root:123456@127.0.0.1:3306/Comment_database'
engine = create_engine(database_url)

# 在MySQL中创建数据库和表
engine.execute("CREATE DATABASE IF NOT EXISTS Comment_database;")
engine.execute("USE Comment_database;")

# 自动搜索目录下的所有xlsx文件
excel_files = glob.glob(r'D:\ShiXi\douyin_comment_spider\spider\result\*.xlsx')

# 遍历所有找到的Excel文件
for file in excel_files:
    # 从文件路径中提取文件名作为表名，去掉.xlsx
    table_name = os.path.splitext(os.path.basename(file))[0]
    table_name = table_name.replace('-', '_').replace(' ', '_')  # 替换不适合SQL表名的字符

    # 读取Excel文件
    xls = pd.ExcelFile(file)
    full_data = pd.DataFrame()

    # 遍历所有工作表
    for sheet_name in xls.sheet_names:
        df = pd.read_excel(xls, sheet_name=sheet_name)
        df['视频ID'] = sheet_name  # 添加视频ID列
        full_data = pd.concat([full_data, df], ignore_index=True)

    # 为每个Excel文件创建和填充一个表
    create_table_sql = f"""
    CREATE TABLE IF NOT EXISTS `{table_name}` (
        视频ID VARCHAR(255),
        作品id VARCHAR(255),
        作品链接 TEXT,
        作品标题 TEXT,
        作品点赞数 INT,
        作品评论数 INT,
        作品发布时间 DATETIME,
        作者名字 VARCHAR(255),
        作者主页 TEXT,
        作者粉丝数 INT,
        作者获赞数 INT,
        评论数据爬取时间 DATETIME,
        评论用户名 VARCHAR(255),
        评论用户主页 TEXT,
        评论时间和地点 TEXT,
        评论内容 TEXT,
        评论被赞数 INT,
        PRIMARY KEY (作品id)
    );"""
    engine.execute(create_table_sql)

    # 将数据导入MySQL
    full_data.to_sql(table_name, con=engine, if_exists='replace', index=False)

    print(f"数据已成功导入MySQL数据库中的表 {table_name}！")
