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
                    newtb = {}
                    for key in db.select(tb).table[0].keys():
                        if key != 'ID':
                            newtb[key] = uinput('Enter ' + key + ': ',False)
                        else:
                            rid = uinput('Enter ' + key + ' or leave blank for Random ID: ',False)
                            newtb[key] = rid or rnd_id()
                    db.select(tb).table.append(newtb)
                    db.write(tb + '.csv')
                elif unip == 'delete':
                    db.select(tb).drop(where={'ID': uinput('Enter ID of entry to delete: ')})
                    db.write(tb + '.csv')
                elif db.select(tb, where={'ID': unip}) is not None:
                    entry = db.select(tb, where={'ID': unip})
                    print('leave blank to keep current value')
                    for key in entry.table[0].keys():
                        if key != 'ID':
                            unip = uinput('Enter ' + key + ': ', False)
                            if unip != '':
                                entry.table[0][key] = unip
                    db.write(tb + '.csv')
    

def get_project():
    unip = ''
    new= True
    if user['type'] == 'admin' or user['type'] == 'faculty':
        if user['type'] == 'admin':
            string = """Select a project to work on by "name" or "ID" or enter "admin" for admin mode."""
        else:
            string = """Select a project to work on by "name" or "ID"."""
        print(line(len(string)))
        print(string)
        print(line(len(string)))
        if db.select('projects',where={'advisor': user['ID']}) is not None:
            print('Your Student\'s projects: ')
            db.select('projects',where={'advisor': user['ID']}).select(['ID', 'name', 'project_data', 'stage']).print()
            print(line(len(string)))
        elif user['type'] == 'faculty':
            print('You have no assigned projects.')
            print(line(len(string)))
        print('All projects: ')
        db.select('projects').select(['ID', 'name', 'project_data', 'stage']).print()
        print(line(len(string)))
        unip = uinput()
        if unip == 'admin' and user['type'] == 'admin':
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
    elif unip == 'new' and user['type'] == 'student':
        create_project()

def edit_project(project_id):
    #  It just works (if it an't broke don't fix it)
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
            print('project member 1: ' + member1.table[0]['fist'] + ' ' + member1.table[0]['last'])
            member2 = db.select('persons', where={'ID': project.table[0]['member2']})
            if member2 is not None:
                print('project member 2: ' + member2.table[0]['fist'] + ' ' + member2.table[0]['last'])
        advisor = db.select('persons', where={'ID': project.table[0]['advisor']})
        if advisor is not None:
            print("Your Student's projects: " + advisor.table[0]['fist'] + ' ' + advisor.table[0]['last'])
        string = 'what would you like to do with this project: '
        print(line(len(string)))
        if project.table[0]['stage'] == 'finished':
            print('This project is finished.')
            uinput('Enter to go back: ')
            return None
        cmd = []
        if project.table[0]['head'] == user['ID'] or user['type'] == 'admin':
            if project.table[0]['stage'] == 'draft':
                cmd.append('1')
                print('"1" Edit project data')
            elif project.table[0]['stage'] == 'accepted':
                cmd.append('1')
                print('"1" Edit Report')
            cmd.append('2')  
            print('"2" Manage member')
            cmd.append('3')
            print('"3" Request advisor')
            if project.table[0]['stage'] == 'draft':
                cmd.append('4')
                print('"4" Submit project')
            elif project.table[0]['stage'] == 'accepted':
                cmd.append('4')
                print('"4" Submit Report')
            cmd.append('5')
            print('"5" Delete project')
        elif project.table[0]['advisor'] == user['ID']:
            cmd.append('5')
            print('"5" abandon your studetns')
        else:
            print('"1" Edit project data')
            print('"5" leave project')
        print('"back" to go back')
        print(line(len(string)))
        unip = uinput(string)
        if unip not in cmd and user['type'] != 'admin':
            unip = 0
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
        match unip:
            case '1':
                if project.table[0]['stage'] == 'draft':
                    project.upsert({'project_data': uinput('Enter new project data: ')})
                else:
                    project.upsert({'project_data': uinput('Enter new report_data: ')})
                db.write('projects.csv')
            case '2':
                db.select('persons',where={'type': 'student'}).select(['ID', 'fist', 'last']).print()
                member1 = db.select('persons', where={'ID': project.table[0]['member1']})
                if member1 is not None:
                    print('project member 1: ' + member1.table[0]['fist'] + ' ' + member1.table[0]['last'])
                member2 = db.select('persons', where={'ID': project.table[0]['member2']})
                if member2 is not None:
                    print('project member 2: ' + member2.table[0]['fist'] + ' ' + member2.table[0]['last'])
                print('Enter the "fist" or "ID" of the person you would like to invite or remove.')
                unip = uinput()
                member_id = db.select('persons', where={'ID': unip}) or db.select('persons', where={'fist': unip})
                if member_id is not None:
                    if project.table[0]['member1'] == member_id.table[0]['ID']:
                        project.upsert({'member1': None})
                        uinput('member 1 removed.')
                        db.write('projects.csv')
                    elif project.table[0]['member2'] == member_id.table[0]['ID']:
                        project.upsert({'member1': None})
                        uinput('member 2 removed.')
                        db.write('projects.csv')
                    elif project.table[0]['member2'] == '' or project.table[0]['member1'] == '':
                        send_request(project, member_id.table[0]['ID'], 'member')
                    else:
                        uinput('This project is full.')
                else:
                    uinput('Invalid ID or fist.')
            case '3':
                print('Enter the "fist" or "ID" of the person you would like to invite.')
                db.select('persons',where={'type': 'faculty'}).select(['ID', 'fist', 'last']).print()
                unip = uinput()
                advisor_id = db.select('persons', where={'ID': unip}) or db.select('persons', where={'fist': unip})
                if advisor_id is not None:
                    send_request(project, advisor_id.table[0]['ID'], 'advisor')
                else:
                    uinput('Invalid ID.')
            case '4':
                if project.table[0]['advisor'] is '':
                    uinput('You need to request an advisor first.')
                    continue
                elif project.table[0]['stage'] == 'draft':
                    send_request(project, project.table[0]['advisor'], 'submit')
                    project.upsert({'stage': 'submitted'})
                elif project.table[0]['stage'] == 'accepted':
                    send_request(project, project.table[0]['advisor'], 'submitreport')
                    project.upsert({'stage': 'submittedreport'})
                db.write('projects.csv')
            case '5':
                if project.table[0]['head'] != user['ID'] and user['type'] != 'admin':
                    project.upsert({'advisor': None}, where={'advisor': user['ID']})
                    project.upsert({'member1': None}, where={'member1': user['ID']})
                    project.upsert({'member2': None}, where={'member2': user['ID']})
                    db.write('projects.csv')
                    return None
                project.select(['ID', 'name', 'project_data', 'stage']).print()
                string = uinput('Are you sure you want to delete this project? enter the "ID" of the project to confirm:')
                if string == project.table[0]['ID']:
                    db.select('projects').drop(where={'ID': project.table[0]['ID']})
                    db.write('projects.csv')
                    return None
            case 'back':
                return None

