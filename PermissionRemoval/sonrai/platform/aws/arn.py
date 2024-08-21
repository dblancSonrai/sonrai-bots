from arnparse.arnparse import arnparse
from arnparse.arnparse import Arn as _Arn

def parse(arn_str):
    arn = arnparse(arn_str)
    arn._arn_str = arn_str
    arn.name = arn.resource.rsplit('/', maxsplit=2)[-1]
    return arn

# Assign Arn.assert_service
def _assert_service(self, service):
    if self.service != service:
        raise ValueError("[{}] Service \"{}\" does not match expected: \"{}\"".format(self, self.service, service))
    return self
setattr(_Arn, 'assert_service', _assert_service)
# Assign Arn.assert_resource_type
def _assert_resource_type(self, resource_type):
    if self.resource_type != resource_type:
        raise ValueError("[{}] Resource Type \"{}\" does not match expected: \"{}\"".format(self, self.resource_type, resource_type))
    return self
setattr(_Arn, 'assert_resource_type', _assert_resource_type)
setattr(_Arn, 'assert_type', _assert_resource_type) # Backwards compatibility
# Assign Arn.__str__
setattr(_Arn, '__str__', lambda self: self._arn_str if hasattr(self, '_arn_str') else super(_Arn, self).__str__())