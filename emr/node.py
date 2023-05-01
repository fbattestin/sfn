class EmrNode:
    """
    Representa um nó EMR com informações relevantes e histórico de execução de steps e scripts shell.
    """
    def __init__(
            self,
            node_type,
            node_id,
            ec2_instance_id,
            instance_type,
            state,
            creation_date,
            group_id,
            market,
            public_dns,
            private_dns
    ):
        self.node_type = node_type
        self.node_id = node_id
        self.ec2_instance_id = ec2_instance_id
        self.instance_type = instance_type
        self._state = state
        self.creation_date = creation_date
        self._end_date = None
        self.group_id = group_id
        self.market = market
        self.public_dns = public_dns
        self.private_dns = private_dns
        self.execution_history = []

    def is_property(self, obj, attr_name):
        attr = getattr(obj.__class__, attr_name, None)
        return isinstance(attr, property)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        self._end_date = value

    def add_script(self, execution: EmrExecution):
        self.execution_history.append(execution)

    def update_script(self, script_id, attr_name, attr_value):
        for execution in self.execution_history:
            if execution.is_completed and execution.script_id == script_id:
                if self.is_property(execution, attr_name):
                    execution.attr_name = attr_value

    def __str__(self):
        return f"EMR Node ID: {self.node_id}, Instance Type: {self.instance_type}, State: {self.state}, Group Name: {self.group_name}, Public DNS: {self.public_dns}, Private DNS: {self.private_dns}, Steps History: {self.steps_history}, Shell Scripts History: {self.shell_scripts_history}"
