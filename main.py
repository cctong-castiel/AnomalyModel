import numpy as np
import pandas as pd
import dask.dataframe as dd
import json
import os
import shutil
import logging
from scripts.func import df_preprocess
from scripts.model import m_pipeline
from handler.awshandler import *
from handler.ziphelper import *
from flask import Flask, request

app = Flask(__name__)

logger = logging.getLogger(__name__)
logging.basicConfig(filename="train.log", filemode='a', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@app.route("/pipe", methods=['POST'])
def pipe():
    try:

        """Train Anomaly model
        Input: json_link
        Output: model file and upload to S3"""

        # post request
        json_link = str(request.get_json(force=True)['json_link'])

        # variables
        logging.info("get variables")
        CWD = os.getcwd()
        MODELS_DIR = os.path.join(CWD, "models")
        model_file_name = os.path.basename(json_link).split(".")[0]
        mdir = os.path.join(MODELS_DIR, model_file_name)
        logging.info(f"mdir is: {mdir}")

        # check if mdir exist
        if os.path.exists(mdir):
            shutil.rmtree(mdir)
            os.makedirs(mdir)
            logging.info(f"mdir path in if path: {mdir}")
        else:
            os.makedirs(mdir)
            logging.info(f"mdir path in else path: {mdir}")
            logging.info(os.path.exists(mdir))

        # wget json link
        logging.info("get json link")
        logging.info(f"wget -P {mdir}/ {json_link}")
        os.system(f"wget -P {mdir}/ {json_link}")
        with open(os.path.join(mdir,model_file_name+'.json'), 'r') as json_f:
            array = json.load(json_f)

        # preprocessing
        df = pd.DataFrame(array['array_text'])
        df_matrix = df.drop(columns=['live_sid', 'post_message'])
        logging.info(f"df_matrix is: \n {df_matrix.head()}")
        logging.info(f"df_matrix info: \n {df_matrix.info()}")
        df = df_preprocess(df_matrix, array['t_period'], array['comment_f'])

        # train model
        logging.info("train model")
        df_out = m_pipeline(df)
        l_time = list(set(df_out.index))
        df = df[df['period'].isin(l_time)]

        for col in ["post_timestamp", "period"]:
            df[col] = df[col].astype(str)


        # remove s3_link json file
        os.remove(os.path.join(mdir,model_file_name+'.json'))

        return json.dumps({'array_text':df.to_dict('records')})
    except Exception as e:
        logging.error(f"Error message is {e}")
        return json.dumps({'error': f'Error message is {e}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=8964, debug=True)
