#! /usr/bin/python
# coding:utf-8
from faked_nfvo.api.validation import parameter_types

list_res_details = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'Version': {'type': 'string'},
            'VimId': {'type': 'string'},
            'Chassis': {
                'type': 'object',
                'properties': {
                    'URL': {'type': 'string'}
                },
                'required': ['URL']
            },
            'Systems': {
                'type': 'object',
                'properties': {
                    'URL': {'type': 'string'}
                },
                'required': ['URL']
            },
            'Switches': {
                'type': 'object',
                'properties': {
                    'URL': {'type': 'string'}
                },
                'required': ['URL']
            },
            'Firewalls': {
                'type': 'object',
                'properties': {
                    'URL': {'type': 'string'}
                },
                'required': ['URL']
            },
            'DiskArrayChassis': {
                'type': 'object',
                'properties': {
                    'URL': {'type': 'string'}
                },
                'required': ['URL']
            },
            'DiskArraySystems': {
                'type': 'object',
                'properties': {
                    'URL': {'type': 'string'}
                },
                'required': ['URL']
            },
            'StorageServices': {
                'type': 'object',
                'properties': {
                    'URL': {'type': 'string'}
                },
                'required': ['URL']
            }
        },
        'required': ['Version', 'VimId', 'Chassis', 'Systems', 'Switches',
                     'Firewalls', 'DiskArrayChassis', 'DiskArraySystems',
                     'StorageServices']
    }

}

list_chassis_list = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'Version': {'type': 'string'},
            'VimId': {'type': 'string'},
            'MembersCount': {'type': 'integer'},
            'Members': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'URL': {'type': 'string'}
                    },
                    'required': ['URL']

                }
            }

        },
        'required': ['Version', 'VimId', 'MembersCount', 'Members']
    }
}

list_chassis_details = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'Version': {'type': 'string'},
            'VimId': {'type': 'string'},
            'Id': {'type': 'string'},
            'Name': {'type': 'string'},
            'ChassisType': {'type': 'string'},
            'AssetTag': {'type': 'string'},
            'Manufacturer': {'type': 'string'},
            'Model': {'type': 'string'},
            'SerialNumber': {'type': 'string'},
            'Thermal': {
                'type': 'object',
                'properties': {
                    'Id': {'type': 'string'},
                    'FansCount': {'type': 'integer'},
                    'Fans': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'MemberId': {'type': 'string'},
                                'RpmPercentage': {'type': 'integer'},
                                'Slot': {'type': 'integer'},
                                'Status': {'type': 'object'}
                            },
                            'required': ['MemberId', 'RpmPercentage', 'Slot',
                                         'Status']
                        }
                    },
                    'Temperatures': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'MemberId': {'type': 'string'},
                                'SensorDeviceType': {'type': 'string'},
                                'ReadingCelsius': {'type': 'integer'}
                            },
                            'required': ['MemberId', 'SensorDeviceType',
                                         'ReadingCelsius']
                        }
                    }
                },
                'required': ['Id', 'FansCount', 'Fans', 'Temperatures']
            },
            'Power': {
                'type': 'object',
                'properties': {
                    'Id': {'type': 'string'},
                    'PowerSuppliesCount': {'type': 'integer'},
                    'PowerSupplies': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'MemberId': {'type': 'string'},
                                'Model': {'type': 'string'},
                                'Slot': {'type': 'integer'},
                                'Status': {'type': 'object'},
                                'PowerCapacityWatts': {'type': 'integer'},
                                'PowerConsumedWatts': {'type': 'integer'}
                            },
                            'required': ['MemberId', 'Model', 'Slot', 'Status',
                                         'PowerCapacityWatts',
                                         'PowerConsumedWatts']

                        }
                    }
                },
                'required': ['Id', 'PowerSuppliesCount', 'PowerSupplies']
            },
            'Managers': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'Id': {'type': 'string'},
                        'IPv4address': {'type': 'string'},
                        'FirmwareVersion': {'type': 'string'}
                    },
                    'required': ['Id', 'IPv4address', 'FirmwareVersion']

                }
            },
            'PropertySource': {'type': 'string'},
            'PutIntoProductionTime': {'type': 'string'},
            'PropertyState': {'type': 'string'},
            'Location': {
                'type': 'object',
                'properties': {
                    'Info': {'type': 'string'}
                },
                'required': ['Info']
            },
            'Status': {'type': 'object'},
            'Links': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'ComputerSystems': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'URL': {'type': 'string'}
                                },
                                'required': ['URL']

                            }
                        }
                    },
                    'required': ['ComputerSystems']

                }
            }
        },
        'require': ['Version', 'VimId', 'Id', 'Name', 'ChassisType', 'AssetTag',
                    'Manufacturer', 'Model', 'SerialNumber', 'Thermal', 'Power',
                    'Managers', 'PropertySource', 'PutIntoProductionTime',
                    'PropertyState', 'Location', 'Status', 'Links']
    }
}

