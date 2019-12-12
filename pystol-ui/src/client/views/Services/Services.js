import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Badge, Card, CardBody, CardHeader, Col, Row, Table } from 'reactstrap';

//import * as k8s from '@kubernetes/client-node';
import usersData from './ServicesData'


function UserRow(props) {
  const user = props.user
  const userLink = `/users/${user.id}`

  const getBadge = (status) => {
    return status === 'Active' ? 'success' :
      status === 'Inactive' ? 'secondary' :
        status === 'Pending' ? 'warning' :
          status === 'Banned' ? 'danger' :
            'primary'
  }
/*
  return (
    <tr key={user.id.toString()}>
      <th scope="row"><Link to={userLink}>{user.metadata.name}</Link></th>
      <td><Link to={userLink}>{user.name}</Link></td>
      <td>{user.registered}</td>
      <td>{user.role}</td>
      <td><Link to={userLink}><Badge color={getBadge(user.status)}>{user.status}</Badge></Link></td>
    </tr>
  )
  */
//var asdf = user.spec.ports.name !== undefined ? user.spec.ports.name : "-";

var arrayLength = user?.spec?.ports?.length;
for (var i = 0; i < arrayLength; i++) {
  var ports_data = user?.spec?.ports[i];
  break;
}

  return (
    <tr>
      <td>{user?.metadata?.name}</td>
      <td>{user?.spec?.clusterIP}</td>
      <td>{ports_data?.name}</td>
      <td>{ports_data?.port}</td>
      <td>{ports_data?.protocol}</td>
      <td>{ports_data?.targetPort}</td>
    </tr>
  )
}

class Services extends Component {

  constructor(props) {
    super(props);
    this.state = {servicesData: usersData.items};
  }

  async componentDidMount() {

    //import * as k8s from '@kubernetes/client-node';
    const k8s = await require('@kubernetes/client-node');
    console.log(k8s)

    var servicesData = {};
    let kubeclient;

    try {
      const kc = await new k8s.KubeConfig();
      kc.loadFromDefault();
      console.log('Kubernetes config:', kc);

      // Core_v1Api docs: https://github.com/kubernetes-client/java/blob/master/kubernetes/docs/CoreV1Api.md //
      // core_v1api -- pods, services (may include nodeport, loadbalancer)
      // optional: serviceaccount, resourcequota, replication controller if needed
      var k8sApi = kc.makeApiClient(k8s.CoreV1Api);
      // Extensions_v1beta1Api docs: https://github.com/kubernetes-client/java/blob/master/kubernetes/docs/ExtensionsV1beta1Api.md //
      // extensions_v1beta1api -- ingress, deployment
      // optional: daemonset, and network policy as well as replica set if needed
      var k8sApi2 = kc.makeApiClient(k8s.ExtensionsV1beta1Api);
    } catch(e) {
      console.log("Problem creating the K8s client");
      console.log(e);
    } finally {
      servicesData = require('./servicesData.json');
    }


    // Get all services
    try {
      const servic = await k8sApi.listNamespacedService('default')
      console.log('Services data:', servic);
    } catch (e) {
      console.log("Problem fetching data");
      console.log(e);
    }

/*
      k8sApi.listNamespacedService('')
        .then((re) => {
          servicesData = re.body;
        })
        .catch((err) => {
          console.log(err);
          servicesData = require('./servicesData.json');
        })
*/


    //var userList = servicesData.items;

    this.setState({
      servicesData: servicesData.items
    });

  }


  render() {

    //var userList = usersData.items

    return (
      <div className="animated fadeIn">
        <Row>
          <Col xl={12}>
            <Card>
              <CardHeader>
                <i className="fa fa-align-justify"></i> Services <small className="text-muted">installed services for all namespaces</small>
              </CardHeader>
              <CardBody>
                <Table responsive hover>
                  <thead>
                    <tr>
                      <th scope="col">Name</th>
                      <th scope="col">ClusterIP</th>
                      <th scope="col">Name</th>
                      <th scope="col">Port</th>
                      <th scope="col">Protocol</th>
                      <th scope="col">Target Port</th>
                    </tr>
                  </thead>
                  <tbody>
                    {this.state.servicesData.map((user, index) =>
                      <UserRow key={index} user={user}/>
                    )}
                  </tbody>
                </Table>
              </CardBody>
            </Card>
          </Col>
        </Row>
      </div>
    )
  }
}

export default Services;
