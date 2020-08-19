import React, { Component } from 'react';
//@ts-ignore
import { RadarChart } from 'react-vis';
//@ts-ignore
import { Hint } from 'react-vis';
import '../node_modules/react-vis/dist/style.css';

// The first 6 data elements here are to simulate a 'spider' type of radar chart -
// similar to CircularGridLines, but straight edges instead.


var healthMin = .32
var healthMax = .68

var tempData = 0.2
var humidData = 0.4
var lightData = 0.75
var moistData = 0.66

var padVal = 0.005

//@ts-ignore


const LAYOUT = [
    //Layout - domain and healthy range
    {
        name: 'spiderMax',
        temp: 1,
        humidity: 1,
        light: 1,
        moisture: 1,

        fill: '#f8f8f8',
        stroke: '#cccccc'
    },

    //Outer axes, so that they appear "below" the healthy range
    {
        name: 'tempAx2',
        temp: 1,
        humidity: 0.001,
        light: 0.001,
        moisture: 0.001,

        fill: 'black',
        stroke: '#cccccc'
    },
    {
        name: 'humidAx2',
        temp: 0.001,
        humidity: 1,
        light: 0.001,
        moisture: 0.001,

        fill: 'black',
        stroke: '#cccccc'
    },
    {
        name: 'lightAx2',
        temp: 0.001,
        humidity: 0.001,
        light: 1,
        moisture: 0.001,

        fill: 'black',
        stroke: '#cccccc'
    },
    {
        name: 'moistAx2',
        temp: 0.001,
        humidity: 0.001,
        light: 0.001,
        moisture: 1,

        fill: 'black',
        stroke: '#cccccc'
    },


    //Outer edge of the healthy range
    {
        name: 'healthHighBorder',
        temp: healthMax,
        humidity: healthMax,
        light: healthMax,
        moisture: healthMax,

        fill: 'rgba(114,210,172,0.8)',
        stroke: 'rgba(114,210,172,1)'
    },

    //Inner edge of the healthy range
    {
        name: 'healthLowBorder',
        temp: healthMin,
        humidity: healthMin,
        light: healthMin,
        moisture: healthMin,

        fill: '#f8f8f8',
        stroke: '#cccccc'
    },

    //The center dot, indicating minimum value
    {
        name: 'minVal',
        temp: 0.001,
        humidity: 0.001,
        light: 0.001,
        moisture: 0.001,

        fill: '#f8f8f8',
        stroke: '#cccccc'
    },


    //Inner portion of the axes
    {
        name: 'tempAx',
        temp: healthMin,
        humidity: 0.001,
        light: 0.001,
        moisture: 0.001,

        fill: 'black',
        stroke: '#cccccc'
    },
    {
        name: 'humidAx',
        temp: 0.001,
        humidity: healthMin,
        light: 0.001,
        moisture: 0.001,

        fill: 'black',
        stroke: '#cccccc'
    },
    {
        name: 'lightAx',
        temp: 0.001,
        humidity: 0.001,
        light: healthMin,
        moisture: 0.001,

        fill: 'black',
        stroke: '#cccccc'
    },
    {
        name: 'moistAx',
        temp: 0.001,
        humidity: 0.001,
        light: 0.001,
        moisture: healthMin,

        fill: 'black',
        stroke: '#cccccc'
    },
];

//const DATA = toGraphableData(tempData, humidData, lightData, moistData, padVal)
//@ts-ignore
function toGraphableData([tempData, humidData, lightData, moistData, padVal]) {
    return [
        {
            name: 'healthLowPad',
            temp: tempData - padVal,
            humidity: humidData - padVal,
            light: lightData - padVal,
            moisture: moistData - padVal,

            fill: 'rgb(0,0,0,0)',
            stroke: 'red'
        },

        {
            name: 'healthHighPad',
            temp: tempData + padVal,
            humidity: humidData + padVal,
            light: lightData + padVal,
            moisture: moistData + padVal,

            fill: 'rgb(0,0,0,0)',
            stroke: 'red'
        },

        {
            name: 'plant',
            temp: tempData,
            humidity: humidData,
            light: lightData,
            moisture: moistData,

            fill: 'rgb(0,0,0,0)',
            stroke: 'red'
        },
    ]
}

const tipStyle = {
    display: 'flex',
    color: '#fff',
    background: '#000',
    alignItems: 'center',
    padding: '5px',
    //position: "absolute"
};

export default class RadarChartWithTooltips extends Component {
    state = {
        hoveredCell: false
    };

    render() {
        //@ts-ignore
        const { hoveredCell } = this.state;
        //@ts-ignore
        const graphable = toGraphableData(this.props.d1)
        console.log(graphable)
        //@ts-ignore
        const DATA = LAYOUT.concat(graphable);
        console.log(DATA)
        return (
            <div>
                <RadarChart
                    data={DATA}

                    //margin={70}
                    //@ts-ignore
                    tickFormat={t => {
                        return '';
                    }}
                    domains={[
                        {
                            name: 'Temp Score',
                            domain: [0, 1],
                            //@ts-ignore
                            getValue: d => d.temp
                        },
                        {
                            name: 'Humidity Score',
                            domain: [0, 1],
                            //@ts-ignore
                            getValue: d => d.humidity
                        },
                        //@ts-ignore
                        { name: 'Light Score', domain: [0, 1], getValue: d => d.light },
                        //@ts-ignore
                        { name: 'Water Score', domain: [0, 1], getValue: d => d.moisture },
                        //@ts-ignore
                    ]}
                    width={400}
                    height={400}
                    //@ts-ignore
                    onValueMouseOver={v => {
                        this.setState({ hoveredCell: v });
                    }}
                    //@ts-ignore
                    onValueMouseOut={v => this.setState({ hoveredCell: false })}
                    style={{

                        labels: {
                            textAnchor: 'middle',
                            fontSize: '0px'
                        },
                        polygons: {
                            strokeWidth: 2

                        },
                        axes: {
                            line: {
                                fillOpacity: 0,
                                strokeWidth: 0,
                                strokeOpacity: 0
                            },
                            ticks: {
                                strokeOpacity: 0,
                            }

                            //margin: '100px'

                        },
                    }

                    }
                    colorRange={['transparent']}
                    hideInnerMostValues={false}
                    renderAxesOverPolygons={true}
                >
                    {hoveredCell &&
                        //@ts-ignore
                        hoveredCell.dataName === 'plant' && (
                            <Hint value={hoveredCell}>
                                <div style={tipStyle}>
                                    {
                                        //@ts-ignore
                                        hoveredCell.domain}: {hoveredCell.value}
                                </div>
                            </Hint>
                        )}
                </RadarChart>
            </div >



        );
    }
}
