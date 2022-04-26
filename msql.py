from typing import Dict

import pymysql

from settings import Settings


def select_money() -> Dict[int, float]:
    result = dict()
    try:
        connection = pymysql.connect(
            host=Settings.database_host,
            database=Settings.database_database,
            user=Settings.database_user,
            password=Settings.database_password,
        )

        sql_select_query = """
        SELECT `UserId`, `RemainMoney` 
        FROM `test`.`usertb` 
        WHERE `EIType` = '1' 
        AND `UserType` NOT IN ('4', '13', '14', '15') 
        AND `Status` = '1' 
        ORDER BY `UserId` DESC
        """
        cursor = connection.cursor()
        cursor.execute(sql_select_query)
        # get all records
        records = cursor.fetchall()
        # print("Total number of rows in table: ", cursor.rowcount)

        for num, row in enumerate(records, start=1):
            result.update({num: float(row[1])})
            # print("UserId = ", row[0], )
            # print("RemainMoney = ", row[1], "\n")

    except pymysql.connect.Error as e:
        print("Error reading data from MySQL table", e)
        raise Exception("Cannot continue")
    finally:
        connection.close()
        cursor.close()

    return result
