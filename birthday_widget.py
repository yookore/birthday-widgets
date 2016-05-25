from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from cassandra.cqlengine import connection
from datetime import datetime, time
from birthdaywidget_app.broker import Broker
from birthdaywidget import settings
from threading import Timer

from cassandra.query import dict_factory, SimpleStatement

# try:
auth_provider = PlainTextAuthProvider(username='cassandra', password='Gonzo@7072')
cluster = Cluster(
    contact_points=['192.168.121.171', '192.168.121.174', '192.168.121.172', '192.168.121.173', '192.168.121.175',
                    '192.168.121.176'], auth_provider=auth_provider)
session = cluster.connect(keyspace='yookos_upm')
session.row_factory = dict_factory

# except OSError , e:
# 	print e.message

def send_message(item, verb_id):

    msg = '''{
                "actor":    "%s",
                "object":   "%s",
                "verb":     %s,
                "target":   %s,
                "time":     %s,
                "extra_context": {
                    "object_type": "birhtday",
                    "target_type": "friends",
                    "content_url": "%s"
                }

            }''' % (
    item.get('username'), item.get('userid'), verb_id , item.get('birthdate'), time(),settings.UPM_URL +"%s" % ( item.get('username')))

    print "##### ", msg
    messanger = Broker()
    messanger.publish(str(msg))


def get_profiles():
    # get today's date
    today = datetime.now()

    query = "SELECT * FROM yookos_upm.userprofile"
    statement = SimpleStatement(query_string=query, fetch_size=100)

    for item in session.execute(statement):

        if item.get('birthdate') == '' or item.get('birthdate') is None:
            print "Does not have birth date : " ,item.get('username')
            # continue
        elif item.get('birthdate').month == today.month and item.get('birthdate').day == today.day :
            print 'Celebrate birthday : ', item.get('firstname') , item.get('birthdate')
            send_message(item,18)
        else:
            print "Not birthdaying today : ",item.get('username')

if __name__ == "__main__":
    get_profiles()

current_date = datetime.today()

run_time = current_date.replace(day = current_date.day , hour=1, minute=0, second=0, microsecond=0)

run = Timer(run_time, get_profiles)
run.start()



