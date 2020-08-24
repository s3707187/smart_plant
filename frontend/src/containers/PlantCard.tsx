import React from "react";
import { Card } from "antd";
import _ from "lodash";

interface PlantCardProps {
    title: string;
    id: string;
    overallHealth: "healthy" | "warning" | "danger";
    userType?: "plant_manager" | "viewer";
}

const PlantCard: React.FC<PlantCardProps> = (props: PlantCardProps) => {
    const { title, overallHealth, userType, id } = props;
    return (
        <Card title={title} extra={<a href={`/plant/${id}`}>View</a>} style={{ width: 300, margin: 20 }}>
            <p>{overallHealth}</p>
            {userType && (
                <p>
                    You are a <span style={{ fontWeight: "bold" }}>{_.startCase(userType)}</span> on this plant
                </p>
            )}
        </Card>
    );
};

export default PlantCard;
