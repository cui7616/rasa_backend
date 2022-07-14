from utils.commons import read_yaml_file
from mongo.rasa_yaml import find_entities_in_training_example, replace_entities
from mongo.mongomodel import *
from logging import getLogger

logger = getLogger(__file__)


class Yaml2Dict:
    def __init__(self, filename, projectId):
        self.projectId = projectId
        self.yamlfile = read_yaml_file(filename)

    def process(self):
        if "nlu" in self.yamlfile:
            self.yaml2example()
        if "stories" in self.yamlfile:
            self.yaml2stories()
        if "rules" in self.yamlfile:
            self.yaml2rules()
        if "action_endpoint" in self.yamlfile:
            self.yaml2endpoint()
        if "pipeline" in self.yamlfile:
            self.yaml2nlu()
            self.yaml2policies()
        if "rest" in self.yamlfile or "socketio" in self.yamlfile or "rasa" in self.yamlfile:
            self.yaml2credentials()
        if "actions" in self.yamlfile:
            self.yaml2projects()
        if "slots" in self.yamlfile:
            self.yaml2slots()
            self.yaml2projects()
        return "上传成功"

    @staticmethod
    def splitfun(inputstr):
        try:
            return [item[:-1] for item in inputstr.split('- ') if item and item.endswith('\n')]
        except Exception as e:
            logger.error(e)

    def yaml2example(self):
        nlu = self.yamlfile.get('nlu')
        nlu_processed = []
        for example in nlu:
            example_list = Yaml2Dict.splitfun(example.get("examples"))
            for ee in example_list:
                example_dict = {"projectId": self.projectId, "text": replace_entities(ee),
                                "intent": example.get("intent"), "entities": find_entities_in_training_example(ee)}
                example_model = ModelExample(**example_dict)
                example_model.save()
                nlu_processed.append(example_dict)
        return nlu_processed

    def yaml2stories(self):
        stories = self.yamlfile.get('stories')
        stories = [{"title": story["story"], "steps": story["steps"], "type": "story", "projectId": self.projectId} for
                   story in stories]
        for story in stories:
            story_model = ModelStories(**story)
            story_model.save()
        return stories

    def yaml2rules(self):
        rules = self.yamlfile.get('rules')
        rules = [{"title": rule["rule"], "steps": rule["steps"], "type": "rule", "projectId": self.projectId} for rule
                 in rules]
        for rule in rules:
            rule_model = ModelStories(**rule)
            rule_model.save()
        return rules

    def yaml2endpoint(self):
        endpoints = self.yamlfile
        endpoints_model = ModelEndpoints(endpoints=endpoints, projectId=self.projectId)
        endpoints_model.save()
        return endpoints

    def yaml2slots(self):
        slots = self.yamlfile.get('slots')
        for key, value in slots.items():
            value["name"] = key
            value["projectId"] = self.projectId
            slot_model = ModelSlots(**value)
            slot_model.save()
        return slots

    def yaml2nlu(self):
        pipeline = self.yamlfile.get('pipeline')
        print(pipeline)
        nlu_model = ModelNlu(language='zh', projectId=self.projectId, pipeline=pipeline)
        nlu_model.save()

    def yaml2policies(self):
        policies = self.yamlfile.get('policies')
        policy_model = ModelPolocies(projectId=self.projectId, polices=policies)
        policy_model.save()

    def yaml2credentials(self):
        credentials = self.yamlfile
        credentials_model = ModelCredentials(projectId=self.projectId, credentials=credentials)
        credentials_model.save()

    def yaml2projects(self):
        domain = self.yamlfile
        domain_model = ModelProjects(projectId=self.projectId, defaultDomain=domain)
        domain_model.save()


if __name__ == "__main__":
    yd = Yaml2Dict("../Chapter03/domain.yml", "test")
    from pprint import pprint

    pprint(yd.process())
