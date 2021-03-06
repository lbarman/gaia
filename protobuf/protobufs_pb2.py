# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: protobufs.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='protobufs.proto',
  package='gaia',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=_b('\n\x0fprotobufs.proto\x12\x04gaia\"\x9c\x02\n\x06\x43onfig\x12 \n\x18\x66\x65\x65\x64ing_module_activated\x18\x01 \x02(\x08\x12!\n\x19watering_module_activated\x18\x02 \x02(\x08\x12!\n\x19\x66\x65\x65\x64ing_module_cronstring\x18\x03 \x02(\t\x12\"\n\x1awatering_module_cronstring\x18\x04 \x02(\t\x12 \n\x18watering_pump_1_duration\x18\x05 \x02(\x05\x12 \n\x18watering_pump_2_duration\x18\x06 \x02(\x05\x12 \n\x18watering_pump_3_duration\x18\x07 \x02(\x05\x12 \n\x18watering_pump_4_duration\x18\x08 \x02(\x05\"U\n\x0cSystemStatus\x12\x0e\n\x06uptime\x18\x01 \x02(\t\x12\x0e\n\x06memory\x18\x02 \x02(\t\x12\x12\n\ndisk_usage\x18\x03 \x02(\t\x12\x11\n\tprocesses\x18\x04 \x02(\t\"\xe3\x01\n\x06Status\x12\x1c\n\x14\x61uthentication_token\x18\x01 \x02(\t\x12\x17\n\x0flocal_timestamp\x18\x02 \x02(\t\x12$\n\x0e\x63urrent_config\x18\x03 \x02(\x0b\x32\x0c.gaia.Config\x12)\n\rsystem_status\x18\x04 \x02(\x0b\x32\x12.gaia.SystemStatus\x12\x13\n\x0btemperature\x18\x05 \x02(\x05\x12\x10\n\x08humidity\x18\x06 \x02(\x05\x12\x14\n\x0ctemperature2\x18\x07 \x02(\x02\x12\x14\n\x0ctemperature3\x18\x08 \x02(\x02\"\xd4\x01\n\x0c\x41\x63tionReport\x12\x1c\n\x14\x61uthentication_token\x18\x01 \x02(\t\x12\x17\n\x0flocal_timestamp\x18\x02 \x02(\t\x12\x35\n\x06\x61\x63tion\x18\x03 \x02(\x0e\x32%.gaia.ActionReport.ActionReportAction\x12\x16\n\x0e\x61\x63tion_details\x18\x04 \x02(\t\">\n\x12\x41\x63tionReportAction\x12\r\n\tUNDEFINED\x10\x00\x12\x0b\n\x07\x46\x45\x45\x44ING\x10\x01\x12\x0c\n\x08WATERING\x10\x02\"\xb7\x01\n\x08Response\x12-\n\x06\x61\x63tion\x18\x01 \x02(\x0e\x32\x1d.gaia.Response.ResponseAction\x12\x1c\n\x06\x63onfig\x18\x02 \x01(\x0b\x32\x0c.gaia.Config\"^\n\x0eResponseAction\x12\x0e\n\nDO_NOTHING\x10\x00\x12\n\n\x06REBOOT\x10\x01\x12\x0c\n\x08SHUTDOWN\x10\x02\x12\x08\n\x04\x46\x45\x45\x44\x10\x03\x12\t\n\x05WATER\x10\x04\x12\r\n\tDELETE_DB\x10\x05\x32\x65\n\x0bGaiaService\x12$\n\x04Ping\x12\x0c.gaia.Status\x1a\x0e.gaia.Response\x12\x30\n\nActionDone\x12\x12.gaia.ActionReport\x1a\x0e.gaia.Response')
)



_ACTIONREPORT_ACTIONREPORTACTION = _descriptor.EnumDescriptor(
  name='ActionReportAction',
  full_name='gaia.ActionReport.ActionReportAction',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='UNDEFINED', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FEEDING', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WATERING', index=2, number=2,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=780,
  serialized_end=842,
)
_sym_db.RegisterEnumDescriptor(_ACTIONREPORT_ACTIONREPORTACTION)

_RESPONSE_RESPONSEACTION = _descriptor.EnumDescriptor(
  name='ResponseAction',
  full_name='gaia.Response.ResponseAction',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='DO_NOTHING', index=0, number=0,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='REBOOT', index=1, number=1,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='SHUTDOWN', index=2, number=2,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='FEED', index=3, number=3,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='WATER', index=4, number=4,
      serialized_options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='DELETE_DB', index=5, number=5,
      serialized_options=None,
      type=None),
  ],
  containing_type=None,
  serialized_options=None,
  serialized_start=934,
  serialized_end=1028,
)
_sym_db.RegisterEnumDescriptor(_RESPONSE_RESPONSEACTION)


_CONFIG = _descriptor.Descriptor(
  name='Config',
  full_name='gaia.Config',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='feeding_module_activated', full_name='gaia.Config.feeding_module_activated', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='watering_module_activated', full_name='gaia.Config.watering_module_activated', index=1,
      number=2, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='feeding_module_cronstring', full_name='gaia.Config.feeding_module_cronstring', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='watering_module_cronstring', full_name='gaia.Config.watering_module_cronstring', index=3,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='watering_pump_1_duration', full_name='gaia.Config.watering_pump_1_duration', index=4,
      number=5, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='watering_pump_2_duration', full_name='gaia.Config.watering_pump_2_duration', index=5,
      number=6, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='watering_pump_3_duration', full_name='gaia.Config.watering_pump_3_duration', index=6,
      number=7, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='watering_pump_4_duration', full_name='gaia.Config.watering_pump_4_duration', index=7,
      number=8, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=26,
  serialized_end=310,
)


