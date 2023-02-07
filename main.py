#!/usr/bin/env python
from constructs import Construct
from cdk8s import App, Chart
from imports import k8s
from webservice import WebService


class MyChart(Chart):
    def __init__(self, scope: Construct, id: str, namespace: str):
        super().__init__(scope, id, namespace=namespace)
        WebService(self, 'guestbook-ui', image='gcr.io/heptio-images/ks-guestbook-demo:0.2')


app = App()
namespace_chart = Chart(app, "namespace")
k8s.KubeNamespace(
    namespace_chart, "namespace",
    metadata=k8s.ObjectMeta(name="guestbook")
)
app_chart = MyChart(app, "cdk8-example", "guestbook")
app_chart.add_dependency(namespace_chart)
app.synth()