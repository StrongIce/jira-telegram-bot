import sqlite3
from ldap3 import Server, Connection, SIMPLE, SYNC, ASYNC, SUBTREE, ALL
import settings as var
from jira import JIRA #Подключение модуля для работы с Jira Api
import telebot 

my_bot = telebot.TeleBot(var.botToken) 


def jira_login():
    jira_options = var.server
    try:
        jira = JIRA(options=jira_options, basic_auth=(var.jira_login, var.jira_api_key))
        return jira
    except:
        return "Error login"


def create_ticket_jira(problem, fullname, user, description):
    jira = jira_login()
    jira.create_issue(fields={
        'project': {'key': 'IT'},
        'issuetype': {
            "name": "Service Request"
        },
         'reporter':{"name": user},
         'summary': problem,
         'description': description,
         'customfield_10105': fullname,
    })

def chat_id_search(chat_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        if chat_id == row[0]:
            return True             
    cursor.close()

def add_user_base(user):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor() 
    cursor.execute("INSERT OR REPLACE INTO users VALUES(?,?,?,?)", user)
    conn.commit()

def user_fullname_search(chat_id):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        if chat_id == row[0]:
            return row[2] + ' ' + row[1]
    cursor.close() 

def ad_user_search(user):
    username = user
    AD_SERVER = var.ldap_srv
    AD_USER = var.ldap_user
    AD_PASSWORD = var.ldap_password
    AD_SEARCH_TREE = var.ldap_ou
    server = Server(AD_SERVER)
    conn = Connection(server,user=AD_USER,password=AD_PASSWORD)
    conn.bind()    
    b = '(&(objectCategory=Person)(cn=' + username + '))'
    conn.search(AD_SEARCH_TREE,b, SUBTREE,
        attributes =['cn','proxyAddresses','department','sAMAccountName', 'displayName', 'telephoneNumber', 'ipPhone', 'streetAddress',
        'title','manager','objectGUID','company','lastLogon']
        )
    if len(conn.entries) == 1:
        for entry in conn.entries:
            return str(entry.sAMAccountName)
    else: 
        return False




