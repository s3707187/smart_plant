import React from "react";
import { Button, Layout, Typography } from "antd";
import PlantCard from "../containers/PlantCard";
import { useGet } from "../utils/apiHooks";
import { Redirect } from "react-router-dom";
import { SettingOutlined } from "@ant-design/icons";

const { Content, Sider, Header } = Layout;
const { Title } = Typography;

interface DashboardScreenProps {}

type GetUsersPlantsData = {
    plant_id: number;
    user_type: "plant_manager" | "viewer";
    username: string;
}[];

interface GetCurrentUserData {
    username: string;
}

const DashboardScreen: React.FC<DashboardScreenProps> = (props: DashboardScreenProps) => {
    const { data, loading, errors } = useGet<GetUsersPlantsData>("get_users_plants");
    const { data: currentUserData } = useGet<GetCurrentUserData>("current_user");

    console.log(data, loading, errors, "dashboard", currentUserData);

    if (loading) {
        return <p>Loading ...</p>;
    } else if (errors) {
        return <p>Errors!</p>;
    }

    return (
        <Layout>
            <Header
                style={{
                    background: "#FFF",
                    flexGrow: 1,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                }}
            >
                <Title level={2} style={{ marginBottom: "0.25em" }}>
                    {currentUserData && currentUserData.username}'s Dashboard
                </Title>
                <div style={{ display: "flex", alignItems: "center" }}>
                    <Button type={"primary"}>Add Plant</Button>
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
                style={{ display: "flex", flexDirection: "row", flexWrap: "wrap", justifyContent: "space-around" }}
            >
                {data &&
                    data.map((item) => (
                        <PlantCard
                            id={item.plant_id.toString()}
                            userType={item.user_type}
                            key={item.plant_id}
                            title={"TODO"}
                            overallHealth={"healthy"}
                        />
                    ))}
            </Content>
        </Layout>
    );
};

export default DashboardScreen;
