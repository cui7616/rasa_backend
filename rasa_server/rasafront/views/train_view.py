#from . import rasa
from train.rasa_trainer import RasaTrainer
from mongo.mongo2yaml import Mongo2Yamler
from sanic import Blueprint
from sanic import response
rasa = Blueprint("rasa",url_prefix='/rasa')

mongo2yamler = Mongo2Yamler()


@rasa.route("/train",methods=["POST",])
def train(request):
    projectId = request.form.get('projectId')
    status = RasaTrainer.train(projectId,mongo2yamler)
    return response.text(status)


@rasa.route("/getconfig",methods=["POST",])
def getconfig(request):
    projectId = request.form.get('projectId')
#    mongo2yamler = Mongo2Yamler()
    endpoints_yaml, credentials_yaml = mongo2yamler.api_helper(projectId)
    return response.json({"data":{"endpoints": endpoints_yaml, "credentials": credentials_yaml}})

@rasa.route("/getnlu",methods=["Post",])
def getnlu(request):
    projectId = request.form.get('projectId')
    train_data = mongo2yamler.yaml_helper(projectId)
    return response.json({"data":train_data})
