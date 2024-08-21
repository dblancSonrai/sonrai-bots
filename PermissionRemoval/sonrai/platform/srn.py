
def parse(srn_str):
    return Srn.parse(srn_str)

class Srn:
    #: srn:<cloud>:<service>:[<region>]:[<accountSubType>|]<accountIdentifier>/<label>[/<type>]/<identifier>
    @staticmethod
    def parse(srn_str):
        parts = srn_str.split(':', 5)
        if len(parts) < 5:
            raise ValueError("Invalid SRN: {}".format(srn_str))
        partition, cloud, service, region, remainder = parts
        if partition != 'srn':
            raise ValueError("Invalid SRN: {}".format(srn_str))
        parts = remainder.split('/', 2)
        if len(parts) < 3:
            raise ValueError("Invalid SRN: {}".format(srn_str))
        account, label, unique_name = parts
        return Srn(cloud, service, region, account, label, unique_name)

    def __init__(self, cloud, service, region, account, label, unique_name):
        self.cloud = cloud or ''
        self.service = service or ''
        self.region = region or ''
        self.account = account or ''
        self.label = label or ''
        self.type = type or ''
        self.unique_name = unique_name or ''
        try:
            i = self.unique_name.index('/')
            self.type = self.unique_name[:i]
            self.resource = self.unique_name[i+1:]
        except ValueError:
            self.type = ''
            self.resource = self.unique_name

    def _build_str(self):
        srn_str = ':'.join(('srn', self.cloud, self.service, self.region, self.account))
        return srn_str + "/".join(("", self.label, self.unique_name))

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self._build_str()
