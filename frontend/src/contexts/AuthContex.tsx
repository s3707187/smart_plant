import React, { createContext } from "react";
import jwt_decode from "jwt-decode";

export interface AuthContextProps {
    token?: string;
}

// @ts-ignore
export const getUserID = (token: string): string => jwt_decode(token).identity;
// @ts-ignore
export const getRole = (token: string): "user" | "admin" => jwt_decode(token).user_claims.role;

export default React.createContext<AuthContextProps>({});
