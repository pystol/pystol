import React, { Component } from 'react';
import { Bar, Doughnut, Line, Pie, Polar, Radar } from 'react-chartjs-2';
import { Card, CardBody, CardColumns, CardHeader, Col, Row  } from 'reactstrap';
import { CustomTooltips } from '@coreui/coreui-plugin-chartjs-custom-tooltips';

/*D3*/
import * as d3 from 'd3';
import { sankey, sankeyLinkHorizontal } from "d3-sankey";
import Tree from 'react-tree-graph';
import 'react-tree-graph/dist/style.css'


import { Graph } from "react-d3-graph";
/*D3*/

/*
Circos
*/
import Circos, { HEATMAP } from 'react-circos';
import layout from './months.json';
import heatmap from './heatmap.json';
/*
Circos
*/

const line = {
  labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
  datasets: [
    {
      label: 'My First dataset',
      fill: false,
      lineTension: 0.1,
      backgroundColor: 'rgba(75,192,192,0.4)',
      borderColor: 'rgba(75,192,192,1)',
      borderCapStyle: 'butt',
      borderDash: [],
      borderDashOffset: 0.0,
      borderJoinStyle: 'miter',
      pointBorderColor: 'rgba(75,192,192,1)',
      pointBackgroundColor: '#fff',
      pointBorderWidth: 1,
      pointHoverRadius: 5,
      pointHoverBackgroundColor: 'rgba(75,192,192,1)',
      pointHoverBorderColor: 'rgba(220,220,220,1)',
      pointHoverBorderWidth: 2,
      pointRadius: 1,
      pointHitRadius: 10,
      data: [65, 59, 80, 81, 56, 55, 40],
    },
  ],
};

const bar = {
  labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
  datasets: [
    {
      label: 'My First dataset',
      backgroundColor: 'rgba(255,99,132,0.2)',
      borderColor: 'rgba(255,99,132,1)',
      borderWidth: 1,
      hoverBackgroundColor: 'rgba(255,99,132,0.4)',
      hoverBorderColor: 'rgba(255,99,132,1)',
      data: [65, 59, 80, 81, 56, 55, 40],
    },
  ],
};

const doughnut = {
  labels: [
    'Red',
    'Green',
    'Yellow',
  ],
  datasets: [
    {
      data: [300, 50, 100],
      backgroundColor: [
        '#FF6384',
        '#36A2EB',
        '#FFCE56',
      ],
      hoverBackgroundColor: [
        '#FF6384',
        '#36A2EB',
        '#FFCE56',
      ],
    }],
};

const radar = {
  labels: ['Eating', 'Drinking', 'Sleeping', 'Designing', 'Coding', 'Cycling', 'Running'],
  datasets: [
    {
      label: 'My First dataset',
      backgroundColor: 'rgba(179,181,198,0.2)',
      borderColor: 'rgba(179,181,198,1)',
      pointBackgroundColor: 'rgba(179,181,198,1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(179,181,198,1)',
      data: [65, 59, 90, 81, 56, 55, 40],
    },
    {
      label: 'My Second dataset',
      backgroundColor: 'rgba(255,99,132,0.2)',
      borderColor: 'rgba(255,99,132,1)',
      pointBackgroundColor: 'rgba(255,99,132,1)',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: 'rgba(255,99,132,1)',
      data: [28, 48, 40, 19, 96, 27, 100],
    },
  ],
};

const pie = {
  labels: [
    'Red',
    'Green',
    'Yellow',
  ],
  datasets: [
    {
      data: [300, 50, 100],
      backgroundColor: [
        '#FF6384',
        '#36A2EB',
        '#FFCE56',
      ],
      hoverBackgroundColor: [
        '#FF6384',
        '#36A2EB',
        '#FFCE56',
      ],
    }],
};

const polar = {
  datasets: [
    {
      data: [
        11,
        16,
        7,
        3,
        14,
      ],
      backgroundColor: [
        '#FF6384',
        '#4BC0C0',
        '#FFCE56',
        '#E7E9ED',
        '#36A2EB',
      ],
      label: 'My dataset' // for legend
    }],
  labels: [
    'Red',
    'Green',
    'Yellow',
    'Grey',
    'Blue',
  ],
};

const options = {
  tooltips: {
    enabled: false,
    custom: CustomTooltips
  },
  maintainAspectRatio: false
}



