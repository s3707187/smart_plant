import React, { useContext, useState } from "react";
import { Button, Layout, Typography, Spin } from "antd";
import AddNewPlantModal from "../containers/AddNewPlantModal";
import PlantCard from "../containers/PlantCard";
import AuthContex, { getRole } from "../contexts/AuthContex";
import { useGet, usePost } from "../utils/apiHooks";
import { Redirect } from "react-router-dom";
import { SettingOutlined } from "@ant-design/icons";
import { LoadingOutlined } from "@ant-design/icons";

const antIcon = <LoadingOutlined style={{ fontSize: 48 }} spin />;

const { Content, Sider, Header } = Layout;
const { Title, Text } = Typography;

interface DashboardScreenProps {}

type GetUsersPlantsData = {
    plant_id: number;
    plant_type: string;
    plant_health: string;
    plant_name: string;
    password: string;
    maintainer: string | null;
}[];

interface GetCurrentUserData {
    username: string;
}

const DashboardScreen: React.FC<DashboardScreenProps> = (props: DashboardScreenProps) => {
    const { token } = useContext(AuthContex);
    const { data, loading, errors, refetch } = useGet<GetUsersPlantsData>("get_users_plants");
    const { data: currentUserData } = useGet<GetCurrentUserData>("current_user");

    // const data = undefined;
    // const loading = true;
    // const errors = undefined;

    const [visible, setVisible] = useState<boolean>(false);
    const role: undefined | "admin" | "user" = token ? getRole(token) : undefined;

    console.log(data, loading, errors, "dashboard", currentUserData);

    if (errors) {
        return <p>Errors!</p>;
    }

    return (
        <Layout style={{ flexGrow: 1 }}>
            <AddNewPlantModal
                onOk={async () => {
                    setVisible(false);
                    //@ts-ignore
                    await refetch();
                }}
                role={role}
                visible={visible}
                onCancel={() => setVisible(false)}
            />
            <Header
                style={{
                    background: "#FFF",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                }}
            >
                <Title level={2} style={{ marginBottom: "0.25em" }}>
                    {currentUserData && currentUserData.username}'s Dashboard
                </Title>
                <div style={{ display: "flex", alignItems: "center" }}>
                    <Button data-cy="add_plant_button" type={"primary"} onClick={() => setVisible(true)}>
                        Add Plant
                    </Button>
                    <SettingOutlined
                        style={{
                            fontSize: 20,
                            padding: 7,
                            margin: 6,
                        }}
                    />
                </div>
            </Header>
            <Content>
                <div
                    style={{
                        display: "flex",
                        flexDirection: "row",
                        flexGrow: loading ? 1 : 0,
                        flexShrink: loading ? 0 : 1,
                        flexWrap: "wrap",
                        justifyContent: loading ? "center" : "flex-start",
                        alignItems: loading ? "center" : "flex-start",
                    }}
                >
                    {loading && <Spin indicator={antIcon} />}
                    {data &&
                        !loading &&
                        //@ts-ignore
                        data.map((item) => (
                            <PlantCard
                                id={item.plant_id.toString()}
                                key={item.plant_id}
                                title={item.plant_name}
                                overallHealth={item.plant_health}
                                maintainer={item.maintainer || undefined}
                                plant_type={item.plant_type}
                            />
                        ))}
                </div>
                <div
                    style={{
                        backgroundColor: "#FFF",
                        marginLeft: 50,
                        marginRight: 50,
                        padding: 10,
                        flexDirection: "column",
                        display: "flex",
                    }}
                >
                    <Title>Key</Title>
                    <Text style={{ flexDirection: "row", display: "flex", marginBottom: 10 }}>
                        <div style={{ height: 25, width: 25, backgroundColor: "#DFD", marginRight: 10 }} /> Healthy
                    </Text>
                    <Text style={{ flexDirection: "row", display: "flex", marginBottom: 10 }}>
                        <div style={{ height: 25, width: 25, backgroundColor: "#FDD", marginRight: 10 }} /> Unhealthy &
                        No maintainer
                    </Text>
                    <Text style={{ flexDirection: "row", display: "flex", marginBottom: 10 }}>
                        <div style={{ height: 25, width: 25, backgroundColor: "#DDF", marginRight: 10 }} /> Unhealthy &
                        you are maintaining this plant
                    </Text>
                    <Text style={{ flexDirection: "row", display: "flex", marginBottom: 10 }}>
                        <div style={{ height: 25, width: 25, backgroundColor: "#FFD", marginRight: 10 }} /> Unhealthy &
                        someone else is maintaining this plant
                    </Text>
                </div>
            </Content>
        </Layout>
    );
};

export default DashboardScreen;
