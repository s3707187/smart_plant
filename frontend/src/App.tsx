import React, { useState } from "react";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import { Layout } from "antd";
import Navbar from "./containers/Navbar";

import "./app/axiosAccess";

import AuthContext from "./contexts/AuthContex";
import DashboardScreen from "./screens/DashboardScreen";
import LoginScreen from "./screens/LoginScreen";
import RegisterScreen from "./screens/RegisterScreen";

import "./App.css";
import "antd/dist/antd.css";

const { Header, Footer, Content } = Layout;

function App() {
    const [token, setToken] = useState<string | undefined>();

    return (
        <AuthContext.Provider value={{ token, setToken }}>
            <Layout style={{ minHeight: "100vh" }}>
                <Router>
                    {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
                    <Navbar />
                    <Content>
                        <Switch>
                            <Route path="/about" component={LoginScreen} />
                            <Route path="/users" component={RegisterScreen} />
                            <Route path="/" component={DashboardScreen} />
                        </Switch>
                    </Content>
                    <Footer>Smort Plont - Mr. Bean, Mate, Paddy, Thomas Frantz, and Thomas Frantz</Footer>
                </Router>
            </Layout>
        </AuthContext.Provider>
    );
}

export default App;
