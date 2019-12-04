// require statements
const express = require('express')
const app = express();
const bodyParser = require('body-parser');
const path = require('path');

// k8s javascript client require
const k8s = require('@kubernetes/client-node');
const kc = new k8s.KubeConfig();
kc.loadFromDefault();

/* Core_v1Api docs: https://github.com/kubernetes-client/java/blob/master/kubernetes/docs/CoreV1Api.md */
// core_v1api -- pods, services (may include nodeport, loadbalancer)
// optional: serviceaccount, resourcequota, replication controller if needed
const k8sApi = kc.makeApiClient(k8s.Core_v1Api);

/* Extensions_v1beta1Api docs: https://github.com/kubernetes-client/java/blob/master/kubernetes/docs/ExtensionsV1beta1Api.md */
// extensions_v1beta1api -- ingress, deployment
// optional: daemonset, and network policy as well as replica set if needed
const k8sApi2 = kc.makeApiClient(k8s.Extensions_v1beta1Api);

// use statements
app.use(bodyParser.json());

app.use(function(req, res, next) {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");
  next();
});

app.use(express.static(path.join(__dirname, '../../dist')))

app.get('/', (req, res) => {
  console.log('serving index.html from ', __dirname)
  return res.status(200).sendFile(path.join(__dirname, '../../dist/index.html'))
  // res.sendFile(path.join(__dirname, '../../dist/index.html'));
});

app.get('/main.js', (req, res) => {
  return res.status(200).sendFile(path.join(__dirname, '../../dist/main.js'));
});

app.get('/pod', (req, res) => {
  /*
    If we specify the namespace as '' it should get all namespaces
    otherwise use for example default. TODO: make this configurable
  */
  k8sApi.listNamespacedPod('')
    .then((re) => {
      return res.status(200).json(re.body);
    })
    .catch((err) => {
      res.send(err);
    })
});

app.get('/service', (req, res) => {
  k8sApi.listNamespacedService('')
    .then((re) => {
      return res.status(200).json(re.body);
    })
    .catch((err) => {
      res.send(err);
    })
});

app.get('/ingress', (req, res) => {
  k8sApi2.listNamespacedIngress('')
    .then((re) => {
      return res.status(200).json(re.body);
    })
    .catch((err) => {
      res.send(err);
    })
});

app.get('/deployment', (req, res) => {
  k8sApi2.listNamespacedDeployment('')
    .then((re) => {
      return res.status(200).json(re.body);
    })
    .catch((err) => {
      res.send(err);
    })
});

app.get('/daemonset', (req, res) => {
  k8sApi2.listNamespacedDaemonSet('')
    .then((re) => {
      res.json(re.body);
    });
});


module.exports = app
