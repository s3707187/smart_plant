import React, { useContext } from "react";
import { Layout, Typography } from "antd";
import { useParams } from "react-router-dom";
import AuthContex, { getUserID } from "../contexts/AuthContex";
import { useGet } from "../utils/apiHooks";
import jwt_decode from "jwt-decode";

const { Content } = Layout;
const { Text, Title } = Typography;

interface UserScreenProps {}

const UserScreen: React.FC<UserScreenProps> = (props: UserScreenProps) => {
    const { token } = useContext(AuthContex);

    const { data, loading, errors } = useGet(
        "get_user_details",
        { user_to_query: token && getUserID(token) },
        token === undefined
    );

    console.log(data);

    return (
        <Layout>
            <Content
                style={{
                    margin: 20,
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    // justifyContent: "center",
                }}
            >
                Hey barry it's me
            </Content>
        </Layout>
    );
};

export default UserScreen;
