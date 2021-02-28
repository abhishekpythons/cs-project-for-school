import mysql.connector as dbms
import csv,time

db='drdo_patent'
create_table={'registration':'''create table registration(
                                                registration_id int(7) primary key auto_increment,
                                                user_name char(20),
                                                password char(20),
                                                email_id varchar(40))''',
                          'application':'''create table application(
                                                application_no int(7) primary key auto_increment,
                                                registration_id int(7),
                                                title varchar(200) not null ,
                                                lab char(10) ,
                                                technology_cluster char(50),
                                                filing_year int(4),
                                                team_allot char(10) not null,
                                                status char(20) default "not checked")''',
                'checking_teams':'''create table checking_teams(
                                                team_id char(7) primary key,
                                                no_of_members int(2),
                                                authentication_pin char(16) not null,
                                                on_mission bool not null default false)''',
            'patents_confirmed':'''create table patents_confirmed(
                                               patent_id int(7) primary key auto_increment,
                                               application_no int(7) ,
                                               checked_by char(20),
                                               filing_year int(4) not null)'''
                        }
def loading_animation(typ,msg,sec=1):
    print(f'[{typ}]\t',msg,end='')
    for i in range(sec):
        time.sleep(1)
        print('.',end=' ')
    print()
       
def connect_to_server(admin, password):
    loading_animation('action','connecting to server',3)
    conn=dbms.connect(user = admin, password = password)
    if conn.is_connected():
        loading_animation('info','connected')
    cur=conn.cursor()
    cur.execute('show databases;')
    databases=[i[0] for i in cur]
    

    def create_tables_if_not_exists(tables):
        cur.execute(f'use {db}')
        cur.execute('show tables')
        tables_in_db=[i[0] for i in cur]
        for table in tables:
            if table not in tables_in_db:
                loading_animation('action',f'creating table {table}',3)
                cur.execute(create_table[table])
            else:
                loading_animation('info',f'table {table} found in database')
                        
    if db not in databases:
        loading_animation('info',"database doesn't exist")
        loading_animation('action',f'creating database {db}',3)
        cur.execute(f'create database {db};')
        loading_animation('info','database created successfully')
        create_tables_if_not_exists(tuple(create_table.keys()))
    else:
        loading_animation('info',f'database {db} found')
        create_tables_if_not_exists(tuple(create_table.keys()))

    cur.execute('select count(*) from checking_teams')
    no_of_teams=cur.fetchall()[0][0]

    if no_of_teams==0:
        file=open('confidential.csv','r')
        reader=csv.reader(file)
        for row in reader:
            row[1]=int(row[1])
            row=tuple(row)
            cur.execute(f'insert into checking_teams(team_id,no_of_members,authentication_pin) values{row}')
            conn.commit()
        loading_animation('info','table checking teams filled')
        file.close()
