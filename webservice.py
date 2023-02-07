#!/usr/bin/env python
from constructs import Construct, Node
from cdk8s import Names
from imports import k8s


class WebService(Construct):
    def __init__(
            self, scope: Construct, id: str, *,
            image: str,
            replicas: int = 1,
            revision_history_limit: int = 3,
            port: int = 80,
            container_port: int = 80,
    ):
        super().__init__(scope, id)
        label = {"app": "hello-k8s"}
        # define resources here        label = {"app": Names.to_dns_label(self)}
        k8s.KubeDeployment(self, 'deployment',
                           spec=k8s.DeploymentSpec(
                               replicas=replicas,
                               revision_history_limit=revision_history_limit,
                               selector=k8s.LabelSelector(match_labels=label),
                               template=k8s.PodTemplateSpec(
                                   metadata=k8s.ObjectMeta(labels=label),
                                   spec=k8s.PodSpec(containers=[
                                       k8s.Container(
                                           name='guestbook-ui',
                                           image=image,
                                           ports=[k8s.ContainerPort(container_port=container_port)])]))))
        k8s.KubeService(self, 'service',
                        spec=k8s.ServiceSpec(
                            type='ClusterIP',
                            ports=[k8s.ServicePort(port=port, target_port=k8s.IntOrString.from_number(container_port))],
                            selector=label))