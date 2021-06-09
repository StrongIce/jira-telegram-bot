#Jira конфиги
jira_login = "user" #Логин пользователя с правами админа в Jira
jira_api_key = "apikey" # API ключ для пользователя(если жира локальная, ключ получается через плагин) 
server = {'server': 'http://jira.contoso.com:8080/'} # URL сервера

#Токен бота
botToken = 'token'

#AD конфиги
ldap_srv = 'ad.contoso.com' # Контроллер домена
ldap_user = 'contoso\ldap_sync' # Учетка для синхронизации с каталогом AD
ldap_password = "password" # Пароль
ldap_ou = 'dc=contoso,dc=com' # Область поиска LDAP