_SYSTEMSTATUS = _descriptor.Descriptor(
  name='SystemStatus',
  full_name='gaia.SystemStatus',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='uptime', full_name='gaia.SystemStatus.uptime', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='memory', full_name='gaia.SystemStatus.memory', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='disk_usage', full_name='gaia.SystemStatus.disk_usage', index=2,
      number=3, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='processes', full_name='gaia.SystemStatus.processes', index=3,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=312,
  serialized_end=397,
)


_STATUS = _descriptor.Descriptor(
  name='Status',
  full_name='gaia.Status',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='authentication_token', full_name='gaia.Status.authentication_token', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='local_timestamp', full_name='gaia.Status.local_timestamp', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='current_config', full_name='gaia.Status.current_config', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='system_status', full_name='gaia.Status.system_status', index=3,
      number=4, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='temperature', full_name='gaia.Status.temperature', index=4,
      number=5, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='humidity', full_name='gaia.Status.humidity', index=5,
      number=6, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='temperature2', full_name='gaia.Status.temperature2', index=6,
      number=7, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='temperature3', full_name='gaia.Status.temperature3', index=7,
      number=8, type=2, cpp_type=6, label=2,
      has_default_value=False, default_value=float(0),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=400,
  serialized_end=627,
)


_ACTIONREPORT = _descriptor.Descriptor(
  name='ActionReport',
  full_name='gaia.ActionReport',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='authentication_token', full_name='gaia.ActionReport.authentication_token', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='local_timestamp', full_name='gaia.ActionReport.local_timestamp', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='action', full_name='gaia.ActionReport.action', index=2,
      number=3, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='action_details', full_name='gaia.ActionReport.action_details', index=3,
      number=4, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _ACTIONREPORT_ACTIONREPORTACTION,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=630,
  serialized_end=842,
)


_RESPONSE = _descriptor.Descriptor(
  name='Response',
  full_name='gaia.Response',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='action', full_name='gaia.Response.action', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='config', full_name='gaia.Response.config', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _RESPONSE_RESPONSEACTION,
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=845,
  serialized_end=1028,
)

_STATUS.fields_by_name['current_config'].message_type = _CONFIG
_STATUS.fields_by_name['system_status'].message_type = _SYSTEMSTATUS
_ACTIONREPORT.fields_by_name['action'].enum_type = _ACTIONREPORT_ACTIONREPORTACTION
_ACTIONREPORT_ACTIONREPORTACTION.containing_type = _ACTIONREPORT
_RESPONSE.fields_by_name['action'].enum_type = _RESPONSE_RESPONSEACTION
_RESPONSE.fields_by_name['config'].message_type = _CONFIG
_RESPONSE_RESPONSEACTION.containing_type = _RESPONSE
DESCRIPTOR.message_types_by_name['Config'] = _CONFIG
DESCRIPTOR.message_types_by_name['SystemStatus'] = _SYSTEMSTATUS
DESCRIPTOR.message_types_by_name['Status'] = _STATUS
DESCRIPTOR.message_types_by_name['ActionReport'] = _ACTIONREPORT
DESCRIPTOR.message_types_by_name['Response'] = _RESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Config = _reflection.GeneratedProtocolMessageType('Config', (_message.Message,), dict(
  DESCRIPTOR = _CONFIG,
  __module__ = 'protobufs_pb2'
  # @@protoc_insertion_point(class_scope:gaia.Config)
  ))
_sym_db.RegisterMessage(Config)

SystemStatus = _reflection.GeneratedProtocolMessageType('SystemStatus', (_message.Message,), dict(
  DESCRIPTOR = _SYSTEMSTATUS,
  __module__ = 'protobufs_pb2'
  # @@protoc_insertion_point(class_scope:gaia.SystemStatus)
  ))
_sym_db.RegisterMessage(SystemStatus)

Status = _reflection.GeneratedProtocolMessageType('Status', (_message.Message,), dict(
  DESCRIPTOR = _STATUS,
  __module__ = 'protobufs_pb2'
  # @@protoc_insertion_point(class_scope:gaia.Status)
  ))
_sym_db.RegisterMessage(Status)

ActionReport = _reflection.GeneratedProtocolMessageType('ActionReport', (_message.Message,), dict(
  DESCRIPTOR = _ACTIONREPORT,
  __module__ = 'protobufs_pb2'
  # @@protoc_insertion_point(class_scope:gaia.ActionReport)
  ))
_sym_db.RegisterMessage(ActionReport)

Response = _reflection.GeneratedProtocolMessageType('Response', (_message.Message,), dict(
  DESCRIPTOR = _RESPONSE,
  __module__ = 'protobufs_pb2'
  # @@protoc_insertion_point(class_scope:gaia.Response)
  ))
_sym_db.RegisterMessage(Response)



_GAIASERVICE = _descriptor.ServiceDescriptor(
  name='GaiaService',
  full_name='gaia.GaiaService',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  serialized_start=1030,
  serialized_end=1131,
  methods=[
  _descriptor.MethodDescriptor(
    name='Ping',
    full_name='gaia.GaiaService.Ping',
    index=0,
    containing_service=None,
    input_type=_STATUS,
    output_type=_RESPONSE,
    serialized_options=None,
  ),
  _descriptor.MethodDescriptor(
    name='ActionDone',
    full_name='gaia.GaiaService.ActionDone',
    index=1,
    containing_service=None,
    input_type=_ACTIONREPORT,
    output_type=_RESPONSE,
    serialized_options=None,
  ),
])
_sym_db.RegisterServiceDescriptor(_GAIASERVICE)

DESCRIPTOR.services_by_name['GaiaService'] = _GAIASERVICE

# @@protoc_insertion_point(module_scope)
