import React, { useContext, useEffect } from "react";
import { Typography, Layout, Space } from "antd";
import { CloseCircleOutlined, CheckCircleOutlined } from "@ant-design/icons";
import AuthContex, { getUserID } from "../contexts/AuthContex";
import NotificationsContext from "../contexts/NotificationsContext";
import { useGet, usePost } from "../utils/apiHooks";

const { Text, Title } = Typography;
const { Header, Sider } = Layout;

interface NotificationsSidebarProps {
    closeSidebar(): void;
}

const NotificationsSidebar: React.FC<NotificationsSidebarProps> = (props: NotificationsSidebarProps) => {
    const { closeSidebar } = props;
    const { token } = useContext(AuthContex);
    const { data, refetch } = useGet<{ plant_id: number; plant_name: string }[]>("get_plant_notifications");
    console.log("NOTIFICATIONS DATA:", data);

    const { registerNotificationSubscriber, deregisterNotificationSubscriber, refetchAll } = useContext(
        NotificationsContext
    );

    const [AddPlantMaintainer, { loading: addLoading }] = usePost<
        {},
        { user_to_link: string; user_link_type: string; plant_id: number }
    >("add_plant_link");

    useEffect(() => {
        const sub = registerNotificationSubscriber(refetch);
        return () => {
            deregisterNotificationSubscriber(sub);
        };
    }, [refetch, registerNotificationSubscriber, deregisterNotificationSubscriber]);

    return (
        <Sider width={300} style={{ backgroundColor: "#f0f2f5" }}>
            <Header
                style={{
                    backgroundColor: "#FFF",
                    display: "flex",
                    flexDirection: "row",
                    alignItems: "center",
                    justifyContent: "space-between",
                    padding: "0 20px",
                }}
            >
                <Title level={2} style={{ marginBottom: "0.25em" }}>
                    Notifications
                </Title>
                <CloseCircleOutlined onClick={closeSidebar} />
            </Header>
            {data?.map((notification) => (
                <div style={{ backgroundColor: "#FFF", margin: 10, padding: 10, borderRadius: 7 }}>
                    <div
                        style={{
                            display: "flex",
                            flexDirection: "row",
                            alignItems: "center",
                            justifyContent: "space-between",
                        }}
                    >
                        <Title level={4} style={{ margin: 0 }}>
                            {notification.plant_name}
                        </Title>
                        <CheckCircleOutlined
                            disabled={addLoading}
                            onClick={async () => {
                                if (token) {
                                    await AddPlantMaintainer({
                                        user_to_link: getUserID(token),
                                        user_link_type: "maintenance",
                                        plant_id: notification.plant_id,
                                    });
                                    refetchAll();
                                }
                            }}
                        />
                    </div>
                    <Text type={"secondary"}>{notification.plant_id}</Text>
                    <br />
                    <Text>This plant is unhealthy</Text>
                </div>
            ))}
            {data?.length === 0 && <Text>You have no notifications.</Text>}
        </Sider>
    );
};

export default NotificationsSidebar;
