# Any inconsistencies in naming standards are due to
# this code integrating with an external api
from sqlalchemy import func
from sqlalchemy.types import Enum
from sqlalchemy.ext.associationproxy import association_proxy
from flask.ext.login import UserMixin
from evesso import db


GroupAuthLevel = Enum('not authed',
                      'authed',
                      'admin',
                      'blacklisted',
                      name='group_auth_level')


class Group(db.Model):

    __tablename__ = 'groups'

    name = db.Column(db.String, primary_key=True)
    description = db.Column(db.String)
    is_private = db.Column(db.Boolean, index=True)

    members = db.relationship('Character', secondary='group_users')


class GroupUser(db.Model):
    """Connects Users to Groups and indicates what 'auth_level' they have"""

    __tablename__ = 'group_users'

    CharacterID = db.Column(db.String, db.ForeignKey('characters.CharacterID'), primary_key=True)
    group_name = db.Column(db.String, db.ForeignKey('groups.name'), primary_key=True)
    auth_level = db.Column(GroupAuthLevel)


class Character(db.Model, UserMixin):

    __tablename__ = 'characters'

    CharacterID = db.Column(db.String, primary_key=True)
    mainCharacterID = db.Column(db.String, db.ForeignKey('characters.CharacterID'), nullable=True)
    CharacterName = db.Column(db.String)
    CharacterOwnerHash = db.Column(db.String)
    ExpiresOn = db.Column(db.DateTime(timezone=True))
    Scopes = db.Column(db.String)
    TokenType = db.Column(db.String)
    createdAt = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updatedAt = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    mainCharacter = db.relationship('Character', backref='other_characters', remote_side=CharacterID)

    crest_authorization = db.relationship('CrestAuthorization', backref='character', uselist=False)
    other_crest_authorizations = association_proxy('other_characters', 'crest_authorization')

    groups = db.relationship('Group', secondary='group_users')

    def get_id(self):
        return self.CharacterID

    def __repr__(self):
        return '<CharacterAuthorization %s> %s' % (self.CharacterOwnerHash, self.CharacterName)


class CrestAuthorization(db.Model):

    __tablename__ = 'crest_authorization'

    CharacterID = db.Column(db.String, db.ForeignKey('characters.CharacterID'), primary_key=True)
    access_token = db.Column(db.String)
    expires_in = db.Column(db.Integer)
    expires_at = db.Column(db.DateTime(timezone=True))
    refresh_token = db.Column(db.String)
    token_type = db.Column(db.String)

    def is_expired(self):
        False


class ChatroomCharacters(db.Model):

    __tablename__ = 'chatroom_characters'

    CharacterID = db.Column(db.String, db.ForeignKey('characters.CharacterID'), primary_key=True)
    group_name = db.Column(db.String, db.ForeignKey('chatrooms.name'), primary_key=True)


class Chatroom(db.Model):

    __tablename__ = 'chatrooms'

    name = db.Column(db.String, primary_key=True)
    motd = db.Column(db.String)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    members = db.relationship('Character', secondary='chatroom_characters')


