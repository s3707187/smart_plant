import React, { useState } from "react";
import { Layout, Typography, Menu } from "antd";
import HistoryVisualisationComponent from "../components/HistoryVisualisationComponent";
import HealthVisualisationComponent from "../components/HealthVisualisationComponent";
import PlantHealthContainer from "../containers/PlantHealthContainer";
import PlantHistoryContainer from "../containers/PlantHistoryContainer";
import PlantUsersContainer from "../containers/PlantUsersContainer";
import { useGet } from "../utils/apiHooks";
import { useParams } from "react-router-dom";
import { CloseCircleOutlined } from "@ant-design/icons";

const { Title, Text, Link } = Typography;

var healthMin = 0.32;
var healthMax = 0.68;

//@ts-ignore
function toGraphableData([tempData, humidData, lightData, moistData, padVal]) {
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

const tipStyle = {
    display: "flex",
    color: "#fff",
    background: "#000",
    alignItems: "center",
    padding: "5px",
    //position: "absolute"
};

interface PlantScreenProps {}
const { Content, Header } = Layout;

const PlantScreen: React.FC<PlantScreenProps> = (props: PlantScreenProps) => {
    const { id: plant_id } = useParams();

    const { data, errors, loading } = useGet<
        {
            latest_reading?: {
                date_time: string;
                humidity: number;
                light: number;
                moisture: number;
                plant_id: number;
                temperature: number;
            };
            plant_name: string;
            plant_id: number;
            plant_type: string;
            plant_health: string;
            password: string;
            access: "read" | "edit";
        },
        { plant_id: number }
    >("view_plant_details", { plant_id });

    console.log("PLANT DATA", data);

    return (
        <Layout>
            <Header style={{ background: "#FFF", display: "flex", alignItems: "center" }}>
                <Typography.Title level={2} style={{ marginBottom: "0.25em" }}>
                    {data?.plant_name}
                </Typography.Title>
            </Header>
            <Content
                style={{
                    margin: 20,
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    justifyContent: "center",
                }}
            >
                <div
                    style={{
                        display: "flex",
                        flexDirection: "row",
                        alignItems: "flex-start",
                        flexWrap: "wrap",
                        justifyContent: "center",
                    }}
                >
                    <PlantHealthContainer plant_id={plant_id} />
                    <PlantHistoryContainer plant_id={plant_id} />
                </div>
                <div
                    style={{
                        margin: 20,
                        display: "flex",

                        flexDirection: "column",
                        alignItems: "center",
                        justifyContent: "center",
                    }}
                >
                    <Title level={2}>Plant Details</Title>
                    <Text>
                        <Text style={{ fontWeight: "bold" }}>Password:</Text> {data?.password || "No password set"}
                        <br />
                        <Text style={{ fontWeight: "bold" }}>Plant Type:</Text>{" "}
                        {data?.plant_type || "No plant type set"}
                    </Text>
                </div>
                <PlantUsersContainer plant_id={plant_id} canEdit={data?.access === "edit"} />
            </Content>
        </Layout>
    );
};

export default PlantScreen;
