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
    # def create(self, request, *args, **kwargs):
    #     pass
    def get_queryset(self):
        friends = []
        _list = []

        username = self.kwargs['username']

        q = 'MATCH (u:User)-[r:FRIEND]->(m:User) WHERE u.username="%s" RETURN m ' %username

        # "db" as defined above
        results = db.query(q , returns=(client.Node, str, client.Node))

        for r in results:
            # print r[0]['username']
            friends.append(r[0]['username'])

        # print friends
        if len(friends) != 0:
            for i in friends:
                query = "SELECT * FROM yookos_upm.userprofile WHERE username = '%s'" %i
                result = session.execute(query)

                # print ">>>>>>>> ", result
                # print "<><><><> ", type(result[0])

                if result[0]['birthdate'] == '' or result[0]['birthdate'] is None:
                    print "---" ,result[0]['username']

                # elif result[0]['birthdate'].month == today.month and result[0]['birthdate'].day == today.day :
                #     print '###', result[0]['firstname'] , result[0]['birthdate']
                #     list.append({result[0]['firstname'] , result[0]['birthdate']})

                elif result[0]['birthdate'].month == 1 and result[0]['birthdate'].day == 1 :
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
    # pagination_class = CustomPagination

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

                    return Response (serializer.data , status.HTTP_200_OK)
            else:
                return Response({'message':'%s is not a valid month ' %month} , status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'month can only have one or two number'},status.HTTP_400_BAD_REQUEST)

class DateBirthdayListViewSet(DefaultMixin,viewsets.ModelViewSet):

    serializer_class = BirthdaySerializer
    # pagination_class = CustomPagination

    def list(self, request, username=None, month=None , day=None):
        friends = []
        _list = []

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
                            # print " NO one is birthdaying today."

                    serializer = BirthdaySerializer(_list, many=True)

                    return Response (serializer.data , status.HTTP_200_OK)
            else:
                return Response({'message':'incorrect date' %month} , status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'month or day can only have one or two number'},status.HTTP_400_BAD_REQUEST)

class ListViewSet(viewsets.ModelViewSet):
    serializer_class = BirthdaySerializer

    def get_queryset(self):
        friends = []
        _list = []

        username = self.kwargs['username']
        month = self.kwargs['month']

        # month = int(month)
        print " $$$$ : ", len(month)

        if len(month)== 1 or len(month)==2:

            month = int(month)

            if month <= 12:

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
                resp = {'message':'<"%s"> is not a valid month ' %month}
                return Response(resp , status.HTTP_400_BAD_REQUEST)
        else:
            res = 'month can only have one or two number'
            return Response(res,status.HTTP_400_BAD_REQUEST)

#         res = {'error': 404, 'errorMessage': 'Not found', 'errors': ''}
#             return Response(res, status=status.HTTP_404_NOT_FOUND)







