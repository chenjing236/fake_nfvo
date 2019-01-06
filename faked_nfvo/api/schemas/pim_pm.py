from faked_nfvo.api.validation import parameter_types

"([0-9]{1,3}\.){3}[0-9]{1,3}"
uri_type = {'type': 'string',
            'pattern': '^(https://)([0-9]{1,3}\.){3}[0-9]{1,3}:[0-9]{1,5}'
                       '/v1/vimPm/files/(.*)(\.gz)$'}


pim_src_type = {
    "type": "string",
    "enum": ["vpim", "pim"],
}


put_pm = {
    'type': 'object',
    'properties': {
        "Version": parameter_types.vim_pim_version,
        "VimId": parameter_types.len_constraint_string(1, 36),
        "SrcType": pim_src_type,
        "MsgType": {'type': 'string',
                    'enum': ['vimPmMetrics']},
        "FileUri": uri_type,
        },
    "required": ["Version", "VimId", "SrcType", "MsgType", "FileUri"],
    'additionalProperties': False
}

