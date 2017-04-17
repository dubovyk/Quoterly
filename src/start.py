from dbconnector import dbconnector

connector = dbconnector.sqliteConnector("data/Quoterly.db")

connector.drop()
connector.create()

connector.add_user('root', 'test@gmail.com', 'password')
connector.update_user('root', 'is_admin', 'true')

connector.add_user('user', 'user@gmail.com', 'password')
