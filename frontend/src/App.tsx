import React, { useState } from "react";
import { BrowserRouter as Router, Switch, Route, RouteProps } from "react-router-dom";
import { Layout } from "antd";
import { useTokenListeners } from "./app/token";
import Navbar from "./containers/Navbar";

import "./app/axiosAccess";

import AuthContext from "./contexts/AuthContex";
import DashboardScreen from "./screens/DashboardScreen";
import LoginScreen from "./screens/LoginScreen";
import RegisterScreen from "./screens/RegisterScreen";

import "./App.css";
import "antd/dist/antd.css";
import RedirectRoute from "./utils/RedirectRoute";

const { Header, Footer, Content } = Layout;

function App() {
    const [token, setToken] = useState<string | undefined>(undefined);

    useTokenListeners((updatedTokens) => {
        console.log(updatedTokens);
        if (updatedTokens.accessToken !== undefined) {
            // accessToken == string | null
            // The following line is just a way to change the null to an undefined for the purpose of the state.
            // null || something == something, string || something == string
            setToken(updatedTokens.accessToken || undefined);
        }
    });

    const ProtectedRoute = (protectedRouteProps: RouteProps) => (
        <RedirectRoute redirectOn={token === undefined} to={"/login"} {...protectedRouteProps} />
    );

    return (
        <AuthContext.Provider value={{ token }}>
            <Layout style={{ minHeight: "100vh" }}>
                <Router>
                    {/* A <Switch> looks through its children <Route>s and
            renders the first one that matches the current URL. */}
                    <Navbar />
                    <Content>
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
