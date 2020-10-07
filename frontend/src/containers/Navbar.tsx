import { Layout, Menu, Badge } from "antd";
import "antd/dist/antd.css";
import React, { useContext, useEffect } from "react";
import { Link, useLocation } from "react-router-dom";
import { removeAccessToken, removeRefreshToken } from "../app/token";
import AuthContex, { getRole } from "../contexts/AuthContex";
import { AlertOutlined } from "@ant-design/icons";
import NotificationsContext from "../contexts/NotificationsContext";
import { useGet } from "../utils/apiHooks";

const { Header } = Layout;

interface NavbarProps {
    openSidebar(): void;
}

const Navbar: React.FC<NavbarProps> = (props: NavbarProps) => {
    let location = useLocation();
    const { openSidebar } = props;
    const { token } = useContext(AuthContex);

    const { data, refetch } = useGet<{ plant_id: number; plant_name: string }[]>("get_plant_notifications");

    const { registerNotificationSubscriber, deregisterNotificationSubscriber } = useContext(NotificationsContext);

    useEffect(() => {
        const sub = registerNotificationSubscriber(refetch);
        return () => {
            deregisterNotificationSubscriber(sub);
        };
    }, [refetch, registerNotificationSubscriber, deregisterNotificationSubscriber]);

    return (
        <Header>
            {/* Make it set the default key a bit better please tom. */}
            <Menu theme="dark" mode="horizontal" defaultSelectedKeys={[location.pathname]}>
                {token === undefined && [
                    <Menu.Item key="/login">
                        <Link to="/login">Login</Link>
                    </Menu.Item>,
                    <Menu.Item key="/register">
                        <Link to="/register">Register</Link>
                    </Menu.Item>,
                ]}
                {token !== undefined && [
                    <Menu.Item key="/">
                        <Link to="/">Home</Link>
                    </Menu.Item>,
                    getRole(token) === "admin" && (
                        <Menu.Item key="/users">
                            <Link to="/users">Users</Link>
                        </Menu.Item>
                    ),
                    <Menu.Item key="/profile">
                        <Link to="/profile">Profile</Link>
                    </Menu.Item>,

                    <Badge count={data?.length || 0} style={{ float: "right", alignSelf: "flex-end" }}>
                        <AlertOutlined style={{ fontSize: 20, margin: "0 15px" }} onClick={openSidebar} />
                    </Badge>,

                    <Menu.Item
                        style={{ float: "right" }}
                        onClick={async () => {
                            await Promise.all([removeAccessToken(), removeRefreshToken()]);
                        }}
                    >
                        Logout
                    </Menu.Item>,
                ]}
            </Menu>
        </Header>
    );
};

export default Navbar;
