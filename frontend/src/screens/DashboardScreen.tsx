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
const { Title } = Typography;

interface DashboardScreenProps {}

type GetUsersPlantsData = {
    plant_id: number;
    plant_type: string;
    plant_health: string;
    plant_name: string;
    password: string;
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
                    <Button type={"primary"} onClick={() => setVisible(true)}>
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
            <Content
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
                        />
                    ))}
            </Content>
        </Layout>
    );
};

export default DashboardScreen;
