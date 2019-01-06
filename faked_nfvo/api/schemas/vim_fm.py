from faked_nfvo.api.validation import parameter_types

vim_src_type = {
    "type": "string",
    "enum": ["vpim", "vim"],
}

vim_msg_type = {
    "type": "string",
    "enum": ["vimFmAlarm", "vimFmActiveAlarms", "vimFmHisAlarms", "vimFmHeartbeat"],
}

alarm_list = {
    "type": "array",
    'items': {
        "type": "object",
        "properties": {
            "alarmTitle": {
                "type": "string",
            },
            "alarmStatus": {
                "type": "integer",
            },
            "alarmType": {
                "type": "string",
            },
            "origSeverity": {
                "type": "integer",
            },
            "eventTime": {
                "type": "string",
                "format": "date-time"
            },
            "alarmId": {
                "type": "string",
            },
            "msgSeq": {
                "type": "integer",
            },
            "specificProblemID": {
                "type": "string",
            },
            "specificProblem": {
                "type": "string",
            },
            "neUID": {
                "type": "string",
            },
            "neName": {
                "type": "string",
            },
            "neType": {
                "type": "string",
            },
            "objectUID": {
                "type": "string",
            },
            "objectName": {
                "type": "string",
            },
            "objectType": {
                "type": "string",
            },
            "locationInfo": {
                "type": "string",
            },
            "addInfo": {
                "type": "string",
            },
            "PVFlag": vim_src_type
        }
    }
}

vim_fm_push_info = {
    "type": "object",
    "properties": {
        "Version": parameter_types.vim_pim_version,
        "VimId": parameter_types.len_constraint_string(1, 36),
        "SrcType": vim_src_type,
        "AlarmList": alarm_list,
        "MsgType": vim_msg_type,
        "CurrentBatch": {
            "type": "integer",
            "minimum": 1,
        },
        "TotalBatches": {
            "type": "integer",
            "minimum": 1,
        },
    },
    "required": ["Version", "VimId", "SrcType", "MsgType"],
}
