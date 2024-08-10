import psycopg2
import random

from psycopg2 import sql

conn = psycopg2.connect(dbname='postgres', user='postgres', 
                        password='postgres', host='localhost', port=5433)

cursor = conn.cursor()

def set_sql():
    columns = """(phone, city,  address,  problem,  description, main_section_time, equip_section_time, cabel_section_time, router_section_time,
                     internet_section_time, lan_section_time, speed_section_time, wifi_section_time, connection_section_time, tariff_section_time,
                     offs_section_time, errors_section_time, my_tariff_section_time, change_tariff_section_time, all_section_time)"""
    
    times = [random.randint(0, 20), random.randint(0, 40), random.randint(0, 20), random.randint(0, 20), random.randint(0, 40), random.randint(0, 20),
             random.randint(0, 20), random.randint(0, 20), random.randint(0, 20), random.randint(0, 20), random.randint(0, 40),
             random.randint(0, 20), random.randint(0, 20), random.randint(0, 20), random.randint(0, 20)]

    all_section_time = sum(times)

    querry = sql.SQL(f"""insert into orders {columns} select {random.randint(80000000000, 90000000000)}, 
                            {random.choice(["'Москва'", "'Санкт-Петербург'", "'Екатеринбург'",  "'Новосибирск'", "'Казань'"])}, {"'-'"}, {"'-'"}, {times[0]}, 
                            {times[1]}, {times[2]}, {times[3]}, {times[4]}, {times[5]},
                            {times[6]}, {times[7]}, {times[8]}, {times[9]}, {times[10]},
                            {times[11]}, {times[12]}, {times[13]}, {times[14]}, {all_section_time}""")
    
    return querry

with conn:
    with conn.cursor() as cursor:
        try:
            for count in range(1):
                cursor.execute(set_sql())
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)