import React, { useState } from "react";
import { Button, Layout, Spin, Typography, Table, Space, Modal, Form, message } from "antd";
import { SettingOutlined } from "@ant-design/icons";
import AddUserForm from "../containers/AddUserForm";
import UpdateUserDetailsModal from "../containers/UpdateUserDetailsModal";
import { useGet, usePost } from "../utils/apiHooks";

const { Header, Content } = Layout;
const { Title, Text, Link } = Typography;
const { Column } = Table;

interface UserDashboardScreenProps {}

const UserDashboardScreen: React.FC<UserDashboardScreenProps> = (props: UserDashboardScreenProps) => {
    const [addUserVisible, setAddUserVisible] = useState(false);
    const [editUserVisible, setEditUserVisible] = useState(false);
    const [selectedUser, setSelectedUser] = useState<
        undefined | { first_name: string; last_name: string; email: string; username: string }
    >(undefined);
    const [form] = Form.useForm();

    const { data, errors, loading, refetch } = useGet("all_users");
    // console.log("DATA", data);
    const [DeleteUser] = usePost<{}, { user_to_del: string }>("delete_user");
    const [Register] = usePost<
        { refresh_token: string; access_token: string },
        {
            username: string;
            password: string;
            first_name: string;
            last_name: string;
            email: string;
        }
    >("register", form);

    const onFinish = async (values: any) => {
        await Register({
            username: values.username,
            password: values.password,
            first_name: values.first_name,
            last_name: values.last_name,
            email: values.email,
        });

        message.success(`${values.username} registered!`);

        setAddUserVisible(false);
        form.resetFields();
        refetch();
    };

    return (
        <Layout style={{ flexGrow: 1 }}>
            <Modal
                visible={addUserVisible}
                onOk={() => {
                    form.submit();
                }}
                onCancel={() => {
                    setAddUserVisible(false);
                }}
                title={"Add New User"}
            >
                <AddUserForm onFinish={onFinish} form={form} />
            </Modal>
            {selectedUser !== undefined && (
                <UpdateUserDetailsModal
                    visible={editUserVisible}
                    onCancel={() => {
                        setEditUserVisible(false);
                        setSelectedUser(undefined);
                    }}
                    onOk={() => {
                        setSelectedUser(undefined);
                        refetch();
                    }}
                    username={selectedUser.username}
                    initialValues={selectedUser}
                />
            )}
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
                    <Button type={"primary"} onClick={() => setAddUserVisible(true)}>
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
                        render={(
                            text,
                            record: {
                                first_name: string;
                                last_name: string;
                                email: string;
                                username: string;
                                password: string;
                            }
                        ) => (
                            <Space size="middle">
                                <a
                                    onClick={() => {
                                        const { password, ...record_new } = record;
                                        setSelectedUser(record_new);
                                        setEditUserVisible(true);
                                    }}
                                >
                                    Edit
                                </a>
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
