from typing import Dict

import pymysql
import win32serviceutil

from settings import Settings


def start_service(service: str) -> None:
    print("Start MySQL service")
    return win32serviceutil.StartService(service)


def stop_service(service: str) -> None:
    print("Stop MySQL service")
    return win32serviceutil.StopService(service)


def restart_service(service: str) -> None:
    print("Restart MySQL service")
    return win32serviceutil.RestartService(service)


def status_service(service: str) -> tuple:
    return win32serviceutil.QueryServiceStatus(service)


def start_or_restart_service(service: str) -> None:
    if not status_service(service):
        print("MySQL service is NOT installed")
        raise Exception
    if status_service(service)[1] != Settings.service_status_running:
        print("MySQL is off")
        return start_service(service)
    if status_service(service)[1] == Settings.service_status_running:
        print("MySQL is running now")
        return restart_service(service)


def select_money() -> Dict[int, float]:
    start_or_restart_service(Settings.service_name)
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

        for num, row in enumerate(records, start=1):
            result.update({num: float(row[1])})

    except pymysql.connect.Error as e:
        print("Error reading data from MySQL table", e)
        raise Exception("Cannot continue")
    finally:
        connection.close()
        cursor.close()

    return result