list_system_list = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'Version': {'type': 'string'},
            'VimId': {'type': 'string'},
            'MembersCount': {'type': 'integer'},
            'Members': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'URL': {'type': 'integer'}
                    },
                    'required': ['URL']

                }
            }
        }
    },
    'required': ['Version', 'VimId', 'MembersCount', 'Members']
}

list_system_details = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'Version': {'type': 'string'},
            'VimId': {'type': 'string'},
            'Id': {'type': 'string'},
            'Processors': {
                'type': 'object',
                'properties': {
                    'MembersCount': {'type': 'integer'},
                    'Members': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'Id': {'type': 'string'},
                                'Manufacturer': {'type': 'string'},
                                'Model': {'type': 'string'},
                                'TotalCores': {'type': 'integer'},
                                'MaxSpeedMHz': {'type': 'integer'},
                                'Slot': {'type': 'integer'},
                                'Status': {'type': 'object'}
                            },
                            'required': ['Id', 'Manufacturer', 'Model',
                                         'TotalCores', 'MaxSpeedMHz', 'Slot',
                                         'Status']

                        }
                    }
                },
                'required': ['MembersCount', 'Members']
            },
            'ProcessorSummary': {
                'type': 'object',
                'properties': {
                    'Count': {'type': 'object'}
                },
                'required': ['Count']
            },
            'Storages': {
                'type': 'object',
                'properties': {
                    'MembersCount': {'type': 'integer'},
                    'Members': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'Id': {'type': 'string'},
                                'StorageControllers': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'object',
                                        'properties': {
                                            'MemberId': {'type': 'string'},
                                            'FirmwareVersion': {
                                                'type': 'string'},
                                            'Model': {'type': 'string'},
                                            'Status': {'type': 'object'}
                                        },
                                        'required': ['MemberId',
                                                     'FirmwareVersion', 'Model',
                                                     'Status']

                                    }
                                },
                                'Drives': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'object',
                                        'properties': {
                                            'Id': {'type': 'string'},
                                            'Model': {'type': 'string'},
                                            'Manufacturer': {'type': 'string'},
                                            'MediaType': {'type': 'string'},
                                            'CapacityBytes': {
                                                'type': 'integer'},
                                            'Slot': {'type': 'integer'},
                                            'Status': {'type': 'object'}
                                        },
                                        'required': ['Id', 'Model',
                                                     'Manufacturer',
                                                     'MediaType',
                                                     'CapacityBytes', 'Slot',
                                                     'Status']

                                    }
                                },
                                'LogicalDrives': {
                                    'type': 'array',
                                    'items': {
                                        'type': 'object',
                                        'properties': {
                                            'Id': {'type': 'string'},
                                            'Status': {'type': 'object'}
                                        },
                                        'required': ['Id', 'Status']

                                    }
                                }
                            },
                            'required': ['Id', 'StorageControllers', 'Drives',
                                         'LogicalDrives']

                        }
                    }
                },
                'required': ['MembersCount', 'Members']
            },
            'MemorySummary': {
                'type': 'object',
                'properties': {
                    'TotalSystemMemoryGiB': {'type': 'integer'}
                }
            },
            'Memorys': {
                'type': 'object',
                'properties': {
                    'MembersCount': {'type': 'integer'},
                    'Members': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'Id': {'type': 'string'},
                                'Model': {'type': 'string'},
                                'MemoryDeviceType': {'type': 'string'},
                                'CapacityMiB': {'type': 'integer'},
                                'Slot': {'type': 'integer'},
                                'Status': {'type': 'object'}
                            },
                            'required': ['Id', 'Model', 'MemoryDeviceType',
                                         'CapacityMiB', 'Slot', 'Status']

                        }
                    }
                },
                'required': ['MembersCount', 'Members']
            },
            'EthernetInterfaces': {
                'type': 'object',
                'properties': {
                    'MembersCount': {'type': 'integer'},
                    'Members': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'Id': {'type': 'string'},
                                'Model': {'type': 'string'},
                                'EthernetInterfaceType': {'type': 'string'},
                                'IPv4Address': {'type': 'array'},
                                'IPv6Address': {'type': 'array'},
                                'MacAddress': {'type': 'string'},
                                'HostNicName': {'type': 'string'},
                                'FirmwareVersion': {'type': 'string'},
                                'EthernetPorts': {'type': 'string'},
                                'Slot': {'type': 'integer'},
                                'Status': {'type': 'object'}
                            },
                            'required': ['Id', 'Model', 'EthernetInterfaceType',
                                         'MacAddress', 'HostNicName',
                                         'FirmwareVersion', 'EthernetPorts',
                                         'Slot', 'Status']

                        }
                    }
                },
                'required': ['MembersCount', 'Members']
            },
            'MotherBoard': {
                'type': 'object',
                'properties': {
                    'SKU': {'type': 'string'},
                    'SerialNumber': {'type': 'string'}
                },
                'required': ['SKU', 'SerialNumber']
            },
            'Status': {'type': 'object'},
            'BiosVersion': {'type': 'string'},
            'ApplicationType': {'type': 'string'},
            'Links': {
                'type': 'object',
                'properties': {
                    'Chassis': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'URL': {'type': 'string'}
                            },
                            'required': ['URL']
                        }

                    }
                },
                'required': ['Chassis']

            }

        },
        'required': ['Version', 'VimId', 'Id', 'Processors', 'ProcessorSummary',
                     'Storages', 'MemorySummary', 'Memorys',
                     'EthernetInterfaces', 'MotherBoard', 'Status',
                     'BiosVersion', 'ApplicationType', 'Links']
    }
}

