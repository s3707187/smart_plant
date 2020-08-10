import React, { createContext } from "react";

export interface AuthContextProps {
    token?: string;
    setToken(token: string): void;
}

export default React.createContext<AuthContextProps>({
    setToken(token: string) {
        console.error("Not implemented");
    },
});
