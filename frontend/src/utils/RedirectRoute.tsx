import React from "react";
import { Redirect, Route, RouteProps } from "react-router-dom";

interface RedirectRouteProps extends RouteProps {
    redirectOn: boolean;
    to: string;
}

const RedirectRoute: React.FC<RedirectRouteProps> = (props: RedirectRouteProps) => {
    const { redirectOn, to, children, ...routeProps } = props;
    console.log(redirectOn, to);

    return <Route {...routeProps}>{redirectOn ? <Redirect to={to} /> : children}</Route>;
};

export default RedirectRoute;
