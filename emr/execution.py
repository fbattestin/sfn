class EmrExecution:
    def __init__(self, script_id, script_name, script_status=None, script_start=None, is_completed=False):
        self.script_id = script_id
        self.script_name = script_name
        self.script_status = script_status
        self.script_start = script_start
        self.script_end = None
        self.is_completed = is_completed

    @property
    def script_status(self):
        return self._script_status

    @script_status.setter
    def script_status(self, value):
        self._script_status = value

    @property
    def script_start(self):
        return self._script_start

    @script_start.setter
    def script_start(self, value):
        self._script_start = value

    @property
    def script_end(self):
        return self._script_end

    @script_end.setter
    def script_end(self, value):
        self._script_end = value

    @property
    def is_completed(self):
        return self._is_completed

    @is_completed.setter
    def is_completed(self, value):
        self._is_completed = value