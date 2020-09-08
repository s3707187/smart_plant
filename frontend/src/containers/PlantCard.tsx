import React from "react";
import { Card } from "antd";
import _ from "lodash";

interface PlantCardProps {
    title: string;
    id: string;
    overallHealth: string;
}

const PlantCard: React.FC<PlantCardProps> = (props: PlantCardProps) => {
    const { title, overallHealth, id } = props;
    return (
        <Card title={title} extra={<a href={`/plant/${id}`}>View</a>} style={{ width: 300, margin: 20, flexGrow: 0 }}>
            <p>{overallHealth}</p>
        </Card>
    );
};

export default PlantCard;
