from collections import defaultdict
import json
from uuid import UUID
from psycopg2 import pool
import logging
from settings import PG_USER, PG_PASSW, PG_HOST, PG_PORT, PG_DB_NAME
from datetime import datetime
from typing import Optional, List

logging.basicConfig(level=logging.INFO)

try:
    connection_pool = pool.SimpleConnectionPool(1, 20,
                            host = PG_HOST,
                            port = PG_PORT,
                            user = PG_USER,
                            password = PG_PASSW,
                            dbname = PG_DB_NAME)
except Exception as exc:
    logging.warning(f'[WARNING] Ошибка работы с БД при инициализации connection pool: {exc}')

def datetime_converter(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()


def get_connection():
    global connection_pool
    return connection_pool.getconn()


def put_connection(connection):
    global connection_pool
    connection_pool.putconn(connection)


def authorization(login: str, passw: str, token: str) -> list:
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            if token:
                update_query = "UPDATE users_authorization SET fcmtoken = %s WHERE login = %s AND passw = %s;"
                cursor.execute(update_query, (token, login, passw))
                conn.commit()
            select_query = "SELECT * FROM users_authorization WHERE login = %s AND passw = %s;"
            cursor.execute(select_query, (login, passw))
            data = cursor.fetchone()
            cursor.close()
            put_connection(conn)
            if data:
                data_dict = defaultdict(str)
                column_names = [description[0] for description in cursor.description]
                for index, value in enumerate(column_names):
                    data_dict[value] = data[index]                
                
                json_string = json.dumps(data_dict, indent=4)

                return json_string
            else:
                json_string  = json.dumps({"details": "user not found"})
                return json_string
        else:
            json_string  = json.dumps({"details": "conn not found or null"})
            return json_string
            
    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД: {exc}')
        json_string  = json.dumps({"error": exc})
        return json_string


def get_current_tasks() -> list:
    try:
        conn = get_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("""SELECT * FROM current_tasks 
                           WHERE status NOT IN ('Выполнено', 'Отменена') 
                           ORDER BY createtime DESC LIMIT 40""")
            data = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]

            tasks = []
            for row in data:
                task = dict(zip(column_names, row))
                convert_workers = task['workers'].split(', ') if task['workers'] else []
                task['workers'] = convert_workers
                convert_datetime = datetime.strftime(task['createtime'], "%Y-%m-%d %H:%M:%S")
                task['createtime']  = convert_datetime
                tasks.append(task)

            cursor.close()
            put_connection(conn)
            return tasks
        else:
            json_string  = json.dumps({"details": "conn not found or null"})
            return json_string

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД: {exc}')
        json_string  = json.dumps({"error": exc})
        return json_string


def update_task_status(task_id: UUID, status: str) -> None:
    try:
        conn  = get_connection()
        if conn:
            cursor  = conn.cursor()
            query = "UPDATE current_tasks SET status = %s WHERE id = %s"
            cursor.execute(query, (status, str(task_id)))
            conn.commit()
            cursor.close()
            put_connection(conn)
            json_string  = json.dumps({"details": "status is changed"})
            return json_string
        else:
            json_string  = json.dumps({"details": "conn not found or null"})
            return json_string

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД:  {exc}')
        json_string  = json.dumps({"error": exc})
        return json_string


def get_tech_card(tech_card_name: str) -> None:
    try:
        conn  = get_connection()
        if conn:
            cursor  = conn.cursor()
            query = "SELECT technological_operations FROM technological_cards WHERE name = %s"
            cursor.execute(query, (tech_card_name,))
            put_connection(conn)
            data  = cursor.fetchall()
            print(type(data[0][0]))
            return data[0][0] if data[0][0] else json.dumps({"details": "techCard not found"})
        else:
            json_string  = json.dumps({"details": "conn not found or null"})
            return json_string

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД:  {exc}')
        json_string  = json.dumps({"error": exc})
        return json_string

def current_sockets(machine_name: str):
    try:
        conn  = get_connection()
        if conn:
            cursor  = conn.cursor()
            query = "SELECT sockets_state FROM current_sockets WHERE machine_name = %s"
            print(query)
            cursor.execute(query, (machine_name,))
            put_connection(conn)
            data  = cursor.fetchall()
            print(data)
            cursor.close()
            json_string  = data[0][0] if data[0][0] else data[0]
            if json_string: return json_string
            else:
               json_string  = json.dumps({"details": "sockets_state is null"})
               return json_string
               

        else:
            json_string  = json.dumps({"details": "conn not found or null"})
            return json_string

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД:  {exc}')
        json_string  = json.dumps({"error": exc})
        return json_string


def update_current_sockets(machine_name: str, sockets_state):
    try:
        conn  = get_connection()
        if conn:
            cursor  = conn.cursor()
            query = "UPDATE current_sockets SET sockets_state = %s WHERE machine_name = %s"
            cursor.execute(query, (sockets_state, machine_name))
            conn.commit()
            put_connection(conn)
            cursor.close()
        else:
            json_string  = json.dumps({"details": "conn not found or null"})
            return json_string

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД:  {exc}')
        json_string  = json.dumps({"error": exc})
        return json_string

def add_anomaly_to_db(image_path: str, task_name: str, comment: str, author: str):
    try:
        conn  = get_connection()
        if conn:
            cursor  = conn.cursor()
            query = "INSERT INTO current_tasks(task, pathtophoto, comment, author) VALUES(%s, %s, %s, %s)"
            cursor.execute(query, (task_name, image_path, comment, author))
            conn.commit()
            put_connection(conn)
            cursor.close()
        else:
            json_string  = json.dumps({"details": "conn not found or null"})
            return json_string

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД:  {exc}')
        json_string  = json.dumps({"error": exc})
        return json_string


def add_defect_to_db(image_path: str, task_name: str, failed_element: str,
                      author: str, status: str, machine_name: str):
    try:
        conn  = get_connection()
        if conn:
            cursor  = conn.cursor()
            query = "INSERT INTO current_tasks(task, pathtophoto, failed_element, author) VALUES(%s, %s, %s, %s)"
            cursor.execute(query, (task_name, image_path, failed_element, author))
            conn.commit()
            query1 = "UPDATE machines SET currentstate = %s WHERE name = %s"
            cursor.execute(query1, (status, machine_name))
            conn.commit()
            put_connection(conn)
            cursor.close()
        else:
            json_string  = json.dumps({"details": "conn not found or null"})
            return json_string

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД:  {exc}')
        json_string  = json.dumps({"error": exc})
        return json_string
    

def update_machine_state(machine_name: str, state: str) -> None:
    try:
        conn  = get_connection()
        if conn:
            cursor  = conn.cursor()
            query = "UPDATE machines SET currentstate = %s WHERE name = %s"
            cursor.execute(query, (state, machine_name))
            conn.commit()
            put_connection(conn)
            return json.dumps({"details": "updated successfully", "currentstate": state})
        else:
            json_string  = json.dumps({"details": "conn not found or null"})
            return json_string

    except Exception as exc:
        logging.warning(f'[WARNING] Ошибка работы с БД:  {exc}')
        json_string  = json.dumps({"error": exc})
        return json_string
    

print(get_current_tasks())