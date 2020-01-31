var express = require('express');
var router = express.Router();

// k8s javascript client require
const k8s = require('@kubernetes/client-node');
const kc = new k8s.KubeConfig();
kc.loadFromDefault();

/* Core_v1Api docs: https://github.com/kubernetes-client/java/blob/master/kubernetes/docs/CoreV1Api.md */
// core_v1api -- pods, services (may include nodeport, loadbalancer)
// optional: serviceaccount, resourcequota, replication controller if needed
const k8sApi = kc.makeApiClient(k8s.CoreV1Api);

/* Extensions_v1beta1Api docs: https://github.com/kubernetes-client/java/blob/master/kubernetes/docs/ExtensionsV1beta1Api.md */
// extensions_v1beta1api -- ingress, deployment
// optional: daemonset, and network policy as well as replica set if needed
const k8sApi2 = kc.makeApiClient(k8s.ExtensionsV1beta1Api);

/*
Endpoint: /api/
*/
router.get('/', function(req, res, next) {
	res.json([
                  Math.random().toString(36).substring(7),
                  Math.random().toString(36).substring(7),
                  Math.random().toString(36).substring(7),
                  Math.random().toString(36).substring(7),
                  Math.random().toString(36).substring(7)
                 ]);
});

/*
Endpoint: /api/getTest
*/
router.get('/getTest', function(req, res, next) {
	res.json(['servA', 'servB', 'servC']);
});

/*
Endpoint: /api/getPods
*/
router.get('/getPods', (req, res) => {
  /*
    If we specify the namespace as '' it should get all namespaces
    otherwise use for example default. TODO: make this configurable
  */

  /*Depending if we are executing the Web ui in Mock mode*/

  if (process.env.NODE_ENV === 'mock') {
    console.log('Mock for getPods');
    return res.status(200).json(require('./mocks/getPods.json'));
  }else{
    k8sApi.listNamespacedPod('')
      .then((re) => {
        return res.status(200).json(re.body);
      })
      .catch((err) => {
        res.send(err);
    })
  }
});

/*
Endpoint: /api/getServices
*/
router.get('/getServices', (req, res) => {
  k8sApi.listNamespacedService('')
    .then((re) => {
      return res.status(200).json(re.body);
    })
    .catch((err) => {
      res.send(err);
    })
});

/*
Endpoint: /api/getIngresses
*/
router.get('/getIngresses', (req, res) => {
  k8sApi2.listNamespacedIngress('')
    .then((re) => {
      return res.status(200).json(re.body);
    })
    .catch((err) => {
      res.send(err);
    })
});

/*
Endpoint: /api/getDeployments
*/
router.get('/getDeployments', (req, res) => {
  k8sApi2.listNamespacedDeployment('')
    .then((re) => {
      return res.status(200).json(re.body);
    })
    .catch((err) => {
      res.send(err);
    })
});

module.exports = router;
