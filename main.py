import numpy as np 
import pandas as pd 
import dask.dataframe as dd
import json 
import os 
import shutil
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from scripts.func import df_preprocess
from handler.awshandler import *
from handler.ziphelper import *
import config
from flask import Flask, request

# s3 config
aws_config = config.s3
accessKey = aws_config['aws_access_key_id']
secretKey = aws_config['aws_secret_access_key']
region = aws_config['region']
bucket = aws_config['bucket']

app = Flask(__name__)

logger = logging.getLogger(__name__)
logging.basicConfig(filename="train.log", filemode='a', level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

@app.route("/train", methods=['POST'])
def run():
    try:
        """Train Anomaly model
        Input: json_link
        Output: model file and upload to S3"""
        # post request
        json_link = str(request.get_json(force=True)['json_link'])

        # variables
        logging.info("get variables")
        model_file_name = os.path.basename(json_link).split(".")[0]
        mdir = os.path.join(config.MODELS_DIR, model_file_name)
        logging.info(f"mdir is: {mdir}")
        hashword = None
        zip_type = ".tar.gz"


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
        df_matrix = df.drop(columns=['post_timestamp', 'live_sid', 'post_message'])
        df = df_preprocess(df_matrix, array['t_period'], array['comment_f'])

        # train model
        logging.info("train model")
        model_path = os.path.join(mdir, model_file_name+'.pkl')
        df_out = m_pipeline(df, model_path)
        l_time = list(set(df_out.index))
        df = df[df['period'].isin(l_time)]

        
        # remove s3_link json file
        os.remove(os.path.join(mdir,model_file_name+'.json'))
        '''
        # zip word2idx.json, tag2idx.json and model files
        logging.info("zip file")
        zip_helper = Ziphelper(mdir, config.MODELS_DIR, model_file_name, zip_type, "")
        zip_helper.compressor()

        # hash
        logging.info("hashing")
        hashword = get_digest(os.path.join(config.MODELS_DIR, model_file_name + zip_type))
        logging.info(f"The directory before hash: {model_file_name}{zip_type}")
        logging.info(f"The hashword is {hashword}")

        # upload s3
        logging.info("upload to s3")
        local_path = os.path.join(config.MODELS_DIR, model_file_name + zip_type)
        m_folder = os.path.basename(os.path.normpath(config.MODELS_DIR))
        s3_path = os.path.join(m_folder, model_file_name)
        aws_handler = AWSHandler(accessKey, secretKey, region, bucket)
        aws_handler.upload_2S3(s3_path, local_path)'''

        return json.dumps({'array_text':df.to_dict('records')})
    except Exception as e:
        logging.error(f"Error message is {e}")
        return json.dumps({'error': f'Error message is {e}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, port=config.port, debug=True)
