import argparse
import glob
import json
import os

import numpy as np
import pandas as pd
import requests
import soundfile as sf

from urllib.parse import urlparse, urljoin

# URL for the web service
SCORING_URI = 'https://dnsmos.azurewebsites.net/score'
# If the service is authenticated, set the key or token
AUTH_KEY    = 'c2luZ2Fwb3JldGVjaC1lZHU6ZG5zbW9z'

# Set the content type
headers = {'Content-Type': 'application/json'}
# If authentication is enabled, set the authorization header
headers['Authorization'] = f'Basic {AUTH_KEY }'


def dnsmos(header, ns, ne, score_file, flag):

    #audio_clips_list = glob.glob(os.path.join(args.testset_dir, "*.wav"))
    audio_clips_list = []
    scores = []
    count = 0
    time_log = os.path.join('./exp', flag+'_dnmos.log')

    for i in range(ns,ne):
            file = header+str(i) + "/0_sph_est.wav"
            if os.path.isfile(file):
               audio_clips_list.append(file)

    for fpath in audio_clips_list:
            count = count + 1
            try:
                audio, fs = sf.read(fpath)
                if fs != 16000:
                    print('Only sampling rate of 16000 is supported as of now')
                data = {"data": audio.tolist()}
                input_data = json.dumps(data)
                # Make the request and display the response
                u = urlparse(SCORING_URI)
                resp = requests.post(urljoin("https://" + u.netloc, 'score'), data=input_data, headers=headers)
                score_dict = resp.json()
                score_dict['file_name'] = os.path.basename(fpath)
                scores.append(score_dict)

                with open(time_log, 'a+') as f:
                    print(fpath,',', score_dict['mos'],file=f)
                    f.flush()

                print(count)
            except Exception as ex:
                 print('skip',count)

    df = pd.DataFrame(scores)
    print('Mean MOS Score for the files is ', np.mean(df['mos']))
    df.to_csv(score_file)

if __name__=="__main__":

	
	audio, fs = sf.read('/home/test/DeepFilterNet/DeepFilterNet/DeepFilterNet/tt_48001_mix_models.wav')
	if fs != 16000:
	    print('Only sampling rate of 16000 is supported as of now')
	data = {"data": audio.tolist()}
	input_data = json.dumps(data)
	# Make the request and display the response
	u = urlparse(SCORING_URI)
	resp = requests.post(urljoin("https://" + u.netloc, 'score'), data=input_data, headers=headers)
	score_dict = resp.json()
	score_dict['file_name'] = os.path.basename(fpath)
	scores.append(score_dict)
	





    
