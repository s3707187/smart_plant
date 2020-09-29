import React, { useState } from "react";
import { useGet } from "../utils/apiHooks";
import { Layout, Typography, Menu } from "antd";
import { CloseCircleOutlined } from "@ant-design/icons";

const { Title, Text, Link } = Typography;

interface PlantUserAccessComponentProps {
    name: string;
    onDelete: () => void;
    canEdit: boolean;
}

const PlantUserAccessComponent: React.FC<PlantUserAccessComponentProps> = (props: PlantUserAccessComponentProps) => {
    const { name, onDelete, canEdit } = props;

    return (
        <div
            style={{
                display: "flex",
                flexDirection: "row",
                alignItems: "center",
                justifyItems: "center",
                marginBottom: 7,
            }}
        >
            <Text>{name}</Text>
            {canEdit && <CloseCircleOutlined style={{ fontSize: 15, marginLeft: 15 }} onClick={onDelete} />}
        </div>
    );
};

export default PlantUserAccessComponent;
