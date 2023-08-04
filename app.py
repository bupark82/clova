import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv() # load environment variables from .env file

# -*- coding: utf-8 -*-

import base64
import json
import http.client

st.write("""
         # My first app 
         """)

class CompletionExecutor:
    def __init__(self, host, api_key, api_key_primary_val, request_id):
        self._host = host
        self._api_key = api_key
        self._api_key_primary_val = api_key_primary_val
        self._request_id = request_id

    def _send_request(self, completion_request):
        headers = {
            'Content-Type': 'application/json; charset=utf-8',
            'X-NCP-CLOVASTUDIO-API-KEY': self._api_key,
            'X-NCP-APIGW-API-KEY': self._api_key_primary_val,
            'X-NCP-CLOVASTUDIO-REQUEST-ID': self._request_id
        }

        conn = http.client.HTTPSConnection(self._host)
        conn.request('POST', '/testapp/v1/tasks/00v4sxbx/search', json.dumps(completion_request), headers)
        response = conn.getresponse()
        result = json.loads(response.read().decode(encoding='utf-8'))
        conn.close()
        return result

    def execute(self, completion_request):
        res = self._send_request(completion_request)
        if res['status']['code'] == '20000':
            return res['result']['outputText']
        else:
            return 'Error'


if __name__ == '__main__':
    completion_executor = CompletionExecutor(
        host='clovastudio.apigw.ntruss.com',
        api_key = os.environ["API_KEY"],
        api_key_primary_val = os.environ["API_KEY_PRIMARY_VAL"],
        request_id = os.environ["REQUEST_ID"]
    )

    col1, col2 = st.columns(2)
    with col1: 
    # preset_text = 'input text'
        preset_text = '5억원 무이자 융자는 되고 7천만원 이사비는 안된다'
        title = st.text_area('Input Text:', preset_text)

        request_data = {
            # 'text': preset_text,
            'text': title,
            'includeAiFilters': True
        }

        response_text = completion_executor.execute(request_data)
        # print(preset_text)
        # print(response_text)




# st.write( 
#     preset_text
#     )

# st.write(
#     response_text
# )

# title = st.text_input('Input Text:', preset_text)
# st.write(title)

# response = completion_executor.execute(request)
with col2:
    st.write('Response')
    st.write(response_text)