from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS
from starcoin.sdk import utils
from pathlib import Path
import json
from typing import Optional

app = Flask(__name__)
cors = CORS(app)
api = Api(app)


def get_user_from_session(session) -> Optional[str]:
    db = {}
    if Path("db.json").exists():
        with open("db.json") as f:
            db = json.load(f)
    # FIXME: get address from session id
    for k, v in db.items():
        if v['session'] == session:
            return k
    return None


def hex_list_to_str(hex_list: list) -> str:
    return "".join([chr(i) for i in hex_list])


class Verify(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        sign = json_data['sign']
        public_address = json_data['from']
        signed_message = utils.verify_signed_message(sign)
        db = {}
        if Path("db.json").exists():
            with open("db.json") as f:
                db = json.load(f)
        session = hex_list_to_str(signed_message.message.value)
        user_id = get_user_from_session(session)
        
        if db[user_id]['wallet_address'].lower() == public_address.lower():
            with open('db.json', 'w') as f:
                db[user_id]['verified'] = True
                json.dump(db, f)
            return {'status': 'success'}
        return {'status': 'fail'}


api.add_resource(Verify, '/verify')

if __name__ == '__main__':
    app.run(debug=True)