def create_project():
    # ID,name,head,member1,member2,advisor,project_data
    os.system('cls' if os.name == 'nt' else "printf '\033c'")
    data = {'ID': rnd_id(), 'name': uinput('Enter project name: '), 'head': user['ID'], 'member1': None, 'member2': None, 'advisor': None, 'project_data': uinput('Enter project data: '),'stage': 'draft'}
    db.select('projects').upsert(data)
    db.write('projects.csv')

def get_request():
    requests = db.select('requests', where={'ID': user['ID']})
    if requests is None:
        print('You have no requests')
    else:
        print('You have ' + str(len(requests)) + ' requests.')
        for request in requests.table:
            print('{Project: "' + request['project_name'] + '" type: "' + request['type'] +'"}')
            string = 'Enter "accept" to accept the request or "decline" to decline it.'
            print(line(len(string)))
            print(string)
            unip = uinput()
            if unip == 'accept':
                if request['type'] == 'member':
                    print('none')
                    if db.select('projects', where={'ID': request['project']}).table[0]['member1'] is '':
                        print("yesss")
                        db.select('projects').upsert({'member1': user['ID']}, where={'ID': request['project']})
                    elif db.select('projects', where={'ID': request['project']}).table[0]['member2'] is '':
                        db.select('projects').upsert({'member2': user['ID']}, where={'ID': request['project']})
                elif request['type'] == 'advisor':
                    db.select('projects').upsert({'advisor': user['ID']}, where={'ID': request['project']})
                elif request['type'] == 'submit':
                    db.select('projects').upsert({'stage': 'accepted'}, where={'ID': request['project']})
                elif request['type'] == 'submitreport':
                    db.select('projects').upsert({'stage': 'finished'}, where={'ID': request['project']})
                db.select('requests').drop(where={'ID': user['ID'], 'project': request['project']})
                print('Request accepted.')
                db.write('projects.csv').write('requests.csv')
            elif unip == 'decline':
                if request['type'] == 'submit':
                    db.select('projects').upsert({'stage': 'draft'}, where={'ID': request['project']})
                elif request['type'] == 'submitreport':
                    db.select('projects').upsert({'stage': 'accepted'}, where={'ID': request['project']})
                db.select('requests').drop(where={'ID': user['ID'], 'project': request['project']})
                uinput('Request declined.')
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

def uinput(string = '',lower = True):
    unip = input(string)
    if lower:
        unip.lower()
    if unip == 'exit':
        exit()
    elif unip == 'logout':
        main()
        return
    return unip

def login():
    # ask the user to enter the username and password 3 times
    for _ in range(3):
        print('--------Login--------')
        username = uinput("username: ",False)
        password = uinput("password: ",False)
        # check if the user id exists and the password matches
        if db.select('login', where={'username': username, 'password': password}) is not None:
            return db.select('login', where={'username': username, 'password': password}).table[0]['ID']
        uinput('Login failed. Please try again.')
        os.system('cls' if os.name == 'nt' else "printf '\033c'")
    uinput('You have exceeded the maximum number of tries. Please try again later.')
    exit()
    return None

def exit():
    # write out all the tables that have been modified to the corresponding CSV files
    db.write('persons.csv')\
        .write('login.csv')\
        .write('projects.csv')\
        .write('requests.csv')
    sys.exit()

def main():
    os.system('cls' if os.name == 'nt' else "printf '\033c'")
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
        string = 'SKE-FP: V0.14 | Welcome '+ user['type'] + " " + user['fist'] + ' ' + user['last'] + '. "exit" to exit. "logout" to relog'
        print( '\n' + line(len(string)))
        print(string)
        print(line(len(string)))
        get_request()
        get_project()

main()


