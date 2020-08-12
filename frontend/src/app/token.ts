import { useEffect } from "react";

export interface Tokens {
    accessToken?: string | null; // undefined means no update, string means token, null means no token
    refreshToken?: string | null;
}

let listenerIDCounter = 0;
const listeners: {
    [key: number]: (updatedTokens: Tokens) => void;
} = {};

export const getAccessToken = () => {
    return localStorage.getItem("accessToken");
};

export const getRefreshToken = () => {
    return localStorage.getItem("refreshToken");
};

export const setAccessToken = async (token: string) => {
    await localStorage.setItem("accessToken", token);
    Object.values(listeners).forEach((value) => {
        value({ accessToken: token });
    });
};

export const setRefreshToken = async (token: string) => {
    await localStorage.setItem("refreshToken", token);
    Object.values(listeners).forEach((value) => {
        value({ refreshToken: token });
    });
};

export const removeAccessToken = async () => {
    await localStorage.removeItem("accessToken");
    Object.values(listeners).forEach((value) => {
        value({ accessToken: null });
    });
};

export const removeRefreshToken = async () => {
    await localStorage.removeItem("refreshToken");
    Object.values(listeners).forEach((value) => {
        value({ refreshToken: null });
    });
};

export const useTokenListeners = (onUpdate: (updatedTokens: Tokens) => void) => {
    useEffect(() => {
        // Call this only once to set up the tokens
        Promise.all([getAccessToken(), getRefreshToken()]).then((value) => {
            onUpdate({
                accessToken: value[0],
                refreshToken: value[1],
            });
        });
    }, []);

    useEffect(() => {
        const listenerID = listenerIDCounter;

        listeners[listenerID] = onUpdate;

        listenerIDCounter += 1;
        return () => {
            delete listeners[listenerID];
        };
    });
};
