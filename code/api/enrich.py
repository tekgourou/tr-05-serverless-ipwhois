from functools import partial
from code.api import ObservableSchema
from code.api.utils import get_json, jsonify_data
from flask import Blueprint, current_app

from code.api.ipwhois import get_ip_geo

def group_observables(relay_input):
    result = []
    for observable in relay_input:
        o_value = observable['value']
        o_type = observable['type'].lower()

        if o_type in current_app.config['CCT_OBSERVABLE_TYPES']:
            obj = {'type': o_type, 'value': o_value}
            if obj in result:
                continue
            result.append(obj)
    return result

def build_input_api(observables):
    for observable in observables:
        o_value = observable['value']
        o_type = observable['type'].lower()
        if current_app.config['CCT_OBSERVABLE_TYPES'][o_type].get('sep'):
            o_value = o_value.split(
                current_app.config['CCT_OBSERVABLE_TYPES'][o_type]['sep'])[-1]
            observable['value'] = o_value
    return observables

enrich_api = Blueprint('enrich', __name__)
get_observables = partial(get_json, schema=ObservableSchema(many=True))


@enrich_api.route('/refer/observables', methods=['POST'])
def refer_observables():
    relay_input = get_json(ObservableSchema(many=True))
    observables = group_observables(relay_input)
    data = []
    if not observables:
        return ({})
    observables = build_input_api(observables)
    for observable in observables:
        o_value = observable['value']
        o_type = observable['type'].lower()
        try:
            data_json = get_ip_geo(o_value)
            if data_json['success'] != True:
                return ({})
            info = 'IP : {} \n Continent : {} \n Country : {} \n Region : {} \n City : {} \n ASN : {} \n Organization : {} \n ISP : {} \n Timezone : {}'.format(o_value, data_json['continent'], data_json['country'], data_json['region'], data_json['city'], data_json['asn'], data_json['org'], data_json['isp'], data_json['timezone']  )
            refer_url = 'https://www.google.com/maps/place/{},+{},+{}'.format(data_json['country'].replace(' ', ''),data_json['region'].replace(' ', ''),data_json['city'].replace(' ', ''))
            data.append(
                {
                    'id': 'ref_ipwhois_{}'.format(o_value),
                    'title': f'Get whois information for {o_value} ',
                    'description': info,
                    'url': refer_url,
                    'categories': ['Search', 'ipwhois']
                }
            )
        except:
            return ({})
    return jsonify_data(data)
