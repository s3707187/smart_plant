export const getAccessToken = () => {
    return localStorage.getItem("accessToken");
};

export const getRefreshToken = () => {
    return localStorage.getItem("refreshToken");
};

export const setAccessToken = (token: string) => {
    return localStorage.setItem("accessToken", token);
};

export const setRefreshToken = (token: string) => {
    return localStorage.setItem("refreshToken", token);
};

export const removeAccessToken = () => {
    return localStorage.removeItem("access");
};

export const removeRefreshToken = () => {
    return localStorage.removeItem("refresh");
};
