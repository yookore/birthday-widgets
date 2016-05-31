from rest_framework import viewsets
from birthdaywidget_app.serializers import BirthdaySerializer
from neo4jrestclient.client import GraphDatabase
from neo4jrestclient import client
from cassandra.query import dict_factory, SimpleStatement
from cassandra.auth import PlainTextAuthProvider
from cassandra.cluster import Cluster
from datetime import datetime
from rest_framework.response import Response
from rest_framework import status
from birthdaywidget_app.pagination import CustomPagination

db = GraphDatabase("http://192.168.121.157:7474", username="neo4j", password="Wordpass15")

auth_provider = PlainTextAuthProvider(username='cassandra', password='Gonzo@7072')
cluster = Cluster(
    contact_points=['192.168.121.171', '192.168.121.174', '192.168.121.172', '192.168.121.173', '192.168.121.175',
                    '192.168.121.176'], auth_provider=auth_provider)
session = cluster.connect(keyspace='yookos_upm')
session.row_factory = dict_factory

def getKey(user):
    return user['firstname']

class DefaultMixin(object):
    pagination_class = CustomPagination
    serializer_class = BirthdaySerializer

class BirthdayListViewSet(DefaultMixin,viewsets.ModelViewSet):
    serializer_class = BirthdaySerializer

    def get_queryset(self):
        friends = []
        _list = []
        today = datetime.now()

        username = self.kwargs['username']

        q = 'MATCH (u:User)-[r:FRIEND]->(m:User) WHERE u.username="%s" RETURN m ' %username

        # "db" as defined above
        results = db.query(q , returns=(client.Node, str, client.Node))

        for r in results:
            friends.append(r[0]['username'])

        # print friends
        if len(friends) != 0:
            for i in friends:
                query = "SELECT * FROM yookos_upm.userprofile WHERE username = '%s'" %i
                result = session.execute(query)

                if result[0]['birthdate'] == '' or result[0]['birthdate'] is None:
                    print "---" ,result[0]['username']

                elif result[0]['birthdate'].month == today.month and result[0]['birthdate'].day == today.day :
                    print ">>>>>> ", result[0]['firstname']

                    item = {'firstname':result[0]['firstname'] ,'lastname':result[0]['lastname'],'username':result[0]['username'],'userid':result[0]['userid'],'birthdate': result[0]['birthdate'] ,'avatarurl': result[0]['avatarurl']}

                    print "====Results===: ", item

                    _list.append(item)
                else:
                    print '###!!!', result[0]['firstname'] , result[0]['birthdate']
                    # print " NO one is birthdaying today."

            print '@@@ ', _list

            return sorted(_list,key=getKey, reverse=False)

class MonthBirthdayListViewSet(DefaultMixin,viewsets.ModelViewSet):
    serializer_class = BirthdaySerializer

    def get_queryset(self):
        friends = []
        _list = []

        username = self.kwargs['username']
        month = self.kwargs['month']

        # month = int(month)
        print " $$$$ : ", len(month)

        if len(month)== 1 or len(month)==2:
            print 'Month OK'

            month = int(month)

            if month <= 12:
                print 'OK again'

                print " Month ", type(month)

                q = 'MATCH (u:User)-[r:FRIEND]->(m:User) WHERE u.username="%s" RETURN m ' %username

                # "db" as defined above
                results = db.query(q , returns=(client.Node, str, client.Node))

                for r in results:
                    friends.append(r[0]['username'])

                if len(friends) != 0:
                    for i in friends:
                        query = "SELECT * FROM yookos_upm.userprofile WHERE username = '%s'" %i
                        result = session.execute(query)

                        if result[0]['birthdate'] == '' or result[0]['birthdate'] is None:
                            print "---" ,result[0]['username']

                        elif result[0]['birthdate'].month == month :
                            print ">>>>>> ", result[0]['firstname']

                            item = {'firstname':result[0]['firstname'] ,'lastname':result[0]['lastname'],'username':result[0]['username'],'userid':result[0]['userid'],'birthdate': result[0]['birthdate'] ,'avatarurl': result[0]['avatarurl']}
                            print "====Results===: ", item

                            _list.append(item)
                        else:
                            print '###!!!', result[0]['firstname'] , result[0]['birthdate']
                            # print " NO one is birthdaying today."

                    print '@@@ ', _list

                    return sorted(_list,key=getKey, reverse=False)
            else:
                print 'WRONG MONTH'
                return Response(data={'message':'%s is not a valid month ' %month} , status = status.HTTP_400_BAD_REQUEST)
        else:
            print 'INVALID MONTH'
            return Response('month can only have 1 or 2 number',status.HTTP_400_BAD_REQUEST)


