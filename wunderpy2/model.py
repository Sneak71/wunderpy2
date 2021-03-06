# Represents the Wunderlist data model

# TODO Potentially make these actual classes and parse the JSON we get back from Wunderlist so we can hand the users classes to work with (intead of dicts)? Looked at the 'colander' module for this, but it didn't really do anything more than's being done right now...

class _WunderlistObj:
    ''' Basic block of all Wunderlist communication '''
    ID = 'id'
    REVISION = 'revision'

class _WunderlistEntity(_WunderlistObj):
    ''' Entity with creation timestamp properties '''
    # NOTE these may be null for certain things, like the inbox
    CREATION_REQUEST_ID = 'created_by_request_id'
    CREATION_TIMESTAMP = 'created_at'
    CREATED_BY_ID = 'created_by_id'

class List(_WunderlistEntity):
    ''' POPO to contain list JSON keys '''
    TITLE = 'title'
    OWNER_ID = 'owner_id'
    OWNER_TYPE = 'owner_type'  # Seems to always be 'user'
    TYPE = 'list_type'
    PUBLIC = 'public'

class Task(_WunderlistEntity):
    ''' POPO to contain task JSON keys '''
    ASSIGNEE_ID = 'assignee_id'
    ASSIGNER_ID = 'assigner_id'
    DUE_DATE = 'due_date'
    LIST_ID = 'list_id'
    STARRED = 'starred'  # boolean
    TITLE = 'title'
    TYPE = 'type'
    COMPLETED = 'completed' # boolean
    RECURRENCE_COUNT = 'recurrence_count'
    RECURRENCE_TYPE = 'recurrence_type'

class Subtask(_WunderlistEntity):
    ''' POJO Containing subtask JSON keys '''
    TITLE = 'title'
    TASK_ID = 'task_id'
    COMPLETED = 'completed'
    TYPE = 'type'

class Membership(_WunderlistObj):
    ''' POJO Containing membership JSON keys '''
    USER_ID = "user_id"
    LIST_ID = "list_id"
    STATE = "state"
    TYPE = "type" # Always 'membership'?
    OWNER = "owner" # boolean
    MUTED = "muted" #boolean

# NOTE Wunderlist automatically creates positions objects, so they don't have creation information
class _PositionsObj(_WunderlistObj):
    VALUES = 'values'
    TYPE = 'type'

class ListPositionsObj(_PositionsObj):
    pass

class TaskPositionsObj(_PositionsObj):
    LIST_ID = 'list_id'

class SubtaskPositionsObj(_PositionsObj):
    TASK_ID = 'task_id'

class Note(_WunderlistObj):
    # NOTE Notes don't seem to get any creation info: user, timestamp, or request 
    TASK_ID = 'task_id'
    TYPE = 'type'   # Always 'note'?
    CONTENT = 'content'

class ReccurrenceTypes():
    DAY = 'day'
    WEEK = 'week'
    MONTH = 'month'
    YEAR= 'year'

class User(_WunderlistObj):
    ''' POPO to contain user JSON keys '''
    NAME = "name"
    CREATION_TIMESTAMP = "created_at"
    UPDATE_TIMESTAMP = "updated_at"
    TYPE = "type" # Always 'user'?
    EMAIL = "email"

class Webhooks(_WunderlistObj):
    LIST_ID = "list_id"
    MEMBERSHIP_ID = "membership_id"
    MEMBERSHIP_TYPE = "membership_type"
    URL = "url"
    PROCESSOR_TYPE = "processor_type"
    CONFIGURATIN = "configuration"
    UPDATE_TIMESTAMP = "updated_at"
