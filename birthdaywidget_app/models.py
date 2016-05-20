from cassandra.cqlengine.models import Model
from datetime import datetime
from cassandra.cqlengine import columns

class Userprofile(Model):
    __table_name__        = 'userprofile'
    userid                = columns.TimeUUID(primary_key=True)
    username                      = columns.Text(required=True,index=True)
    # pagename                    = columns.Text(index=True)
    # description                 = columns.Text(required=False)
    # page_url                    = columns.Text(required=False,index=True)
    # new_url                     = columns.Text(required=False,index=True)
    # telephone_number            = columns.Text(required=False)
    # cellphone_number            = columns.Text(required=False)
    # email_address               = columns.Text(required=False)
    # website                     = columns.Text(required=False)
    # created_at                  = columns.DateTime(default=datetime.now())
    # updated_at                  = columns.DateTime(default=datetime.now())
    # follower_count              = columns.Integer(default=0)
    # cover_image                 = columns.Bytes(required=False)
    # pagecoverpicurl             = columns.Text(required=False)
    # cover_thumbnail             = columns.Text(required=False)
    # background_image            = columns.Bytes(required=False)
    # background_url              = columns.Text(required=False)
    # background_thumbnail        = columns.Text(required=False)