/*
D3
*/
const datas = {
	name: 'Parent',
	children: [{
		name: 'Child One',
    children: [{
      name: 'Child One'
       }, {
      name: 'Child Two'
    }]
	   }, {
		name: 'Child Two'
	}]
};
/*
D3
*/

/*d3 graph*/


// graph payload (with minimalist structure)
const data = {
  links: [
          // Groups
          {
              source: "Marvel",
              target: "Heroes",
          },
          {
              source: "Marvel",
              target: "Villains",
          },
          {
              source: "Marvel",
              target: "Teams",
          },
          // Heroes
          {
              source: "Heroes",
              target: "Spider-Man",
          },
          {
              source: "Heroes",
              target: "CAPTAIN MARVEL",
          },
          {
              source: "Heroes",
              target: "HULK",
          },
          {
              source: "Heroes",
              target: "Black Widow",
          },
          {
              source: "Heroes",
              target: "Daredevil",
          },
          {
              source: "Heroes",
              target: "Wolverine",
          },
          {
              source: "Heroes",
              target: "Captain America",
          },
          {
              source: "Heroes",
              target: "Iron Man",
          },
          {
              source: "Heroes",
              target: "THOR",
          },
          // Villains
          {
              source: "Villains",
              target: "Dr. Doom",
          },
          {
              source: "Villains",
              target: "Mystique",
          },
          {
              source: "Villains",
              target: "Red Skull",
          },
          {
              source: "Villains",
              target: "Ronan",
          },
          {
              source: "Villains",
              target: "Magneto",
          },
          {
              source: "Villains",
              target: "Thanos",
          },
          {
              source: "Villains",
              target: "Black Cat",
          },
          // Teams
          {
              source: "Teams",
              target: "Avengers",
          },
          {
              source: "Teams",
              target: "Guardians of the Galaxy",
          },
          {
              source: "Teams",
              target: "Defenders",
          },
          {
              source: "Teams",
              target: "X-Men",
          },
          {
              source: "Teams",
              target: "Fantastic Four",
          },
          {
              source: "Teams",
              target: "Inhumans",
          },
      ],
      nodes: [
          // Groups
          {
              id: "Marvel",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/marvel.png",
              size: 500,
              fontSize: 18,
          },
          {
              id: "Heroes",
              symbolType: "circle",
              color: "red",
              size: 300,
          },
          {
              id: "Villains",
              symbolType: "circle",
              color: "red",
              size: 300,
          },
          {
              id: "Teams",
              symbolType: "circle",
              color: "red",
              size: 300,
          },
          // Heroes
          {
              id: "Spider-Man",
              name: "Peter Benjamin Parker",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_spiderman.png",
              size: 400,
          },
          {
              id: "CAPTAIN MARVEL",
              name: "Carol Danvers",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_captainmarvel.png",
              size: 400,
          },
          {
              id: "HULK",
              name: "Robert Bruce Banner",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_hulk.png",
              size: 400,
          },
          {
              id: "Black Widow",
              name: "Natasha Alianovna Romanova",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_blackwidow.png",
              size: 400,
          },
          {
              id: "Daredevil",
              name: "Matthew Michael Murdock",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_daredevil.png",
              size: 400,
          },
          {
              id: "Wolverine",
              name: "James Howlett",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_wolverine.png",
              size: 400,
          },
          {
              id: "Captain America",
              name: "Steven Rogers",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_captainamerica.png",
              size: 400,
          },
          {
              id: "Iron Man",
              name: "Tony Stark",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_ironman.png",
              size: 400,
          },
          {
              id: "THOR",
              name: "Thor Odinson",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_thor.png",
              size: 400,
          },
          // Villains
          {
              id: "Dr. Doom",
              name: "Victor von Doom",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/drdoom.png",
              size: 400,
          },
          {
              id: "Mystique",
              name: "Unrevealed",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/mystique.png",
              size: 400,
          },
          {
              id: "Red Skull",
              name: "Johann Shmidt",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/redskull.png",
              size: 400,
          },
          {
              id: "Ronan",
              name: "Ronan",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/ronan.png",
              size: 400,
          },
          {
              id: "Magneto",
              name: "Max Eisenhardt",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/magneto.png",
              size: 400,
          },
          {
              id: "Thanos",
              name: "Thanos",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/thanos.png",
              size: 400,
          },
          {
              id: "Black Cat",
              name: "Felicia Hardy",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/blackcat.png",
              size: 400,
          },
          // Teams
          {
              id: "Avengers",
              name: "",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/avengers.png",
              size: 400,
          },
          {
              id: "Guardians of the Galaxy",
              name: "",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/gofgalaxy.png",
              size: 400,
          },
          {
              id: "Defenders",
              name: "",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/defenders.png",
              size: 400,
          },
          {
              id: "X-Men",
              name: "",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/xmen.png",
              size: 400,
          },
          {
              id: "Fantastic Four",
              name: "",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/fantasticfour.png",
              size: 400,
          },
          {
              id: "Inhumans",
              name: "",
              svg: "http://marvel-force-chart.surge.sh/marvel_force_chart_img/inhumans.png",
              size: 400,
          },
      ],
};

