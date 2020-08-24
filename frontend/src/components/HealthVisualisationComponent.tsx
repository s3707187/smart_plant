import React, { Component, useCallback, useLayoutEffect, useState } from "react";
import { RadarChart, Hint } from "react-vis";
import "react-vis/dist/style.css";
import { CloudOutlined, ExperimentOutlined, BulbOutlined, FireOutlined } from "@ant-design/icons";

// The first 6 data elements here are to simulate a 'spider' type of radar chart -
// similar to CircularGridLines, but straight edges instead.

var healthMin = 0.32;
var healthMax = 0.68;

var tempData = 0.2;
var humidData = 0.4;
var lightData = 0.75;
var moistData = 0.66;

var padVal = 0.005;

//@ts-ignore

const LAYOUT = [
    //Layout - domain and healthy range
    {
        name: "spiderMax",
        temp: 1,
        humidity: 1,
        light: 1,
        moisture: 1,

        fill: "#f8f8f8",
        stroke: "#cccccc",
    },

    //Outer axes, so that they appear "below" the healthy range
    {
        name: "tempAx2",
        temp: 1,
        humidity: 0.001,
        light: 0.001,
        moisture: 0.001,

        fill: "black",
        stroke: "#cccccc",
    },
    {
        name: "humidAx2",
        temp: 0.001,
        humidity: 1,
        light: 0.001,
        moisture: 0.001,

        fill: "black",
        stroke: "#cccccc",
    },
    {
        name: "lightAx2",
        temp: 0.001,
        humidity: 0.001,
        light: 1,
        moisture: 0.001,

        fill: "black",
        stroke: "#cccccc",
    },
    {
        name: "moistAx2",
        temp: 0.001,
        humidity: 0.001,
        light: 0.001,
        moisture: 1,

        fill: "black",
        stroke: "#cccccc",
    },

    //Outer edge of the healthy range
    {
        name: "healthHighBorder",
        temp: healthMax,
        humidity: healthMax,
        light: healthMax,
        moisture: healthMax,

        fill: "rgba(114,210,172,0.8)",
        stroke: "rgba(114,210,172,1)",
    },

    //Inner edge of the healthy range
    {
        name: "healthLowBorder",
        temp: healthMin,
        humidity: healthMin,
        light: healthMin,
        moisture: healthMin,

        fill: "#f8f8f8",
        stroke: "#cccccc",
    },

    //The center dot, indicating minimum value
    {
        name: "minVal",
        temp: 0.001,
        humidity: 0.001,
        light: 0.001,
        moisture: 0.001,

        fill: "#f8f8f8",
        stroke: "#cccccc",
    },

    //Inner portion of the axes
    {
        name: "tempAx",
        temp: healthMin,
        humidity: 0.001,
        light: 0.001,
        moisture: 0.001,

        fill: "black",
        stroke: "#cccccc",
    },
    {
        name: "humidAx",
        temp: 0.001,
        humidity: healthMin,
        light: 0.001,
        moisture: 0.001,

        fill: "black",
        stroke: "#cccccc",
    },
    {
        name: "lightAx",
        temp: 0.001,
        humidity: 0.001,
        light: healthMin,
        moisture: 0.001,

        fill: "black",
        stroke: "#cccccc",
    },
    {
        name: "moistAx",
        temp: 0.001,
        humidity: 0.001,
        light: 0.001,
        moisture: healthMin,

        fill: "black",
        stroke: "#cccccc",
    },
];

//const DATA = toGraphableData(tempData, humidData, lightData, moistData, padVal)
//@ts-ignore

interface HealthVisualisationComponentProps {
    d1: [number, number, number, number, number];
    style: any;
}

