import React from "react";
import { Typography } from "antd";
import HealthVisualisationComponent from "../components/HealthVisualisationComponent";
import { useGet } from "../utils/apiHooks";

const { Text, Title } = Typography;

interface PlantHealthContainerProps {
    plant_id: number;
}

const PlantHealthContainer: React.FC<PlantHealthContainerProps> = (props: PlantHealthContainerProps) => {
    const { plant_id } = props;
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
        },
        { plant_id: number }
    >("view_plant_details", { plant_id });
    console.log("data", data);

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
            <Title level={2}>Plant Health</Title>
            {data?.latest_reading && (
                <HealthVisualisationComponent
                    style={{ width: 400, height: 400 }}
                    d1={[
                        data.latest_reading.temperature,
                        data.latest_reading.humidity,
                        data.latest_reading.light,
                        data.latest_reading.moisture,
                        0.002,
                    ]}
                />
            )}
            {data?.latest_reading == null && <Text>There are no current readings for the plant.</Text>}
        </div>
    );
};

export default PlantHealthContainer;
