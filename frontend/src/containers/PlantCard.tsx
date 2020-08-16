import React from "react";
import { Card } from "antd";

interface PlantCardProps {
    title: string;
    overallHealth: "healthy" | "warning" | "danger";
}

const PlantCard: React.FC<PlantCardProps> = (props: PlantCardProps) => {
    const { title, overallHealth } = props;
    return (
        <Card title={title} extra={<a href="/plant/id">View</a>} style={{ width: 300, margin: 20 }}>
            {overallHealth}
        </Card>
    );
};

export default PlantCard;
