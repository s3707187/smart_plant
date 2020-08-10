import { Layout, Menu } from "antd";
import "antd/dist/antd.css";
import React from "react";
import { Link, useLocation } from "react-router-dom";

const { Header } = Layout;

interface NavbarProps {}

const Navbar: React.FC<NavbarProps> = (props: NavbarProps) => {
    let location = useLocation();

    return (
        <Header>
            {/* Make it set the default key a bit better please tom. */}
            <Menu theme="dark" mode="horizontal" defaultSelectedKeys={[location.pathname]}>
                <Menu.Item key="/">
                    <Link to="/">Home</Link>
                </Menu.Item>
                <Menu.Item key="/about">
                    <Link to="/about">About</Link>
                </Menu.Item>
                <Menu.Item key="/users">
                    <Link to="/users">Users</Link>
                </Menu.Item>
            </Menu>
        </Header>
    );
};

export default Navbar;
