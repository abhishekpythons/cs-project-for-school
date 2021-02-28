import mysql.connector as dbms
import random,server_setup
from server_setup import loading_animation as echo
from time import localtime

def signup():
    username=input('username :- ')
    password=input('password :- ')
    while len(password)<8:
        password=input('password is too short \n enter valid password :-')
    while len(password)>20:
        password=input('password is too long \n enter valid password :-')
    email=input('email id :- ')
    if conn.is_connected():
        echo('info','connected')
    cur.execute(f'insert into registration(user_name,password,email_id) values("{username}","{password}","{email}")')
    echo('info',"registered")
    conn.commit()
    cur.execute('select * from registration')
    rid=cur.fetchall()[-1][0]
    echo('info','your registeration id is %d'%rid)

def login():
    rid=int(input('enter registration id :- '))
    cur.execute('select count(*) from registration where registration_id=%d'%rid)
    if cur.fetchall()[0][0]:
        pwd=input('enter password :- ')
        cur.execute('select password from registration where registration_id=%d'%rid)
        correct_pwd=cur.fetchall()[0][0]
        print(correct_pwd)
        while pwd != correct_pwd: 
            echo('alert','oops ! incorrect password')
            pwd=input('try again :-')
        else:
            print(' logged in...',
                  'press 1 for file a patent',
                  'press 2 for status of filed patent',
                  'press 3 for list of patents owned by you',
                  sep='\n')
            choice=int(input('enter your choice then press return key '))
            if choice==1:
                file_a_patent(rid)
            elif choice==2:
                status_of_patent(rid)
            elif choice==3:
                list_of_patents(rid)
            else :
                echo('alert','you choosed an invalid choice number')
    else:
        echo('alert','registration id not exists')
            
def file_a_patent(rid):
    title=input('Title of your project (max 200 words) :- ')
    lab=input('enter your lab :- ')
    TC=input('enter technology cluster of you project :- ')
    filing_year=localtime().tm_year
    cur.execute('select team_id from checking_teams where on_mission=false')
    free_teams=[i[0] for i in cur.fetchall()]
    team_allot=random.choice(free_teams)
    data=(rid,title,lab,TC,filing_year,team_allot)
    cur.execute(f'insert into application(registration_id,title,lab,technology_cluster,filing_year,team_allot) values{data}')
    cur.execute('update checking_teams set on_mission=1 where team_id="%s"'%team_allot)
    conn.commit()
    cur.execute('select * from application')
    aid=[i for i in cur][-1][0]
    echo('info',' successfully applied your application no. is %s '%aid)
    echo('info','a team with code %s will come soon for verification and confirmation of your research/product'%team_allot) 

def list_of_patents(rid):
    cur.execute(f'select title from application where registration_id="{rid}"')
    patents=[i[0] for i in cur]
    for i in range(len(patents)):
        print(i+1,'. ',patents[i])
    return patents

def status_of_patent(rid):
    cur.execute(f'select count(*) from application where registration_id={rid}')
    if cur.fetchall()[0][0]>0:
        echo('choose','you have following patents application')
        patents=list_of_patents(rid)
        choice=-1
        while not 0<=choice <len(patents):
            choice=int(input('choose patent no. to view status :- '))-1
        cur.execute(f'select status from application where title="{patents[choice]}"')
        data = cur.fetchall()[0][0]
        print(data)
    else:
        echo('alert','you do not filed any patent request till now')

def team_login():
    tid=input('enter team id :- ')
    pin=input('enter authentication pin :- ')
    cur.execute('select authentication_pin from checking_teams where team_id="%s"'%tid)
    correct_pin=cur.fetchall()[0][0]
    print(correct_pin)
    while pin!=correct_pin: 
        echo('alert',' oops ! incorrect password')
        pin=input('try again :-')
    else:
        print(' logged in...',
              'press 1 for checking is any task assigned',
              'press 2 for deatails of patent to be checked',
              'press 3 for confirming that verification have done',
              'press 4 to disqualify this request of patent',
              sep='\n')
        choice=int(input('enter your choice then press return key :-'))
        if choice==1:
            is_on_mission(tid)
        elif choice==2:
            details_of_patent(tid)
        elif choice==3:
            verify_the_patent(tid)
        elif choice==4:
            disqualify_the_patent(tid)

def is_busy(tid):
    echo('action','wait a minute checking',3)
    cur.execute(f'select on_mission from checking_teams where team_id="{tid}"')
    busy=cur.fetchall()[0][0]
    return busy

def is_on_mission(tid):
    if is_busy(tid):
        echo('info',f'yes you have a job to verify a patent')
    else:
        echo('info','you have not assigned any patent yet ')

def details_of_patent(tid):
    if is_busy(tid):
        cur.execute(f'select * from application where team_allot="{tid}"')
        data=[i for i in cur]
        print(data)

def verify_the_patent(tid):
    if is_busy(tid):
        cur.execute(f'select application_no,filing_year from application where team_allot="{tid}"')
        data=cur.fetchall()[0]
        data=data[0],tid,data[1]
        print(data)
        cur.execute(f'insert into patents_confirmed(application_no,checked_by,filing_year) values{data}')
        cur.execute(f'update application set status="verified" where team_allot="{tid}"')
        cur.execute(f'update checking_teams set on_mission=false where team_id="{tid}"')   
        conn.commit()
        echo('success','verified successfully')
    else:
        is_on_mission(tid)
        print('\t to verify')

def disqualify_the_patent(tid):
    if is_busy(tid):
        cur.execute(f'update application set status="rejected" where team_allot="{tid}"')
        cur.execute(f'update checking_teams set on_mission=false where team_id="{tid}"')   
        conn.commit()
        echo('done','team disqualified successfully')
    else:
        is_on_mission(tid)
        print('\t to disqualify')


#main
dbms_admin=input('enter DBMS(MySQL) username :- ')
dbms_pass=input('enter DBMS(MySQL) password :- ')
try:
    server_setup.connect_to_server(dbms_admin,dbms_pass)
    db='drdo_patent'
    conn=dbms.connect(user = dbms_admin, password = dbms_pass, database=db)
    cur=conn.cursor()
except:
    echo('alert','either username or password or both incorrect')
    echo('info','not able to connect please try again',3)
    quit()
