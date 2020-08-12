import React, { useEffect, useState } from "react";
import axios, { AxiosResponse } from "axios";

export const apiURL =
    !process.env.NODE_ENV || process.env.NODE_ENV === "development"
        ? "http://127.0.0.1:8080"
        : "https://smart-plant-1.uc.r.appspot.com";

export interface ResponseError {}
export type ResponseData<Data> = AxiosResponse<Data>;

export const useGet = <Data = {}, Variables = {}>(
    route: string
): {
    data?: Data;
    errors?: ResponseError[];
    loading: boolean;
} => {
    const [data, setData] = useState<Data | undefined>(undefined);
    const [errors, setErrors] = useState<ResponseError[] | undefined>(undefined);
    const [loading, setLoading] = useState<boolean>(false);

    const request = async (variables?: Variables) => {
        setLoading(true);

        // TODO change this so it works with post, etc.
        // TODO proper error shit
        const result = await axios.get<Data>(`${apiURL}/${route}`, {
            data: variables,
        });

        setLoading(false);
        setData(result?.data);

        return result;
    };

    useEffect(() => {
        request().then().catch();
    }, []);

    return { data, errors, loading };
};

export const usePost = <Data = {}, Variables = {}>(
    route: string
): [
    (variables: Variables) => Promise<AxiosResponse<Data>>,
    {
        data?: Data;
        errors?: ResponseError[];
        loading: boolean;
    }
] => {
    const [data, setData] = useState<Data | undefined>(undefined);
    const [errors, setErrors] = useState<ResponseError[] | undefined>(undefined);
    const [loading, setLoading] = useState<boolean>(false);

    const request = async (variables: Variables) => {
        setLoading(true);

        // TODO change this so it works with post, etc.
        // TODO proper error shit
        const result = await axios.post<Data>(`${apiURL}/${route}`, {
            data: variables,
        });

        setLoading(false);
        setData(result.data);

        return result;
    };

    return [request, { data, errors, loading }];
};
