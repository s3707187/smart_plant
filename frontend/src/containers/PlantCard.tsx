import React, { useContext } from "react";
import { Card, Typography } from "antd";
import _ from "lodash";
import AuthContex, { getUserID } from "../contexts/AuthContex";

const { Text, Title } = Typography;

interface PlantCardProps {
    title: string;
    id: string;
    overallHealth: string;
    maintainer?: string;
    plant_type?: string;
}

const imagePaths = {
    "Cactus type": "cactus",
    "Flowering type": "flower",
    "Foliage type": "foliage",
};

const PlantCard: React.FC<PlantCardProps> = (props: PlantCardProps) => {
    const { title, overallHealth, id, maintainer, plant_type } = props;
    const { token } = useContext(AuthContex);

    const userID = token && getUserID(token);
    const cardHeaderStyle =
        overallHealth.toLowerCase() === "healthy"
            ? "#DFD" // Healthy (Green)
            : !maintainer
            ? "#FDD" // No maintainer (Red)
            : maintainer === userID
            ? "#DDF" // We are the maintainer (Blue)
            : "#FFD"; // Someone else is the maintainer (Yellow)
    return (
        <Card
            title={title}
            headStyle={{
                backgroundColor: cardHeaderStyle,
            }}
            extra={<a href={`/plant/${id}`}>View</a>}
            style={{ width: 300, margin: 20, flexGrow: 0 }}
        >
            <div style={{ flexDirection: "row", display: "flex" }}>
                <img
                    // @ts-ignore
                    src={`${process.env.PUBLIC_URL}/${imagePaths[plant_type || "flower"]}.png`}
                    style={{ marginLeft: -12 }}
                    width={50}
                    height={50}
                />
                <div>
                    <Text>
                        <Text style={{ fontWeight: "bold" }}>Health:</Text> {overallHealth}
                    </Text>
                    <br />
                    <Text>
                        <Text style={{ fontWeight: "bold" }}>Maintainer:</Text> {maintainer || "No Maintainer."}
                    </Text>
                </div>
            </div>
        </Card>
    );
};

export default PlantCard;
