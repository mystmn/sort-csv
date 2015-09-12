from flask import Flask
from storage import backbone
from model import func as func_
from wtforms import StringField, validators
from flask_wtf import Form

app = Flask(__name__)

''' Name your Table '''


def req(msg=None):
    if msg:
        msg_new = "Please enter %s" % msg
        return [validators.DataRequired(msg_new)]
    else:
        return None


def fields():
    eachField = [

        #           Bill(
        #                   id int NOT NULL PRIMARY KEY,
        #                   LastName varchar(255) NOT NULL,
        #                   FirstName varchar(255),
        #                   Address varchar(255),
        #                   City varchar(255)
        #           );

        {'htmlTag': "id", 'htmlDesc': "ID", 'dbfield': 'id'},
        {'htmlTag': 'LastName', 'htmlDesc': 'Last Name', 'dbfield': 'LastName'},
        {'htmlTag': 'FirstName', 'htmlDesc': 'First Name', 'dbfield': 'FirstName'},
        {'htmlTag': 'Address', 'htmlDesc': 'Address', 'dbfield': 'Address'},
        {'htmlTag': 'City', 'htmlDesc': 'City', 'dbfield': 'City'}
    ]
    return eachField


class Bill(Form):
    fields = fields()
#    field0 = StringField(fields[0]['htmlTag'])
    field1 = StringField(fields[1]['htmlTag'], req(fields[1]['htmlDesc']))
    field2 = StringField(fields[2]['htmlTag'], req(fields[2]['htmlDesc']))
    field3 = StringField(fields[3]['htmlTag'])
    field4 = StringField(fields[4]['htmlTag'])


class dbStructure(object):
    def __init__(self):
        ''' Takes the URL Query request, compares to our static dict, and looks through our database '''
        ''' {Table Name: Code Name found through URL Query } '''
        self.tableNames = {'Bill': 'billing', 'cows': 'test', 'queryTableNames': 'd'}

        ''' Same thing here, URL Query to predetermined dict, compares and continues to database '''
        self.operatorList = {'SELECT': 'view', 'CREATE': 'insert', 'DROP': 'delete', 'UPDATE': 'update'}

        ''' Let's put our database connection on standby'''
        self.feedDB = backbone.get_db()

        self.default = {}

    def mainGET(self, queryTableName=None, queryOperator=None, dbColumnSearch=None):
        '''
        Example:
            [queryOperator=SELECT] [dbColumnSearch=id, name, date] FROM [queryTableName=Billing]
        '''

        ''' '''
        secureTableName = func_.dictValueExist(queryTableName, self.tableNames)

        tableOperator = func_.dictValueExist(queryOperator, self.operatorList)

        if self.verifyTableExistence(secureTableName):

            if tableOperator:

                return self.dbSelectForResults(secureTableName, tableOperator, dbColumnSearch)

                # self.dataInsertion(self, queryTableName, Bill.fields(), dataNeedingToBeInserted)

            else:
                a = {"Table Exist, no operator specified": False}

        else:
            msg = "The requested table doesn't exist '%s'" % secureTableName
            self.default = {msg: False}

            return self.default

        return a

    def mainPOST(self, table, listData):

        secureTableName = func_.dictValueExist(table, self.tableNames)

        a = []

        for h in fields():
            a.append(h['dbfield'])

        query = 'INSERT INTO %s (%s) VALUES (%s)' % (
            secureTableName,
            ', '.join(a),
            ', '.join(['?'] * len(listData))
        )

        try:
            self.feedDB.execute(query)
            return "BAM!"

        except:
            return "Didn't work"

    def dbSelectForResults(self, table=None, operator=None, searchColumns="*"):
        db = backbone.get_db()
        listSelection = ", ".join(searchColumns)

        try:
            cur = db.execute(operator + ' ' + listSelection + ' FROM ' + table)

            return cur.fetchall()

        except:

            self.default = {"No Results found or error with operator": False}

    def verifyTableExistence(self, table=None):

        try:
            self.feedDB.execute('SELECT 1 FROM ' + table + ' LIMIT 1;')
            return True

        except:
            self.default = {"Table doesn't exist", False}

    def tablecreation(self, naming):
        self.feedDB.execute(
            "CREATE Table " + naming + " (id integer, chair varchar(52) NOT Null)")

    def nothing(self):
        print ''
        '''
        create table dbNames(
            id integer PRIMARY KEY autoincrement,
            name varchar(255) NOT NULL,
            description varchar(255) NOT NULL,
            datatype varchar(255),
            dateCreated DATE
        );
        '''
