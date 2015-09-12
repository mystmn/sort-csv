class Bill():

    def fields(self):
        eachField = [

            {'htmlTag': None, 'htmlDesc': None, 'dbfield': 'id'},
            {'htmlTag': 'LastName', 'htmlDesc': 'Last Name', 'dbfield': 'LastName'},
            {'htmlTag': 'FirstName', 'htmlDesc': 'First Name', 'dbfield': 'FirstName'},
            {'htmlTag': 'Address', 'htmlDesc': 'Address', 'dbfield': 'Address'},
            {'htmlTag': 'City', 'htmlDesc': 'City', 'dbfield': 'City'},
        ]
        return eachField

a = Bill()

print type(a.fields())

for g in a.fields():
    print g['htmlTag']