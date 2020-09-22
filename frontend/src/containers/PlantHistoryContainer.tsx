import React from "react";
import { Typography } from "antd";
import { useGet } from "../utils/apiHooks";
import HistoryVisualisationComponent from "../components/HistoryVisualisationComponent";

const { Text, Title } = Typography;

interface PlantHistoryComponentProps {
    plant_id: number;
}

const PlantHistoryContainer: React.FC<PlantHistoryComponentProps> = (props: PlantHistoryComponentProps) => {
    const { plant_id } = props;

    const { data } = useGet<
        {
            date_time: string;
            humidity: number;
            light: number;
            moisture: number;
            plant_id: number;
            temperature: number;
        }[],
        { plant_id: number }
    >("get_plant_records", { plant_id });
    console.log(data);

    return (
        <div
            style={{
                margin: 20,
                display: "flex",

                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
            }}
        >
            <Title level={2}>Plant History</Title>
            {/* TODO hook this up to API */}
            <HistoryVisualisationComponent
                rawData={
                    data?.map((item) => ({ ...item, date: new Date(item.date_time), temp: item.temperature })) || []
                }
            />
        </div>
    );
};

export default PlantHistoryContainer;