const HealthVisualisationComponent = (props: HealthVisualisationComponentProps) => {
    const { d1, style } = props;
    const [hoveredCell, setHoveredCell] = useState<false | "">(false);
    const [height, setHeight] = useState<number>(0);
    const [width, setWidth] = useState<number>(0);

    function toGraphableData([tempData, humidData, lightData, moistData, padVal]: [
        number,
        number,
        number,
        number,
        number
    ]) {
        return [
            {
                name: "healthLowPad",
                temp: tempData - padVal,
                humidity: humidData - padVal,
                light: lightData - padVal,
                moisture: moistData - padVal,

                fill: "rgb(0,0,0,0)",
                stroke: "red",
            },

            {
                name: "healthHighPad",
                temp: tempData + padVal,
                humidity: humidData + padVal,
                light: lightData + padVal,
                moisture: moistData + padVal,

                fill: "rgb(0,0,0,0)",
                stroke: "red",
            },

            {
                name: "plant",
                temp: tempData,
                humidity: humidData,
                light: lightData,
                moisture: moistData,

                fill: "rgb(0,0,0,0)",
                stroke: "red",
            },
        ];
    }
    const graphable = toGraphableData(d1);
    const tipStyle = {
        display: "flex",
        color: "#fff",
        background: "#000",
        alignItems: "center",
        padding: "5px",
        //position: "absolute"
    };
    const DATA = LAYOUT.concat(graphable);
    console.log(DATA);

    const div = useCallback((node) => {
        if (node !== null) {
            setHeight(node.getBoundingClientRect().height);
            setWidth(node.getBoundingClientRect().width);
        }
    }, []);

    return (
        <div style={{ display: "flex", flexDirection: "column" }}>
            {/*<p style={{ alignSelf: "center" }}>dank</p>*/}
            <div style={{ display: "flex", justifyContent: "center" }}>
                <FireOutlined style={{ fontSize: 30, color: "#AAAAAA" }} />
            </div>
            <div style={{ display: "flex", flexDirection: "row", alignItems: "center" }}>
                <CloudOutlined style={{ fontSize: 30, color: "#AAAAAA" }} />
                <div ref={div} style={{ ...style }}>
                    <RadarChart
                        data={DATA}
                        tickFormat={(t) => {
                            return "";
                        }}
                        margin={6}
                        //@ts-ignore
                        domains={
                            [
                                {
                                    name: "Temperature Score",
                                    domain: [0, 1],
                                    //@ts-ignore
                                    getValue: (d) => d.temp,
                                },

                                {
                                    name: "Humidity Score",
                                    domain: [0, 1],
                                    //@ts-ignore
                                    getValue: (d) => d.humidity,
                                },

                                {
                                    name: "Light Score",
                                    domain: [0, 1],
                                    //@ts-ignore
                                    getValue: (d) => d.light,
                                },

                                {
                                    name: "Water Score",
                                    domain: [0, 1],
                                    //@ts-ignore
                                    getValue: (d) => d.moisture,
                                },
                            ] as unknown
                        }
                        width={width}
                        height={height}
                        onValueMouseOver={setHoveredCell}
                        onValueMouseOut={() => setHoveredCell(false)}
                        style={{
                            labels: {
                                textAnchor: "middle",
                                fontSize: "0px",
                            },
                            polygons: {
                                strokeWidth: 2,
                            },
                            axes: {
                                line: {
                                    fillOpacity: 0,
                                    strokeWidth: 0,
                                    strokeOpacity: 0,
                                },
                                ticks: {
                                    strokeOpacity: 0,
                                },

                                //margin: '100px'
                            },
                        }}
                        colorRange={["transparent"]}
                        hideInnerMostValues={false}
                        renderAxesOverPolygons={true}
                    >
                        {hoveredCell &&
                            //@ts-ignore
                            hoveredCell.dataName === "plant" && (
                                <Hint value={hoveredCell}>
                                    <div style={tipStyle}>
                                        {
                                            //@ts-ignore
                                            hoveredCell.domain
                                        }
                                        :{" "}
                                        {
                                            //@ts-ignore
                                            hoveredCell.value
                                        }
                                    </div>
                                </Hint>
                            )}
                    </RadarChart>
                </div>

                <ExperimentOutlined style={{ fontSize: 30, color: "#AAAAAA" }} />
            </div>
            <div style={{ display: "flex", justifyContent: "center" }}>
                <BulbOutlined style={{ fontSize: 30, color: "#AAAAAA" }} />
            </div>
        </div>
    );
};

export default HealthVisualisationComponent;
