import { Layout, Menu } from "antd";
import "antd/dist/antd.css";
import React, { useContext } from "react";
import { Link, useLocation } from "react-router-dom";
import { removeAccessToken, removeRefreshToken } from "../app/token";
import AuthContex, { getRole } from "../contexts/AuthContex";

const { Header } = Layout;

interface NavbarProps {}

const Navbar: React.FC<NavbarProps> = (props: NavbarProps) => {
    let location = useLocation();
    const { token } = useContext(AuthContex);

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
