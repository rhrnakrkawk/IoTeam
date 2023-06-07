import pymysql
conn = pymysql.connect(
        host="3.216.219.9",
        port=3306,
        user="hhs",
        password="5499458k",
        db="restaurant",
        charset="utf8"
    )
db = conn.cursor()

# 테이블 목록 가져오기
script = "SHOW TABLES;"
db.execute(script)
tables = db.fetchall()

try:
    # 각 테이블에 대해 Auto Increment 초기화 및 재정렬
    for table in tables:
        table_name = table[0]
        if table_name == "alembic_version":
            continue
        script1 = f"ALTER TABLE {table_name} AUTO_INCREMENT=1;"
        script2=f"SET @COUNT = 0;"
        script3=f"UPDATE {table_name} SET id = @COUNT:=@COUNT+1;"
        db.execute(script1)
        db.execute(script2)
        db.execute(script3)
    conn.commit()
    db.close()
    conn.close()
    print("Auto Increment 초기화 및 재정렬 완료")
except Exception as e:
    print(e)
    db.close()
    conn.close()
finally:
    print("종료")