import React, { useState } from "react";
import { Simulate } from "react-dom/test-utils";
import { BrowserRouter as Router, Switch, Route, RouteProps } from "react-router-dom";
import { Layout } from "antd";
import { useTokenListeners } from "./app/token";
import Navbar from "./containers/Navbar";

import "./app/axiosAccess";

import AuthContext from "./contexts/AuthContex";
import DashboardScreen from "./screens/DashboardScreen";
import LoginScreen from "./screens/LoginScreen";
import PlantScreen from "./screens/PlantScreen";
import RegisterScreen from "./screens/RegisterScreen";

import "./App.css";
import "antd/dist/antd.css";
import RedirectRoute from "./utils/RedirectRoute";

const { Header, Footer, Content } = Layout;

function App() {
    const [loading, setLoading] = useState(true);
    const [token, setToken] = useState<string | undefined>(undefined);

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
            <Layout style={{ minHeight: "100vh" }}>
                <Router>
                    {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
                    <Navbar />
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
                                path="/register"
                                exact
                                component={RegisterScreen}
                                redirectOn={token !== undefined}
                                to={"/"}
                            />
                            <ProtectedRoute path="/plant/:id" component={PlantScreen} />
                            <ProtectedRoute path="/" component={DashboardScreen} />
                        </Switch>
                    </Content>
                    <Footer>Smort Plont - Mr. Bean, Mate, Paddy, Thomas Frantz, and Thomas Frantz</Footer>
                </Router>
            </Layout>
        </AuthContext.Provider>
    );
}

export default App;
