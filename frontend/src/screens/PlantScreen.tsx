import React, { useState } from "react";
import { Layout, Typography, Menu } from "antd";
import HistoryVisualisationComponent from "../components/HistoryVisualisationComponent";
import HealthVisualisationComponent from "../components/HealthVisualisationComponent";

interface PlantScreenProps {}
const { Content, Header } = Layout;

const PlantScreen: React.FC<PlantScreenProps> = (props: PlantScreenProps) => {
    const [selectedKeys, setSelectedKeys] = useState<string[]>([]);

    return (
        <Layout>
            <Header style={{ background: "#FFF", display: "flex", alignItems: "center" }}>
                <Typography.Title level={2} style={{ marginBottom: "0.25em" }}>
                    Plant Name
                </Typography.Title>
            </Header>
            <Content style={{ margin: 20 }}>
                <Typography.Title level={2}>Plant Health</Typography.Title>
                <HealthVisualisationComponent />
                <Typography.Title level={2}>Plant History</Typography.Title>
                <Menu
                    onClick={({ key }) => {
                        //@ts-ignore
                        setSelectedKeys((prevState) => {
                            //@ts-ignore
                            if (prevState.includes(key)) {
                                return prevState.filter((value) => value != key);
                            } else {
                                return [...prevState, key];
                            }
                        });
                    }}
                    selectedKeys={selectedKeys}
                    mode="horizontal"
                >
                    <Menu.Item key={"temperature"}>Temperature</Menu.Item>
                    <Menu.Item key={"humidity"}>Humidity</Menu.Item>
                    <Menu.Item key={"light"}>Light</Menu.Item>
                    <Menu.Item key={"soil"}>Soil Moisture</Menu.Item>
                </Menu>
                <HistoryVisualisationComponent />
            </Content>
        </Layout>
    );
};

export default PlantScreen;
