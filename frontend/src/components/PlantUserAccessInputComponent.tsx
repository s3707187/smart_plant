import React from "react";
import { Input, Typography } from "antd";
import { CloseCircleOutlined, CheckCircleOutlined } from "@ant-design/icons";
import { ResponseError } from "../utils/apiHooks";

const { Text } = Typography;

interface PlantUserAccessInputComponentProps {
    onDone: (name: string) => void;
    onCancel: () => void;
    name: string;
    onChange: (name: string) => void;
    errors?: ResponseError[];
}

const PlantUserAccessInputComponent: React.FC<PlantUserAccessInputComponentProps> = (
    props: PlantUserAccessInputComponentProps
) => {
    const { name, onCancel, onDone, onChange, errors } = props;

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
            <div
                style={{
                    display: "flex",

                    flexDirection: "row",
                    alignItems: "center",
                    justifyContent: "center",
                }}
            >
                <Input placeholder="Basic usage" value={name} onChange={(e) => onChange(e.target.value)} />
                <CloseCircleOutlined style={{ fontSize: 15, marginLeft: 15 }} onClick={onCancel} />
                <CheckCircleOutlined style={{ fontSize: 15, marginLeft: 15 }} onClick={() => onDone(name)} />
            </div>
            {errors && errors.length > 0 && <Text type={"danger"}>{errors[0].message}</Text>}
        </div>
    );
};

export default PlantUserAccessInputComponent;
