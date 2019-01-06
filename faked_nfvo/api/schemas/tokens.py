get_token = {
    'type': 'object',
    'properties': {
        'VimId': {
            'type': 'string',
            'minLength': 36, 'maxLength': 36,
        }
    },
    'required': ['VimId']
}

token_for_nfvo = {
    'status_code': [201],
    'response_body': {
        'type': 'object',
        'properties': {
            'Token': {'type': 'string'},
            'IssuedAt': {'type': 'string'},
            'ExpiresAt': {'type': 'string'},
            'CallBackUris': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'UriType': {'type': 'string'},
                        'CallBackUri': {'type': 'string'}
                    }
                }
            }

        }
    },
    'required': ['Token', 'IssuedAt', 'ExpiresAt', 'CallBackUris']
}
