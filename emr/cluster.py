import boto3


class EMRCluster:
    def __init__(
            self,
            cluster_id: str,
            cluster_name: str,
            state: str,
            parallelism: str,
            created_at: str,
            applications: list,
            instance_type: str,
            instance_count: int,
            ec2_instance_ids: list
    ):
        self.cluster_id = cluster_id
        self.cluster_name = cluster_name
        self.state = state
        self.parallelism = parallelism
        self._is_active = None
        self.created_at = created_at
        self.applications = applications
        self.instance_type = instance_type
        self.instance_count = instance_count
        self.ec2_instance_ids = ec2_instance_ids
        self._ended_at = None
        self.total_instances_running = None
        self.active_ec2_instance_ids = []
        self.ec2_instance_ids_history = []

    def __str__(self) -> str:
        return (
            f"EMR Cluster: {self.cluster_name}\n"
            f"ID: {self.cluster_id}\n"
            f"State: {self.state}\n"
            f"Created at: {self.created_at}\n"
            f"Applications: {', '.join(self.applications)}\n"
            f"Instance type: {self.instance_type}\n"
            f"Instance count: {self.instance_count}\n"
            f"EC2 instance IDs: {', '.join(self.ec2_instance_ids)}"
        )

    @property
    def ended_at(self):
        return self._ended_at

    @ended_at.setter
    def ended_at(self, value):
        self._ended_at = value

    @property
    def is_active(self):
        '''
        AWAITING_FULFILLMENT (False): A instância está aguardando recursos para ser provisionada.
        PROVISIONING (False): A instância está sendo provisionada.
        BOOTSTRAPPING (True): A instância está sendo inicializada.
        RUNNING (True): A instância está em execução e pronta para uso.
        TERMINATED (False): A instância foi encerrada.
        TERMINATING (False): A instância está sendo encerrada.
        FAILED (False): A instância falhou e não está mais disponível.
        TERMINATED_WITH_ERRORS (False): A instância foi encerrada com erros.
        '''

        active_states = ["STARTING", "BOOTSTRAPPING", "RUNNING", "WAITING"]

        if self.state in active_states:
            self._is_active = True
            return self._is_active
        else:
            self._is_active = False
            return self._is_active

    def update_cluster_state(self):
        emr_client = boto3.client("emr")
        response = emr_client.describe_cluster(ClusterId=self.cluster_id)
        self.state = response["Cluster"]["Status"]["State"]

    def update_total_instances_running(self):
        emr_client = boto3.client("emr")
        response = emr_client.list_instances(ClusterId=self.cluster_id)

        active_instance_ids = [
            instance["Ec2InstanceId"] for instance in response["Instances"] if
            instance["Status"]["State"] in ["RUNNING", "BOOTSTRAPPING"]
        ]

        self.total_instances_running = len(active_instance_ids)

    def update_active_ec2_instance_ids(self):
        emr_client = boto3.client("emr")
        response = emr_client.list_instances(ClusterId=self.cluster_id)

        updated_active_instance_ids = [
            instance["Ec2InstanceId"] for instance in response["Instances"] if
            instance["Status"]["State"] in ["RUNNING", "BOOTSTRAPPING"]
        ]

        for instance_id in self.active_ec2_instance_ids:
            if instance_id not in updated_active_instance_ids:
                self.ec2_instance_ids_history.append(instance_id)

        self.active_ec2_instance_ids = updated_active_instance_ids