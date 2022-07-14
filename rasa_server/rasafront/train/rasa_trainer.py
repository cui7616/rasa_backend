import aiohttp
import asyncio
from mongo.mongo2yaml import Mongo2Yamler
import requests
import config


class RasaTrainer:

    @staticmethod
    def train(projectId,mongo2yamler):
        result_yaml = mongo2yamler.yaml_helper(projectId)
        headers = {"Content-type": "application/x-yaml","Accept":"application/octet-stream"}
        params = {"force_training": True}
        response = requests.post(
            config.train_url,
            data=result_yaml.encode('utf-8'),
            headers=headers,
            params=params,
        )
        if response.status_code == 200:
            filename = response.headers['filename']
            headers2 = {"Content-type": "application/octet-stream","File-Name":filename}
            for chunk in response.iter_content(chunk_size=1024*1024):
                print('aaa')
                if chunk:
                    r = requests.post(config.recieve_url, data=chunk, headers=headers2)
            return response.headers['filename']
        else:
            return response.reason

if __name__ == "__main__":
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(RasaTrainer.train('test'))
    print(RasaTrainer.train('test'))
