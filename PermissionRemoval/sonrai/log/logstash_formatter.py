import datetime
import traceback

from logstash_formatter import LogstashFormatter as _LogstashFormatter


class LogstashFormatter(_LogstashFormatter):
    def __init__(self, *args, custom_fields=None, **kwargs):
        self.custom_fields = custom_fields if custom_fields is not None else {}
        # noinspection PyTypeChecker
        super().__init__(
            *args,
            fmt=(
                'asctime', # timestamp
                'levelname', # ERROR/WARN/etc
                'pathname', # Full path to file
                'lineno', # Line within the file
                'funcName', # Name of function
                'message', # Formatted message (un-formatted uses 'msg')
                'exc_info', # Stack trace, see format method
                'name', # Name of the logger
                'threadName', # Name of the thread
            ),
#            rename={
#                # These are renamed to maintain consistency with our Java containers
#                # The bootstrap could rename these upon ingestion, but this doing it here is sufficient
#                'asctime': '@timestamp',
#                'levelname': 'level',
#                'funcName': 'func',
#                'name': 'logger_name',
#                'threadName': 'thread_name'
#            },
#           validate=False,
#           **kwargs
        )

    def format(self, record):
        exc_info = getattr(record, 'exc_info', None)
        if exc_info:
            delattr(record, 'exc_info')
            #: Formats the traceback with and places it in the stack_trace field
            #: This mirrors the Java containers
            record.stack_trace = "".join(traceback.format_exception(*exc_info))
        if self.custom_fields:
            for k in self.custom_fields:
                setattr(record, k, self.custom_fields[k])
        return super().format(record)

    # Since we always use UTC, the offset is hardcoded here to mirror the Java containers
    # If %z is used, then the timestamp is formatted as '+0000', not '+00:00' as per RFC3339
    # Another formatter could be supported in the bootstrap, but that would waste cycles
    default_time_format = '%Y-%m-%dT%H:%M:%S.%f+00:00'

    @staticmethod
    def converter(t):
        return datetime.datetime.fromtimestamp(t, tz=datetime.timezone.utc)
