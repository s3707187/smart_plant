import React, { createContext } from "react";

export interface AuthContextProps {
    token?: string;
}

export default React.createContext<AuthContextProps>({});
