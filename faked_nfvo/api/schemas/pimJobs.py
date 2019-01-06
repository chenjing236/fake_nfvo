listsubscriptions = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'NfvoId': {
                'type': 'string',
                'maxLength': 36,
            },
            'IdentityUri': {
                'type': 'string',
                'maxLength': 255,
            },
            'qType': {
                'type': 'string',
                'maxLength': 5,
            },
            'Period': {
                'type': 'integer',
                'maxLength': 8,
            },
            'HeartbeatCm': {
                'type': 'integer',
                'maxLength': 8,
            },
            'HeartbeatFm': {
                'type': 'integer',
                'maxLength': 8,
            }
        },
        'required': ['NfvoId', 'IdentityUri', 'qType']
    }
}
createsubscription = {
    'status_code': [201],
    'response_body': {
        'type': 'object',
        'properties': {
            'VimId': {
                'type': 'string',
                'maxLength': 36,
            }
        },
        'required': ['VimId']
    }
}
deletesubscription = {
    'status_code': [201]
}
