from sanic import Sanic
from views.train_view import rasa
import logging
logger = logging.getLogger(__file__)
app = Sanic(__name__)
app.blueprint(rasa)
