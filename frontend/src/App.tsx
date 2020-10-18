import React, { useState } from "react";
import { Simulate } from "react-dom/test-utils";
import { BrowserRouter as Router, Switch, Route, RouteProps } from "react-router-dom";
import { Layout, Typography } from "antd";
import { useTokenListeners } from "./app/token";
import Navbar from "./containers/Navbar";

import "./app/axiosAccess";
import AuthContex from "./contexts/AuthContex";

import AuthContext from "./contexts/AuthContex";
import NotificationsContext from "./contexts/NotificationsContext";
import DashboardScreen from "./screens/DashboardScreen";
import ForgotPasswordScreen from "./screens/ForgotPasswordScreen";
import LoginScreen from "./screens/LoginScreen";
import PlantScreen from "./screens/PlantScreen";
import RegisterScreen from "./screens/RegisterScreen";

import "./App.css";
import "antd/dist/antd.css";
import UserDashboardScreen from "./screens/UserDashboardScreen";
import UserScreen from "./screens/UserScreen";
import RedirectRoute from "./utils/RedirectRoute";
import NotificationsSidebar from "./containers/NotificationsSidebar";

const { Title, Text } = Typography;
const { Header, Footer, Content, Sider } = Layout;

let count = 0;
const notificationsListeners: { [key: number]: () => any } = {};

function App() {
    const [loading, setLoading] = useState(true);
    const [token, setToken] = useState<string | undefined>(undefined);
    const [sidebarVisible, setSidebarVisible] = useState(false);

    useTokenListeners((updatedTokens) => {
        console.log(updatedTokens);
        if (updatedTokens.accessToken !== undefined) {
            // accessToken == string | null
            // The following line is just a way to change the null to an undefined for the purpose of the state.
            // null || something == something, string || something == string
            setToken(updatedTokens.accessToken || undefined);
            setLoading(false);
        }
    });

    const ProtectedRoute = (protectedRouteProps: RouteProps) => (
        <RedirectRoute redirectOn={token === undefined} to={"/login"} {...protectedRouteProps} />
    );

    if (loading) {
        return <p>loading</p>;
    }

    return (
        <AuthContext.Provider value={{ token }}>
            <NotificationsContext.Provider
                value={{
                    registerNotificationSubscriber: (refetch_function: () => any): number => {
                        notificationsListeners[count] = refetch_function;
                        count += 1;
                        return count - 1;
                    },
                    deregisterNotificationSubscriber: (subscriber: number) => {
                        delete notificationsListeners[count];
                    },
                    refetchAll: () => {
                        Object.values(notificationsListeners).forEach((refetch) => refetch());
                    },
                }}
            >
                <Layout style={{ minHeight: "100vh" }}>
                    <Router>
                        {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
                        <Navbar
                            openSidebar={() => {
                                setSidebarVisible(true);
                            }}
                        />
                        <Layout>
                            <Layout>
                                <Content style={{ display: "flex" }}>
                                    <Switch>
                                        <RedirectRoute
                                            path="/login"
                                            exact
                                            component={LoginScreen}
                                            redirectOn={token !== undefined}
                                            to={"/"}
                                        />
                                        <RedirectRoute
                                            path="/forgot_password"
                                            exact
                                            component={ForgotPasswordScreen}
                                            redirectOn={token !== undefined}
                                            to={"/"}
                                        />
                                        <RedirectRoute
                                            path="/register"
                                            exact
                                            component={RegisterScreen}
                                            redirectOn={token !== undefined}
                                            to={"/"}
                                        />
                                        <ProtectedRoute path="/plant/:id" component={PlantScreen} />
                                        <ProtectedRoute path="/profile" component={UserScreen} />
                                        <ProtectedRoute path="/users" component={UserDashboardScreen} />
                                        <ProtectedRoute path="/" component={DashboardScreen} />
                                    </Switch>
                                </Content>
                                <Footer>
                                    Smart Plant - Mitch Wood, Mateo Diaz, Patrick Rohan, Sam Hoch, and Thomas Frantz
                                </Footer>
                            </Layout>
                            {sidebarVisible && <NotificationsSidebar closeSidebar={() => setSidebarVisible(false)} />}
                        </Layout>
                    </Router>
                </Layout>
            </NotificationsContext.Provider>
        </AuthContext.Provider>
    );
}

export default App;
