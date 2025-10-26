"""
JSON encoding utilities for IntellEvalPro
Provides custom JSON encoder for Decimal, date, and datetime types
"""
import json
from decimal import Decimal
from datetime import date, datetime
from flask import make_response
from flask.json.provider import JSONProvider


class DecimalEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle Decimal, date, and datetime types"""
    
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super(DecimalEncoder, self).default(obj)


class DecimalJSONProvider(JSONProvider):
    """Custom JSON provider for Flask that handles Decimal, date, and datetime types"""
    
    def dumps(self, obj, **kwargs):
        return json.dumps(obj, cls=DecimalEncoder, **kwargs)
    
    def loads(self, s, **kwargs):
        return json.loads(s, **kwargs)


def jsonify(*args, **kwargs):
    """
    Custom jsonify function that handles Decimal types
    
    Usage:
        from utils.json_encoder import jsonify
        
        @app.route('/api/data')
        def get_data():
            return jsonify({'value': Decimal('10.5')})
    """
    if args and kwargs:
        raise TypeError('jsonify() behavior undefined when passed both args and kwargs')
    elif len(args) == 1:
        data = args[0]
    else:
        data = dict(*args, **kwargs) if args else kwargs
    
    # Convert data using our custom encoder
    json_str = json.dumps(data, cls=DecimalEncoder)
    response = make_response(json_str)
    response.mimetype = 'application/json'
    return response
