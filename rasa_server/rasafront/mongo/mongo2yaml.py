from ruamel.yaml import StringIO
import ruamel.yaml as yaml
from logging import getLogger
from mongo.mongomodel import *
from pprint import pprint
from ruamel.yaml.scalarstring import LiteralScalarString
from mongo.utils import all_subclasses

logger = getLogger(__file__)


class Mongo2Yamler:
    def __init__(self):
        # self.projectId = projectId
        self.yamls = {}
        self._regist_all_model()

    def _regist_all_model(self):
        models = all_subclasses(ModelImp)
        for model in models:
            self.register_model(model())

    def register_model(self,model):
        if model.mode().startswith("yaml"):
            self.yamls[model.mode()] = model.mongo2dict
            logger.debug("registed the mode:{}".format(model.mode()))
        # elif: model.mode().startswith("api"):
            # self.api[model.mode()] =  model.mongo2dict

    def yaml_helper(self,projectId):
        result = {"language": "zh"}
        for model,f in self.yamls.items():
            result.update(f(projectId)) 
        stream = StringIO()
        dumper = yaml.YAML()
        dumper.dump(result, stream)
        result_yaml = stream.getvalue()
        return result_yaml

    def api_helper(self,projectId):
        endpoints = ModelEndpoints().mongo2dict(projectId)
        credentials = ModelCredentials().mongo2dict(projectId)
        return endpoints, credentials



if __name__ == "__main__":
    # my = Mongo2Yamler('test')
    # print(my.mongo2yaml())
    ec = EndpointAndCredentials()
    pprint(ec.mongo2yaml('test'))
