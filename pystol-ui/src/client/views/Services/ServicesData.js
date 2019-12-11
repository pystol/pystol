/*k8s javascript client require*/
//const k8s = require('@kubernetes/client-node');

/*
import * as k8s from '@kubernetes/client-node';

var servicesData = {};

try {
  const kc = new k8s.KubeConfig();
  kc.loadFromDefault();

  // Core_v1Api docs: https://github.com/kubernetes-client/java/blob/master/kubernetes/docs/CoreV1Api.md //
  // core_v1api -- pods, services (may include nodeport, loadbalancer)
  // optional: serviceaccount, resourcequota, replication controller if needed
  const k8sApi = kc.makeApiClient(k8s.Core_v1Api);
  // Extensions_v1beta1Api docs: https://github.com/kubernetes-client/java/blob/master/kubernetes/docs/ExtensionsV1beta1Api.md //
  // extensions_v1beta1api -- ingress, deployment
  // optional: daemonset, and network policy as well as replica set if needed
  const k8sApi2 = kc.makeApiClient(k8s.Extensions_v1beta1Api);

  k8sApi.listNamespacedService('')
    .then((re) => {
      servicesData = re.body;
    })
    .catch((err) => {
      console.log(err);
      servicesData = require('./servicesData.json');
    })

} catch(e) {
  console.log(e.message);
} finally {
  servicesData = require('./servicesData.json');
}

*/


const servicesData = require('./servicesData.json');
export default servicesData
/*End K8s*/
