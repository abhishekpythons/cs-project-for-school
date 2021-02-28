import server_setup, server_logic
from server_setup import loading_animation as echo

choice = 'y'
while choice=='y':
    actions=['signup','login','login as checking team']
    for i in range(len(actions)):
        print(f'press {i+1} for {actions[i]}')
    action_index=int(input('choose the action'))-1
    if action_index==0:
        server_logic.signup()
    elif action_index==1:
        server_logic.login()
    elif action_index==2:
        server_logic.team_login()
    else:
        echo('alert','please make a valid choice')
    print(r' /-\ \/  '*10)
    choice=input('do you want to give another command (y/n) :- ')
    
else:
    echo('info','OK shutting down server on your machine',5)
    quit()

