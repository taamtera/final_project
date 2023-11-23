import random ,sys, os
from database import DB

db = DB()
user = None


def initializing():
    db.load('persons.csv')\
        .load('login.csv')\
        .load('projects.csv')\
        .load('requests.csv')\
            
def admin():
    while True:
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        print('Welcome admin. select a table to edit type "back" to exit admin mode.')
        db.print()
        unip = uinput()
        if unip == 'back':
            return None
        if db.select(unip) is not None:
            tb = unip
            while True:
                os.system('cls' if os.name == 'nt' else "printf '\033c'")
                db.select(tb).print()
                print('Enter the "ID" of the entry you would like to edit or')
                print('"new" add new entry')
                print('"delete" delete entry')
                print('"back" to go back')
                unip = uinput()
                if unip == 'back':
                    break
                elif unip == 'new':
                    db.select(tb).table.append({'ID': rnd_id()})
                    for key in db.select(tb).table[0].keys():
                        if key != 'ID':
                            db.select(tb).table[0][key] = uinput('Enter ' + key + ': ')
                    db.write(tb + '.csv')
                elif unip == 'delete':
                    db.select(tb).drop(where={'ID': uinput('Enter ID of entry to delete: ')})
                    db.write(tb + '.csv')
                elif db.select(tb, where={'ID': unip}) is not None:
                    entry = db.select(tb, where={'ID': unip})
                    print('leave blank to keep current value')
                    for key in entry.table[0].keys():
                        if key != 'ID':
                            unip = uinput('Enter ' + key + ': ')
                            if unip != '':
                                entry.table[0][key] = unip
                    db.write(tb + '.csv')
    

def get_project():
    unip = ''
    new= True
    if user['type'] == 'admin':
        string = """Select a project to work on by "name" or "ID" or enter "admin" for admin mode."""
        print(line(len(string)))
        print(string)
        print(line(len(string)))
        db.select('projects').select(['ID', 'name', 'project_data', 'stage']).print()
        print(line(len(string)))
        unip = uinput()
        if unip == 'admin':
            admin()
            return None
    else:
        string = """Select a project to work on by "name" or "ID"."""
        print(line(len(string)))
        print(string)
        print(line(len(string)))
        if db.select('projects',where={'head': user['ID']}) is not None:
            new = False
            print('Your projects: ')
            db.select('projects',where={'head': user['ID']}).select(['ID', 'name', 'project_data', 'stage']).print()
            print(line(len(string)))
        if db.select('projects',where={'member1': user['ID']}) or db.select('projects',where={'member2': user['ID']}) is not None:
            new = False
            print('Projects you are a member of: ')
            if db.select('projects',where={'member1': user['ID']}) is not None:
                db.select('projects',where={'member1': user['ID']}).select(['ID', 'name', 'project_data', 'stage']).print()
            if db.select('projects',where={'member2': user['ID']}) is not None:
                db.select('projects',where={'member2': user['ID']}).select(['ID', 'name', 'project_data', 'stage']).print()
            print(line(len(string)))
        if db.select('projects',where={'advisor': user['ID']}) is not None:
            new = False
            print('Your Student\'s projects: ')
            db.select('projects',where={'advisor': user['ID']}).select(['ID', 'name', 'project_data', 'stage']).print()
            print(line(len(string)))
        if new:
            unip = uinput('You have no projects. type "New" to make a new project: ')
        else:
            unip = uinput('or "New" to make a new project: ')

    if unip == '':
        return None
    unip = unip.lower()
    project_id = db.select('projects', where={'ID': unip}) or db.select('projects', where={'name': unip})
    if project_id is not None:
        edit_project(project_id)
    elif unip == 'new':
        create_project()

