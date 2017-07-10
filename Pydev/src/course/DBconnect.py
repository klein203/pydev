'''
Created on 2017年6月29日

@author: xusheng
'''

import pymysql

def fetchdata():
    config = {
        'host':'10.32.173.250',
        'port':3306,
        'user':'cxpspmsit',
        'password':'k3WAw2At4wsnqlT',
        'db':'cxpspmsit',
        'charset':'utf8mb4',
        'cursorclass':pymysql.cursors.DictCursor,
    }
    conn = pymysql.connect(**config)
    
    try:
        with conn.cursor() as cursor:
            cursor.execute('select id, name from t_brand')
            res = cursor.fetchall()
            print('id', 'name')
            print('---------------------')
            for item in res:
                print(item['id'], item['name'])
    except BaseException as e:
        print(e)
    finally:
        conn.close()


if __name__ == '__main__':
    fetchdata()