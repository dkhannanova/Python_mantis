from sys import maxsize
class Project:
    def __init__(self, id=None, name=None, state=None, enabled=True,
                 visibility=None, description=None):
        self.id = id
        self.name = name
        self.state = state
        self.enabled = enabled
        self.visibility = visibility
        self.description = description



    def __repr__(self):
        return "%s:%s:%s" % (self.id, self.name, self.description)

    def __eq__(self, other):
        return (self.id is None or other.id is None or self.id == other.id) and self.name == other.name


    def prid_or_max(self):
        if self.id:
            return int(self.id)
        else:
            return maxsize



