from faked_nfvo.api.validation import parameter_types

available_zone = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'Name': parameter_types.len_constraint_string(1, 36),
            'cRegion': parameter_types.len_constraint_string(1, 36),
        },
        'required': ['Name', 'cRegion']
    }
}

host_aggregation = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'Name': parameter_types.len_constraint_string(1, 36),
            'cAZ': parameter_types.len_constraint_string(0, 36)
        },
        'required': ['Name', 'cAZ']
    }
}

hosts_info = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'SerialNumber': parameter_types.len_constraint_string(1, 20),
            'Hostname': parameter_types.len_constraint_string(1, 36),
            'cHAs': parameter_types.multi_params({'type': 'string'}),
            'MgmtV4IP': parameter_types.cidr,
            'MgmtV6IP': parameter_types.cidr,
            'HostType': parameter_types.len_constraint_string(1, 16),
            'vCpuTotal': {'type': 'integer'},
            'vRamTotal': {'type': 'number'},
            'BandWidth': {'type': 'integer'},
            'OpsStatus': {
                'type': 'string',
                'enum': ['UNKNOWN', 'UP', 'DOWN', 'MAINTENANCE']
            }
        },
        'required': ['SerialNumber', 'Hostname', 'cHAs', 'HostType', 'OpsStatus']
    }
}

storages_info = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'Backend': parameter_types.len_constraint_string(1, 36),
            'TotalCapacity': {'type': 'integer'}
        },
        'required': ['Backend', 'TotalCapacity']
    }
}

res_pool_info = {
    'type': 'object',
    'properties': {
        'Regions': parameter_types.multi_params({'type': 'string'}),
        'AZs': available_zone,
        'HAs': host_aggregation,
        'Hosts': hosts_info,
        'Storages': storages_info
    },
    'required': ['Regions', 'AZs', 'HAs', 'Hosts', 'Storages']
}

vNics_array = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'vNicMac': parameter_types.mac_address,
            'vNicId': parameter_types.len_constraint_string(36, 36),
            'vNicIPs': {
                'type': 'array',
                'items': {'type': 'string', 'format': 'cidr'}
            }
        },
        'required': ['vNicMac', 'vNicId', 'vNicIPs']
    }

}

vDisks_array = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'Name': parameter_types.len_constraint_string(1, 36),
            'vDiskId': parameter_types.len_constraint_string(36, 36),
            'Backend': parameter_types.len_constraint_string(0, 36),
            'Size': {'type': 'integer'}
        },
        'required': ['Name', 'Size']
    }
}

vms_info = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'VmId': parameter_types.len_constraint_string(36, 36),
            'Name': {'type': 'string'},
            'cHost': {'type': 'string'},
            'vCpus': {'type': 'integer'},
            'vRams': {'type': 'integer'},
            'vNics': vNics_array,
            'vDisks': vDisks_array
        },
        'required': ['VmId', 'Name', 'cHost', 'vCpus', 'vRams', 'vNics']
    }
}

src_type = {
    'type': 'string',
    'enum': ['vpim', 'vim']
}

msg_type = {
    'type': 'string',
    'enmu': ['vimCmRespool', 'vimCmVmChanges', 'vimCmHeartbeat']
}

vim_cm_push_info = {
    'type': 'object',
    'properties': {
        'Version': parameter_types.vim_pim_version,
        'VimId': parameter_types.len_constraint_string(36, 36),
        'SrcType': src_type,
        'MsgType':msg_type,
        'ResPool': res_pool_info,
        'AddVMs': vms_info,
        'UpdtVMs': vms_info,
        'DelVMs': {
            'type': 'array',
            'items': parameter_types.len_constraint_string(36, 36)
        }
    },
    'required': ['Version', 'VimId', 'SrcType', 'MsgType'],
    'additionalProperties': False
}

vim_cm_response = {
    'status_code': [200]
}

list_res_details_response = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'Version': parameter_types.vim_pim_version,
            'VimId': parameter_types.len_constraint_string(36, 36),
            'FileUri': parameter_types.gz_package_download_uri,
        }
    }
}

res_details = {
    'type': 'object',
    'properties': {
        'ResPool': res_pool_info,
        'AllVMs': vms_info
    }
}