class DateBirthdayListViewSet(DefaultMixin,viewsets.ModelViewSet):

    serializer_class = BirthdaySerializer

    def get_queryset(self):
        friends = []
        _list = []

        username = self.kwargs['username']
        month = self.kwargs['month']
        day = self.kwargs['day']

        if len(month)== 1 or len(month)==2 and len(day)==1 or len(day)==2:

            month = int(month)
            day = int(day)

            if month <= 12 and day <= 31:

                q = 'MATCH (u:User)-[r:FRIEND]->(m:User) WHERE u.username="%s" RETURN m ' %username

                # "db" as defined above
                results = db.query(q , returns=(client.Node, str, client.Node))

                for r in results:
                    friends.append(r[0]['username'])

                if len(friends) != 0:
                    for i in friends:
                        query = "SELECT * FROM yookos_upm.userprofile WHERE username = '%s'" %i
                        result = session.execute(query)

                        if result[0]['birthdate'] == '' or result[0]['birthdate'] is None:
                            print "---" ,result[0]['username']

                        elif result[0]['birthdate'].month == month and result[0]['birthdate'].day == day :
                            print ">>>>>> ", result[0]['firstname']

                            item = {'firstname':result[0]['firstname'] ,'lastname':result[0]['lastname'],'username':result[0]['username'],'userid':result[0]['userid'],'birthdate': result[0]['birthdate'] ,'avatarurl': result[0]['avatarurl']}
                            print "====Results===: ", item

                            _list.append(item)
                        else:
                            print '###!!!', result[0]['firstname'] , result[0]['birthdate']

                    return sorted(_list, key=getKey, reverse=False)
            else:
                return Response('incorrect date' , status.HTTP_400_BAD_REQUEST)
        else:
            return Response('month or day can only have 1 or 2 number',status.HTTP_400_BAD_REQUEST)

#         ListViewSet

class ListViewSet(DefaultMixin,viewsets.ModelViewSet):

    serializer_class = BirthdaySerializer

    def list(self, request, username=None, month=None):
        friends = []
        _list = []

        if len(month)== 1 or len(month)==2:

            month = int(month)

            if month <= 12:

                q = 'MATCH (u:User)-[r:FRIEND]->(m:User) WHERE u.username="%s" RETURN m ' %username

                # "db" as defined above
                results = db.query(q , returns=(client.Node, str, client.Node))

                for r in results:
                    friends.append(r[0]['username'])

                if len(friends) != 0:
                    for i in friends:
                        query = "SELECT * FROM yookos_upm.userprofile WHERE username = '%s'" %i
                        result = session.execute(query)

                        if result[0]['birthdate'] == '' or result[0]['birthdate'] is None:
                            print "---" ,result[0]['username']

                        elif result[0]['birthdate'].month == month :
                            print ">>>>>> ", result[0]['firstname']

                            item = {'firstname':result[0]['firstname'] ,'lastname':result[0]['lastname'],'username':result[0]['username'],'userid':result[0]['userid'],'birthdate': result[0]['birthdate'] ,'avatarurl': result[0]['avatarurl']}
                            print "====Results===: ", item

                            _list.append(item)
                        else:
                            print '###!!!', result[0]['firstname'] , result[0]['birthdate']
                            # print " NO one is birthdaying today."

                    serializer = BirthdaySerializer(_list, many=True)

                    return Response(sorted(serializer.data, key=getKey, reverse=False) , status.HTTP_200_OK)
            else:
                return Response(data={'message':'%s is not a valid month ' %month} , status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'month can only have one or two number'},status.HTTP_400_BAD_REQUEST)









