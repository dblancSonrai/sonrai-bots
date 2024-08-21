import re

class ParsedResourceId:
  _PATTERN = re.compile('/subscriptions/([^/]*)/resourcegroups/([^/]*)/providers/([^/]*)/([^/]*)/([^/]*)', re.IGNORECASE)

  def __init__(self, resource_id):
    m = self._PATTERN.search(resource_id)
    if not m:
      raise ValueError("Invalid resource_id: {}".format(resource_id))
    self._value = resource_id
    self.subscription = m.group(1)
    self.resource_group = m.group(2)
    self.provider = m.group(3)
    self.type = m.group(4)
    self.name = m.group(5)

  def assert_subscription(self, subscription):
    if self.subscription != subscription:
      raise ValueError("[{}] Subscription \"{}\" does not match expected: \"{}\"".format(self, self.subscription, subscription))
    return self

  def assert_resource_group(self, resource_group):
    if self.resource_group != resource_group:
      raise ValueError("[{}] Resource Group \"{}\" does not match expected: \"{}\"".format(self, self.resource_group, resource_group))
    return self

  def assert_provider(self, provider):
    if self.provider.lower() != provider.lower():
      raise ValueError("[{}] Provider \"{}\" does not match expected: \"{}\"".format(self, self.provider.lower(), provider.lower()))
    return self

  def assert_type(self, t):
    if self.type.lower() != t.lower():
      raise ValueError("[{}] Type \"{}\" does not match expected: \"{}\"".format(self, self.type.lower(), t.lower()))
    return self

  def assert_name(self, name):
    if self.name != name:
      raise ValueError("[{}] Name \"{}\" does not match expected: \"{}\"".format(self, self.name, name))
    return self

  def __str__(self):
    return self._value