from typing import Dict

import pymysql

from settings import Settings

from .service import start_or_restart_service


def select_balance() -> Dict[int, float]:
    start_or_restart_service(Settings.service_name)
    result = dict()
    try:
        connection = pymysql.connect(
            host=Settings.database_host,
            database=Settings.database_database,
            user=Settings.database_user,
            password=Settings.database_password,
        )

        sql_select_query = f"""
        SELECT `RemainMoney` 
        FROM `{Settings.database_select_database}`.`usertb` 
        WHERE `EIType` = '1' 
        AND `UserType` NOT IN ('4', '13', '14', '15') 
        AND `Status` = '1' 
        ORDER BY `UserId` DESC
        """
        cursor = connection.cursor()
        cursor.execute(sql_select_query)
        # get all records
        records = cursor.fetchall()

        for num, row in enumerate(records, start=1):
            result.update({num: float(row[0])})

    except pymysql.connect.Error as e:
        print("Error reading data from MySQL table", e)
        raise Exception("Cannot continue")
    finally:
        connection.close()
        cursor.close()

    return result
