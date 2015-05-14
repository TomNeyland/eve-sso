from fixture import SQLAlchemyFixture, DataSet
from evesso import db
from evesso.models import Chatroom

dbfixture = SQLAlchemyFixture(env={'ChatroomData': Chatroom}, engine=db.engine)

class ChatroomData(DataSet):

    class notifications:
        name = "notifications"
        motd = "This chatroom contains everyone"

    class general:
        name = "general"
        motd = "gbs in here"
