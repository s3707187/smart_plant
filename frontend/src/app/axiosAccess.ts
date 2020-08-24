import { apiURL } from "../utils/apiHooks";
import {
    getAccessToken,
    getRefreshToken,
    setAccessToken,
    setRefreshToken,
    removeAccessToken,
    removeRefreshToken,
} from "./token";
import axios from "axios";

axios.interceptors.request.use(
    async (config) => {
        const token = await getAccessToken();
        if (token) {
            config.headers["Authorization"] = `Bearer ${token}`;
            console.log("Setting auth with token");
        }

        config.headers["Content-Type"] = "application/json";
        config.headers["Access-Control-Allow-Origin"] = "*";
        return config;
    },
    (error) => {
        Promise.reject(error);
    }
);

axios.interceptors.response.use(
    (response) => {
        return response;
    },
    // The error handler, runs if we ever get back a 400 or 500 style repsonse (error)
    async (error) => {
        const originalRequest = error.config;

        // 401 == Unauthenticated, ie, the access token was invalid
        if (error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            // Try to get a new access token from the /refresh endpoint
            const refreshToken = await getRefreshToken();
            if (refreshToken == undefined) {
                return Promise.reject(error);
            }
            return axios
                .create()
                .post(
                    `${apiURL}/refresh`,
                    {},
                    {
                        headers: {
                            Authorization: `Bearer ${refreshToken}`,
                        },
                    }
                )
                .then(async (res) => {
                    // if we get a new refresh token
                    console.log(res);
                    if (res.status === 201) {
                        await setAccessToken(res.data.access_token);
                        axios.defaults.headers.common["Authorization"] = `Bearer ${res.data.access_token}`;
                        return axios(originalRequest);
                    }
                })
                .catch(async (e) => {
                    // if we do not get a new refresh token
                    console.error(e);
                    await removeRefreshToken();
                    await removeAccessToken();
                    return Promise.reject(e);
                });
        } else {
            return Promise.reject(error);
        }
    }
);
