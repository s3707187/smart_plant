import React, { useEffect, useState } from "react";
import axios, { AxiosResponse } from "axios";

interface Error {}
export type ResponseData<Data> = AxiosResponse<Data>;

export const useGet = <Data = {}, Variables = {}>(
    route: string
): {
    data?: Data;
    errors?: Error[];
    loading: boolean;
} => {
    const [data, setData] = useState<Data | undefined>(undefined);
    const [errors, setErrors] = useState<Error[] | undefined>(undefined);
    const [loading, setLoading] = useState<boolean>(false);

    const request = async (variables?: Variables) => {
        setLoading(true);

        // TODO change this so it works with post, etc.
        // TODO proper error shit
        const result = await axios.get<Data>(`https://smart-plant-1.uc.r.appspot.com/${route}`, {
            data: variables,
        });

        setLoading(false);
        setData(result.data);

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
        errors?: Error[];
        loading: boolean;
    }
] => {
    const [data, setData] = useState<Data | undefined>(undefined);
    const [errors, setErrors] = useState<Error[] | undefined>(undefined);
    const [loading, setLoading] = useState<boolean>(false);

    const request = async (variables: Variables) => {
        setLoading(true);

        // TODO change this so it works with post, etc.
        // TODO proper error shit
        const result = await axios.get<Data>(`https://smart-plant-1.uc.r.appspot.com/${route}`, {
            data: variables,
        });

        setLoading(false);
        setData(result.data);

        return result;
    };

    return [request, { data, errors, loading }];
};