// the graph configuration, you only need to pass down properties
// that you want to override, otherwise default ones will be used
const myConfig = {
  directed: true,
  automaticRearrangeAfterDropNode: true,
  collapsible: true,
  height: 400,
  highlightDegree: 2,
  highlightOpacity: 0.2,
  linkHighlightBehavior: true,
  maxZoom: 12,
  minZoom: 0.05,
  nodeHighlightBehavior: true,
  panAndZoom: false,
  staticGraph: false,
  width: 800,
  d3: {
      alphaTarget: 0.05,
      gravity: -250,
      linkLength: 120,
      linkStrength: 2,
  },
  node: {
      color: "#d3d3d3",
      fontColor: "black",
      fontSize: 10,
      fontWeight: "normal",
      highlightColor: "red",
      highlightFontSize: 14,
      highlightFontWeight: "bold",
      highlightStrokeColor: "red",
      highlightStrokeWidth: 1.5,
      labelProperty: n => (n.name ? `${n.id} - ${n.name}` : n.id),
      mouseCursor: "crosshair",
      opacity: 0.9,
      renderLabel: true,
      size: 200,
      strokeColor: "none",
      strokeWidth: 1.5,
      svg: "",
      symbolType: "circle",
      viewGenerator: null,
  },
  link: {
      color: "lightgray",
      highlightColor: "red",
      mouseCursor: "pointer",
      opacity: 1,
      semanticStrokeWidth: true,
      strokeWidth: 3,
      type: "STRAIGHT",
  },
};

// graph event callbacks
const onClickGraph = function() {
    window.alert(`Clicked the graph background`);
};

const onClickNode = function(nodeId) {
    window.alert(`Clicked node ${nodeId}`);
};

const onDoubleClickNode = function(nodeId) {
    window.alert(`Double clicked node ${nodeId}`);
};

const onRightClickNode = function(event, nodeId) {
    window.alert(`Right clicked node ${nodeId}`);
};

const onMouseOverNode = function(nodeId) {
    window.alert(`Mouse over node ${nodeId}`);
};

const onMouseOutNode = function(nodeId) {
    window.alert(`Mouse out node ${nodeId}`);
};

const onClickLink = function(source, target) {
    window.alert(`Clicked link between ${source} and ${target}`);
};

const onRightClickLink = function(event, source, target) {
    window.alert(`Right clicked link between ${source} and ${target}`);
};

const onMouseOverLink = function(source, target) {
    window.alert(`Mouse over in link between ${source} and ${target}`);
};

const onMouseOutLink = function(source, target) {
    window.alert(`Mouse out link between ${source} and ${target}`);
};

const onNodePositionChange = function(nodeId, x, y) {
    window.alert(`Node ${nodeId} is moved to new position. New position is x= ${x} y= ${y}`);
};

/*d3*/

/*Circos*/
const size = 800;
/*Circos*/

class Charts extends Component {

