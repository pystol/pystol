import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { Badge, Card, CardBody, CardHeader, Col, Row, Table } from 'reactstrap';

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

  render() {

    const userList = usersData.items

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
                    {userList.map((user, index) =>
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
