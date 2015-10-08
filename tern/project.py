class ProjectFile(object):
  def __init__(self, name, view, project):
    self.project = project
    self.name = name
    self.dirty = view.is_dirty()
    self.cached_completions = None
    self.cached_arguments = None
    self.showing_arguments = False
    self.last_modified = 0

class Project(object):
  def __init__(self, dir):
    self.dir = dir
    self.port = None
    self.proc = None
    self.last_failed = 0
    self.disabled = False