def edit_project(project_id):
    while True:
        db.load('projects.csv')
        project = db.select('projects', where={'ID': project_id.table[0]['ID']})
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        print('Project data: ')
        print(line(len('Project data: ')))
        project.select(['ID', 'name', 'project_data', 'stage']).print()
        head = db.select('persons', where={'ID': project.table[0]['head']})
        print('project head: ' + head.table[0]['fist'] + ' ' + head.table[0]['last'])
        member1 = db.select('persons', where={'ID': project.table[0]['member1']})
        if member1 is not None:
            print('project member1: ' + member1.table[0]['fist'] + ' ' + member1.table[0]['last'])
            member2 = db.select('persons', where={'ID': project.table[0]['member2']})
            if member2 is not None:
                print('project member2: ' + member2.table[0]['fist'] + ' ' + member2.table[0]['last'])
        advisor = db.select('persons', where={'ID': project.table[0]['advisor']})
        if advisor is not None:
            print("Your Student's projects: " + advisor.table[0]['fist'] + ' ' + advisor.table[0]['last'])
        string = 'what would you like to do with this project: '
        print(line(len(string)))
        if project.table[0]['head'] == user['ID'] or user['type'] == 'admin':
            print('"1" Edit project data')
            print('"2" Invite member')
            print('"3" Request advisor')
            print('"4" submit project')
            print('"5" Delete project')
        elif project.table[0]['advisor'] == user['ID']:
            print('"5" abandon your studetns')
        else:
            print('"1" Edit project data')
            print('"5" leave project')
        print('"back" to go back')
        print(line(len(string)))
        unip = uinput(string)
        if project.table[0]['head'] != user['ID'] and unip in ['2' '3', '4'] and user['type'] != 'admin':
            unip = 0
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        match unip:
            case '1':
                project.upsert({'project_data': uinput('Enter new project data: ')})
                db.write('projects.csv')
            case '2':
                print('Enter the ID of the person you would like to invite.')
                db.select('persons',where={'type': 'student'}).select(['ID', 'fist', 'last']).print()
                unip = uinput()
                if db.select('persons', where={'ID': unip}) is not None:
                    if project.table[0]['member1'] == '':
                        send_request(project, unip, 'member1')
                    elif project.table[0]['member2'] == '':
                        send_request(project, unip, 'member2')
                    else:
                        uinput('This project is full.')
                else:
                    uinput('Invalid ID.')
            case '3':
                print('Enter the ID of the person you would like to invite.')
                db.select('persons',where={'type': 'faculty'}).select(['ID', 'fist', 'last']).print()
                unip = uinput()
                if db.select('persons', where={'ID': unip}) is not None:
                    send_request(project, unip, 'advisor')
                else:
                    uinput('Invalid ID.')
            case '4':
                if project.table[0]['advisor'] is '':
                    uinput('You need to request an advisor first.')
                else:
                    send_request(project.table[0]['ID'], project.table[0]['advisor'], 'submit')
                    project.upsert({'stage': 'submitted'})
                    uinput('Project submitted.')
            case '5':
                if project.table[0]['head'] != user['ID']:
                    project.upsert({'advisor': None}, where={'advisor': user['ID']})
                    project.upsert({'member1': None}, where={'member1': user['ID']})
                    project.upsert({'member2': None}, where={'member2': user['ID']})
                    db.write('projects.csv')
                    return None
                project.select(['ID', 'name', 'project_data', 'stage']).print()
                string = uinput('Are you sure you want to delete this project? enter the id of the project to confirm:')
                if string == project.table[0]['ID']:
                    db.select('projects').drop(where={'ID': project_id.table[0]['ID']})
                    return None
            case 'back':
                return None

def create_project():
    # ID,name,head,member1,member2,advisor,project_data
    os.system('cls' if os.name == 'nt' else "printf '\033c'")
    data = {'ID': rnd_id(), 'name': uinput('Enter project name: '), 'head': user['ID'], 'member1': None, 'member2': None, 'advisor': None, 'project_data': uinput('Enter project data: '),'stage': 'draft'}
    db.select('projects').upsert(data).write('projects.csv')

def get_request():
    requests = db.select('requests', where={'ID': user['ID']})
    if requests is None:
        print('You have no requests')
    else:
        print('You have ' + str(len(requests)) + ' requests.')
        for request in requests.table:
            print('{Project: "' + request['project_name'] + '" type: "' + request['type'] +'"}')
            print('Enter "accept" to accept the request or "decline" to decline it.')
            unip = uinput()
            if unip == 'accept':
                if request['type'] == 'member1':
                    db.select('projects').upsert({'member1': user['ID']}, where={'ID': request['project']})
                elif request['type'] == 'member2':
                    db.select('projects').upsert({'member2': user['ID']}, where={'ID': request['project']})
                elif request['type'] == 'advisor':
                    db.select('projects').upsert({'advisor': user['ID']}, where={'ID': request['project']})
                elif request['type'] == 'submit':
                    db.select('projects').upsert({'stage': 'accepted'}, where={'ID': request['project']})
                db.select('requests').drop(where={'ID': user['ID'], 'project': request['project']})
                print('Request accepted.\n')
                db.write('projects.csv').write('requests.csv')
            elif unip == 'decline':
                if request['type'] == 'submit':
                    db.select('projects').upsert({'stage': 'draft'}, where={'ID': request['project']})
                db.select('requests').drop(where={'ID': user['ID'], 'project': request['project']})
                print('Request declined.\n')
                db.write('projects.csv').write('requests.csv')
    return None

def send_request(project,user_id,type):
    db.select('requests').upsert({'ID': user_id, 'project': project.table[0]['ID'], 'type': type, 'project_name': project.table[0]['name']})
    uinput('Request sent.')
    db.write('requests.csv')

def rnd_id():
    return str(random.randint(1000000, 9999999))

def line(leng):
    return ''.join(['-' for _ in range(leng)])

def uinput(string = ''):
    unip = input(string).lower()
    if unip == 'exit':
        exit()
    return unip

def login():
    # ask the user to enter the username and password 3 times
    for _ in range(3):
        # username = uinput("Enter username: ")
        # password = uinput("Enter password: ",clear=true)
        username = 'Taam.P'
        password = '1234'
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        # check if the user id exists and the password matches
        login_id = db.select('login', where={'username': username, 'password': password})
        if login_id:
            return login_id.table[0]['ID']
        print('Login failed. Please try again.')
    print('You have exceeded the maximum number of tries. Please try again later.')
    return None

def exit():
    # write out all the tables that have been modified to the corresponding CSV files
    db.write('persons.csv')\
        .write('login.csv')\
        .write('projects.csv')\
        .write('requests.csv')
    sys.exit()

def main():
    # make calls to the initializing and login functions defined above
    initializing()
    user_id = login()
    if user_id is None:
        uinput()
        return
    global user
    user = db.select('persons', where={'ID': user_id}).table[0]
    while True:
        initializing()
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        string = 'Welcome '+ user['type'] + " " + user['fist'] + ' ' + user['last'] + '. type "exit" to exit.'
        print( '\n' + line(len(string)))
        print(string)
        print(line(len(string)))
        get_request()
        get_project()

main()