list_disk_array_chassis_list = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'Version': {'type': 'string'},
            'VimId': {'type': 'string'},
            'MembersCount': {'type': 'integer'},
            'Members': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'URL': {'type': 'string'}
                    },
                    'required': ['URL']

                }
            }
        },
        'required': ['Version', 'VimId', 'MembersCount', 'Members']
    }
}

list_disk_array_chassis_details = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'Version': {'type': 'string'},
            'VimId': {'type': 'string'},
            'Id': {'type': 'string'},
            'Name': {'type': 'string'},
            'ChassisType': {'type': 'string'},
            'AssetTag': {'type': 'string'},
            'Manufacturer': {'type': 'string'},
            'Model': {'type': 'string'},
            'SerialNumber': {'type': 'string'},
            'Thermal': {
                'type': 'object',
                'properties': {
                    'Id': {'type': 'string'},
                    'FansCount': {'type': 'integer'},
                    'Fans': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'MemberId': {'type': 'string'},
                                'Slot': {'type': 'integer'},
                                'Status': {'type': 'object'}
                            },
                            'required': ['MemberId', 'Slot', 'Status']

                        }
                    },
                    'Temperatures': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'MemberId': {'type': 'string'},
                                'SensorDeviceType': {'type': 'string'},
                                'ReadingCelsius': {'type': 'integer'}
                            },
                            'required': ['MemberId', 'SensorDeviceType',
                                         'ReadingCelsius']
                        }
                    }
                },
                'required': ['Id', 'FansCount', 'Fans', 'Temperatures']
            },
            'Power': {
                'type': 'object',
                'properties': {
                    'Id': {'type': 'string'},
                    'PowerSuppliesCount': {'type': 'integer'},
                    'PowerSupplies': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'MemberId': {'type': 'string'},
                                'Slot': {'type': 'integer'},
                                'Status': {'type': 'object'}
                            },
                            'required': ['MemberId', 'Slot', 'Status']

                        }
                    }
                },
                'required': ['Id', 'PowerSuppliesCount', 'PowerSupplies']
            },
            'BBUs': {
                'type': 'object',
                'properties': {
                    'BBU': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'Id': {'type': 'string'},
                                'Slot': {'type': 'integer'},
                                'Status': {'type': 'object'}
                            },
                            'required': ['Id', 'Slot', 'Status']
                        }
                    },
                    'BBUsCount': {'type': 'integer'}
                },
                'required': ['BBU', 'BBUsCount']
            },
            'PropertySource': {'type': 'string'},
            'PutIntoProductionTime': {'type': 'string'},
            'License': {'type': 'string'},
            'SoftwareVersion': {'type': 'string'},
            'OperationingStatus': {'type': 'string'},
            'PropertyState': {'type': 'string'},
            'Location': {
                'type': 'object',
                'properties': {
                    'Info': {'type': 'string'}
                },
                'required': ['Info']
            },
            'Status': {'type': 'object'},
            'Links': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'DiskArraySystem': {
                            'type': 'object',
                            'properties': {
                                'URL': {'type': 'string'}
                            }
                        },
                        'Storages': {
                            'type': 'array',
                            'items': {
                                'type': 'object',
                                'properties': {
                                    'URL': {'type': 'string'}
                                }
                            }
                        }
                    },
                    'required': ['DiskArraySystem', 'Storages']
                }
            }
        },
        'required': ['Version', 'VimId', 'Id', 'Name', 'ChassisType',
                     'AssetTag', 'Manufacturer', 'Model', 'SerialNumber',
                     'Thermal', 'Power', 'BBUs', 'PropertySource',
                     'PutIntoProductionTime',
                     'SoftwareVersion', 'OperationingStatus', 'PropertyState',
                     'Location', 'Status', 'Links']

    }
}

