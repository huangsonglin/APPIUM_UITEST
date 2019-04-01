#-*-coding:utf-8 -*-
import pymysql

class Mysql:
    # 进入数据库
    def into_mysql(self):
        intodb = pymysql.Connect(host='rdsnpyc1dt23z1ilc87w.mysql.rds.aliyuncs.com', user='testreport',
                             password='Dcang@pmtest0309', database='paimai_train', charset='utf8')
        # 建立游标池
        db = intodb.cursor()
        return db

    # 执行查询
    def sql_result(self,sql):
        db = Mysql().into_mysql()
        try:
            db.execute(sql)
            data = db.fetchall()
            return list(data)
        except():
            raise ValueError('查询出错')

    # 更新语句
    def updata(self,sql):
        db = Mysql().into_mysql()
        db.execute(sql)
        db.connection.commit()

    # 删除语句
    def delete(self, sql):
        db = Mysql().into_mysql()
        db.execute(sql)
        db.connection.commit()

    # 查询结果转换
    def reslut_replace(self,sql):
        result = Mysql().sql_result(sql)
        if result == []:
            result = ''
        else:
            result = result[0][0]
        return str(result)

    # 执行其他操作
    def user_database(self,sql):
        db = Mysql().into_mysql()
        db.execute(sql)




