from mongoengine import connect
from mongoengine import Document, StringField, DateTimeField, IntField, EmbeddedDocumentField, EmbeddedDocument, \
    ListField
from mongoengine import *
from datetime import datetime
import json
from mongo.utils import *
import config

connect(config.database, host=config.mongo_url)


class ModelImp:

    def mode(slef):
        return NotImplementedError("An Model must implement a mode")

    def mongo2dict(self,projectId):
        return NotImplementedError("An Model must implement its mongo2dict method")


class ModelExample(Document,ModelImp):
    meta = {"collection": "example"}
    text = StringField(required=True)
    intent = StringField(required=True)
    projectId = StringField(required=True)
    entities = ListField()
    createAt = DateTimeField(default=datetime.utcnow())
    updateAt = DateTimeField(default=datetime.utcnow())

    def mode(self):
        return "yaml_example"

    def mongo2dict(self,projectId):
        examples = ModelExample.objects(projectId=projectId)
        examples = [m2d_fields(example, 'text', 'intent', 'entities') for example in examples]
        examples_dict = example2dict(examples)
        examples = [value for key, value in examples_dict.items()]
        result = {"nlu": examples}
        return result



class ModelStories(Document,ModelImp):

    meta = {"collection": "stories"}
    steps = ListField()
    title = StringField(required=True)
    type = StringField()
    textIndex = StringField()
    events = ListField()
    metadata = DictField()
    projectId = StringField(required=True)
    condition = ListField()

    def mode(self):
        return "yaml_story"

    def mongo2dict(self,projectId):
        stories = ModelStories.objects(projectId=projectId)
        stories = [m2d_fields(story, 'title', 'type', 'steps', 'condition') for story in stories]
        stories_dict = {"stories": [{'story': story['title'], 'steps': story['steps']}
                                    for story in stories if story['type'] == 'story']}
        result = {"rules": [{'rule': story['title'], 'steps': story['step'], 'condition': story['condition']}
                                for story in stories if story['type'] == 'rule']}
        result.update(stories_dict)
        return result


class ModelSlots(Document,ModelImp):

    meta = {"collection":"slots"}
    name = StringField()
    type = StringField()
    projectId = StringField()
    influence_conversation = BooleanField()
    initial_value = StringField()

    def mode(self):
        return "yaml_slot"

    def mongo2dict(self,projectId):
        return {}

class ModelProjects(Document,ModelImp):

    meta = {"collection":"projects"}
    name = StringField()
    defaultLanguage = StringField()
    projectId = StringField()
    defaultDomain = DictField()
    nluThreshold = FloatField()
    updatedAt = DateTimeField(default=datetime.utcnow())
    training = DictField()

    def mode(self):
        return "yaml_project"

    def mongo2dict(self,projectId):
        result = ModelProjects.objects(projectId=projectId)[0].to_mongo().to_dict()['defaultDomain']
        return result


class ModelBotResponses(Document,ModelImp):
    meta = {"collection":"botResponses"}
    key = StringField()
    projectId = StringField()
    textIndex = StringField()
    values = ListField()#返回形式多样

    def mode(self):
        return "yaml_response"

    def mongo2dict(self,projectId):
        return {}


class ModelForms(Document,ModelImp):
    meta = {"collection":"forms"}
    name = StringField()
    projectId = StringField()
    content = DictField()

    def mode(self):
        return "yaml_form"

    def mongo2dict(self,projectId):
        return {}


class ModelEndpoints(Document,ModelImp):
    meta = {"collection":"endpoints"}
    endpoints = DictField()
    projectId = StringField()
    environment = StringField(default="development")
    updatedAt = DateTimeField(default=datetime.utcnow())

    def mode(self):
        return "api_endpoints"

    def mongo2dict(self,projectId):
        result = ModelEndpoints.objects(projectId=projectId)[0].to_mongo().to_dict()['endpoints']
        return result


class ModelCredentials(Document,ModelImp):
    meta = {"collection":"credentials"}
    projectId = StringField()
    environment = StringField(default="development")
    credentials = DictField()
    updatedAt = DateTimeField(default=datetime.utcnow())

    def mode(self):
        return "api_endpoints"

    def mongo2dict(self,projectId):
        result = ModelCredentials.objects(projectId=projectId)[0].to_mongo().to_dict()['credentials']
        return result


class ModelPolocies(Document,ModelImp):
    meta = {"collection": "core_policies"}
    projectId = StringField()
    polices = ListField()
    updatedAt = DateTimeField(default=datetime.utcnow())

    def mode(slef):
        return "yaml_policy"

    def mongo2dict(self,projectId):
        policies = ModelPolocies.objects(projectId=projectId)[0].to_mongo().to_dict()
        result = {"policies": policies["polices"]}
        return result


class ModelNlu(Document,ModelImp):
    meta = {"collection": "nlu_model"}
    projectId = StringField()
    language = StringField()
    pipeline = ListField()
    updatedAt = DateTimeField(default=datetime.utcnow())

    def mode(self):
        return "yaml_nlu"

    def mongo2dict(slef,projectId):
        nlu = ModelNlu.objects(projectId=projectId)[0].to_mongo().to_dict()
        result = {"pipeline": nlu["pipeline"]}
        return result

