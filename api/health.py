from flask import Blueprint
from api.utils import jsonify_data
from api.ipwhois import get_ip_geo
health_api = Blueprint('health', __name__)


@health_api.route('/health', methods=['POST'])
def health():
    try:
        get_ip_geo('208.67.222.222')
        return jsonify_data({'status': 'ok'})
    except:
        return jsonify_data({})


