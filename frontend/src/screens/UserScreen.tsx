import React, { useContext, useState } from "react";
import { Button, Layout, Typography, Avatar } from "antd";
import { useParams } from "react-router-dom";
import UpdateUserDetailsModal from "../containers/UpdateUserDetailsModal";
import AuthContex, { getUserID } from "../contexts/AuthContex";
import { useGet } from "../utils/apiHooks";
import jwt_decode from "jwt-decode";
import { SettingOutlined, UserOutlined } from "@ant-design/icons";

const { Content, Header } = Layout;
const { Text, Title } = Typography;

interface UserScreenProps {}

const UserScreen: React.FC<UserScreenProps> = (props: UserScreenProps) => {
    const { token } = useContext(AuthContex);

    const { data, loading, errors, refetch } = useGet(
        "get_user_details",
        { user_to_query: token && getUserID(token) },
        token === undefined
    );

    const [visible, setVisible] = useState(false);

    console.log(data);

    return (
        <>
            {data && (
                <UpdateUserDetailsModal
                    visible={visible}
                    onOk={() => {
                        setVisible(false);
                        refetch({ user_to_query: token && getUserID(token) });
                    }}
                    onCancel={() => setVisible(false)}
                    initialValues={data}
                    username={data.username}
                />
            )}
            <Layout>
                <Header
                    style={{
                        background: "#FFF",
                        display: "flex",
                        flexDirection: "row",
                        alignItems: "center",
                        justifyContent: "space-between",
                    }}
                >
                    <Typography.Title level={2} style={{ marginBottom: "0.25em" }}>
                        {data?.first_name} {data?.last_name}'s Profile
                    </Typography.Title>
                    <div style={{ display: "flex", alignItems: "center", float: "right" }}>
                        <Button type={"primary"} onClick={() => setVisible(true)}>
                            Edit user profile
                        </Button>
                        {/*<SettingOutlined*/}
                        {/*    style={{*/}
                        {/*        fontSize: 20,*/}
                        {/*        padding: 7,*/}
                        {/*        margin: 6,*/}
                        {/*    }}*/}
                        {/*/>*/}
                    </div>
                </Header>
                <Content
                    style={{
                        margin: 20,
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        // justifyContent: "center",
                    }}
                >
                    <Avatar size={128} style={{ margin: 20 }} icon={<UserOutlined />} />
                    <Title level={2}>User Details</Title>
                    <Text>
                        <Text style={{ fontWeight: "bold" }}>First Name:</Text> {data?.first_name}
                    </Text>
                    <Text>
                        <Text style={{ fontWeight: "bold" }}>Last Name:</Text> {data?.last_name}
                    </Text>
                    <Text>
                        <Text style={{ fontWeight: "bold" }}>Email: </Text>
                        {data?.email}
                    </Text>
                    <Text>
                        <Text style={{ fontWeight: "bold" }}>Username: </Text>
                        {data?.username}
                    </Text>
                </Content>
            </Layout>
        </>
    );
};

export default UserScreen;