list_disk_array_system_list = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'Version': {'type': 'string'},
            'VimId': {'type': 'string'},
            'MembersCount': {'type': 'integer'},
            'Members': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'URL': {'type': 'string'}
                    },
                    'required': ['URL']
                }
            }
        },
        'required': ['Version', 'VimId', 'MembersCount', 'Members']
    }
}

list_disk_array_system_details = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'Version': {'type': 'string'},
            'VimId': {'type': 'string'},
            'Id': {'type': 'string'},
            'Processors': {
                'type': 'object',
                'properties': {
                    'MembersCount': {'type': 'integer'},
                    'Members': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'Id': {'type': 'string'},
                                'Status': {'type': 'object'}
                            },
                            'required': ['Id', 'Status']
                        }
                    }
                },
                'required': ['MembersCount', 'Members']
            },
            'EthernetInterfaces': {
                'type': 'object',
                'properties': {
                    'MembersCount': {'type': 'integer'},
                    'Members': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'Id': {'type': 'string'},
                                'IPv4Address': {'type': 'string'},
                                'IPv6Address': {'type': 'string'},
                                'MacAddress': {'type': 'string'},
                                'Status': {'type': 'object'}
                            },
                            'required': ['Id', 'IPv4Address', 'IPv6Address',
                                         'MacAddress', 'Status']
                        }
                    }
                },
                'required': ['MembersCount', 'Members']
            },
            'ChacheGB': {'type': 'integer'},
            'Links': {
                'type': 'object',
                'properties': {
                    'Chassis': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'URL': {'type': 'string'}
                            }
                        }
                    },
                    'Storages': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'URL': {'type': 'string'}
                            }
                        }
                    }
                },
                'required': ['Chassis', 'Storages']
            }

        },
        'required': ['Version', 'VimId', 'Id', 'EthernetInterfaces', 'ChacheGB',
                     'Links']
    }
}

list_history_metrics = {
    'status_code': [200],
    'response_body': {
        'type': 'object',
        'properties': {
            'Version': {'type': 'string'},
            'VimId': {'type': 'string'},
            'SrcType': {'type': 'string'},
            'MsgType': {'type': 'string'},
            'FileUris': {'type': 'array'}
        },
        'required': ['Version', 'VimId', 'SrcType', 'MsgType', 'FileUris']
    }
}

src_type = {
    'type': 'string',
    'enum': ['vpim', 'pim']
}

msg_type_cm = {
    'type': 'string',
    'enum': ['pimCmHeartbeat', 'pimCmResChanges']
}

res_type = {
    'type': 'object',
    'properties':{
        'Chassis': {'type': 'array'},
        'ComputerSystems': {'type': 'array'},
        'DiskArrayChassis': {'type': 'array'},
        'DiskArraySystems': {'type': 'array'},
        'Storages': {'type': 'array'},
        'Switches': {'type': 'array'},
    }
}

push_cm_info = {
    'type': 'object',
    'properties': {
        'Version': parameter_types.vim_pim_version,
        'VimId': parameter_types.len_constraint_string(36, 36),
        'SrcType': src_type,
        'MsgType': msg_type_cm,
        'AddRes': res_type,
        'UpdtRes': res_type,
        'DelRes': res_type
    },
    'required': ['Version', 'VimId', 'SrcType', 'MsgType'],
    'additionalProperties': False
}