import React, { useState } from "react";
import { Button, Layout, Spin, Typography, Table, Space } from "antd";
import { SettingOutlined } from "@ant-design/icons";
import { useGet, usePost } from "../utils/apiHooks";

const { Header, Content } = Layout;
const { Title, Text, Link } = Typography;
const { Column } = Table;

interface UserDashboardScreenProps {}

const UserDashboardScreen: React.FC<UserDashboardScreenProps> = (props: UserDashboardScreenProps) => {
    const [visible, setVisible] = useState(false);

    const { data, errors, loading, refetch } = useGet("all_users");
    // console.log("DATA", data);
    const [DeleteUser] = usePost<{}, { user_to_del: string }>("delete_user");

    return (
        <Layout style={{ flexGrow: 1 }}>
            <Header
                style={{
                    background: "#FFF",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "space-between",
                }}
            >
                <Title level={2} style={{ marginBottom: "0.25em" }}>
                    Admin User Dashboard
                </Title>
                <div style={{ display: "flex", alignItems: "center" }}>
                    <Button type={"primary"} onClick={() => setVisible(true)}>
                        Add User
                    </Button>
                </div>
            </Header>
            <Content
                style={{
                    margin: 20,
                }}
            >
                <Table dataSource={data}>
                    <Column title="Username" dataIndex="username" key="username" />
                    <Column title="First Name" dataIndex="first_name" key="first_name" />
                    <Column title="Last Name" dataIndex="last_name" key="last_name" />
                    <Column title="Email" dataIndex="email" key="email" />
                    <Column title="User Type" dataIndex="account_type" key="account_type" />
                    <Column
                        title="Action"
                        key="action"
                        render={(text, record: { username: string }) => (
                            <Space size="middle">
                                <a onClick={() => {}}>Edit</a>
                                <a
                                    onClick={async () => {
                                        await DeleteUser({ user_to_del: record.username });
                                        await refetch();
                                    }}
                                >
                                    Delete
                                </a>
                            </Space>
                        )}
                    />
                </Table>
            </Content>
        </Layout>
    );
};

export default UserDashboardScreen;