  render() {

    return (
      <div className="animated fadeIn">
      <Row>
        <Col xs="12">
          <Card>
            <CardHeader>
              Line Chart
              <div className="card-header-actions">
                <a href="http://www.chartjs.org" className="card-header-action">
                  <small className="text-muted">docs</small>
                </a>
              </div>
            </CardHeader>
            <CardBody>
              <div className="chart-wrapper">
                <Line data={line} options={options} />
              </div>
            </CardBody>
          </Card>
          <Card>
            <CardHeader>
              Bar Chart
              <div className="card-header-actions">
                <a href="http://www.chartjs.org" className="card-header-action">
                  <small className="text-muted">docs</small>
                </a>
              </div>
            </CardHeader>
            <CardBody>
              <div className="chart-wrapper">
                <Bar data={bar} options={options} />
              </div>
            </CardBody>
          </Card>
          <Card>
            <CardHeader>
              Doughnut Chart
              <div className="card-header-actions">
                <a href="http://www.chartjs.org" className="card-header-action">
                  <small className="text-muted">docs</small>
                </a>
              </div>
            </CardHeader>
            <CardBody>
              <div className="chart-wrapper">
                <Doughnut data={doughnut} />
              </div>
            </CardBody>
          </Card>
          <Card>
            <CardHeader>
              Radar Chart
              <div className="card-header-actions">
                <a href="http://www.chartjs.org" className="card-header-action">
                  <small className="text-muted">docs</small>
                </a>
              </div>
            </CardHeader>
            <CardBody>
              <div className="chart-wrapper">
                <Radar data={radar} />
              </div>
            </CardBody>
          </Card>
          <Card>
            <CardHeader>
              Pie Chart
              <div className="card-header-actions">
                <a href="http://www.chartjs.org" className="card-header-action">
                  <small className="text-muted">docs</small>
                </a>
              </div>
            </CardHeader>
            <CardBody>
              <div className="chart-wrapper">
                <Pie data={pie} />
              </div>
            </CardBody>
          </Card>
          <Card>
            <CardHeader>
              Polar Area Chart
              <div className="card-header-actions">
                <a href="http://www.chartjs.org" className="card-header-action">
                  <small className="text-muted">docs</small>
                </a>
              </div>
            </CardHeader>
            <CardBody>
              <div className="chart-wrapper">
                <Polar data={polar} options={options}/>
              </div>
            </CardBody>
          </Card>

          <Card>
            <CardHeader>
              D3
              <div className="card-header-actions">
                <a href="http://www.chartjs.org" className="card-header-action">
                  <small className="text-muted">docs</small>
                </a>
              </div>
            </CardHeader>
            <CardBody>
              <div className="chart-wrapper">
              <Tree
              	data={datas}
              	height={400}
              	width={400}/>
              </div>
            </CardBody>
          </Card>

          <Card>
            <CardHeader>
              react-d3-graph
              <div className="card-header-actions">
                <a href="http://www.chartjs.org" className="card-header-action">
                  <small className="text-muted">docs</small>
                </a>
              </div>
            </CardHeader>
            <CardBody>
              <div className="chart-wrapper">
              <Graph
                  id="graph-id" // id is mandatory, if no id is defined rd3g will throw an error
                  data={data}
                  config={myConfig}
                  onClickNode={onClickNode}
                  //onRightClickNode={onRightClickNode}
                  //onClickGraph={onClickGraph}
                  //onClickLink={onClickLink}
                  //onRightClickLink={onRightClickLink}
                  //onMouseOverNode={onMouseOverNode}
                  //onMouseOutNode={onMouseOutNode}
                  //onMouseOverLink={onMouseOverLink}
                  //onMouseOutLink={onMouseOutLink}
                  //onNodePositionChange={onNodePositionChange}
              />
              </div>
            </CardBody>
          </Card>

          <Card>
            <CardHeader>
              Circos
              <div className="card-header-actions">
                <a href="http://www.chartjs.org" className="card-header-action">
                  <small className="text-muted">docs</small>
                </a>
              </div>
            </CardHeader>
            <CardBody>
              <div className="chart-wrapper">
              <Circos
                  size={800}
                  layout={layout}
                  config={{
                    innerRadius: size / 2 - 80,
                    outerRadius: size / 2 - 30,
                    ticks: {
                      display: false,
                    },
                    labels: {
                      position: 'center',
                      display: true,
                      size: 14,
                      color: '#000',
                      radialOffset: 15,
                    },
                  }}
                  tracks={[{
                    type: HEATMAP,
                    data: heatmap,
                    config: {
                      innerRadius: 0.8,
                      outerRadius: 0.98,
                      logScale: false,
                      color: 'YlOrRd',
                    },
                  }]}
                />
              </div>
            </CardBody>
          </Card>
          </Col>
        </Row>
      </div>
    );
  }
}

export default Charts;
