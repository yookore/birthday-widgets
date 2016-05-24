from cassandra.cqlengine.models import Model
from datetime import datetime
from cassandra.cqlengine import columns

class Userprofile(Model):
    __table_name__        = 'userprofile'
    userid                = columns.TimeUUID(primary_key=True)
    username              = columns.Text(primary_key=True,required=True,index=True)
    avatarurl             = columns.Text()
    biography             = columns.Text()
    birthdate             = columns.Text()
    creationdate = columns.DateTime()
    currentcity = columns.Text()
    currentcountry = columns.Text()
    firstname = columns.Text()
    gender = columns.Text()
    lastname = columns.Text()
    title = columns.Text()

