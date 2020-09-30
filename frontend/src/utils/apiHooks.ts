import React, { useEffect, useState } from "react";
import { Form } from "antd";
import { FormInstance } from "antd/es/form";
import axios, { AxiosResponse } from "axios";
import { NamePath } from "antd/lib/form/interface";

export const apiURL =
    !process.env.NODE_ENV || process.env.NODE_ENV === "development"
        ? "http://127.0.0.1:8080"
        : "https://smart-plant-1.uc.r.appspot.com";

export interface ResponseError {
    message: string;
    path: string[];
}
export type ResponseData<Data> = AxiosResponse<Data>;

export const useGet = <Data = {}, Variables = {}>(
    route: string,
    variables?: Variables,
    skip?: boolean
): {
    data?: Data;
    errors?: ResponseError[];
    loading: boolean;
    refetch: (variables?: Variables) => Promise<AxiosResponse<Data>>;
} => {
    const [data, setData] = useState<Data | undefined>(undefined);
    const [errors, setErrors] = useState<ResponseError[] | undefined>(undefined);
    const [loading, setLoading] = useState<boolean>(false);

    const request = async (inner_variables?: Variables) => {
        setLoading(true);

        // TODO change this so it works with post, etc.
        // TODO proper error shit
        const result = await axios.get<Data>(`${apiURL}/${route}`, { params: inner_variables || variables });

        setLoading(false);
        setData(result?.data);

        return result;
    };

    useEffect(() => {
        if (skip !== true) request(variables).then().catch();
    }, []);

    return { data, errors, loading, refetch: request };
};

export const usePost = <Data = {}, Variables = {}>(
    route: string,
    form?: FormInstance
): [
    (variables: Variables) => Promise<AxiosResponse<Data>>,
    { data?: Data; errors?: ResponseError[]; loading: boolean }
] => {
    const [data, setData] = useState<Data | undefined>(undefined);
    const [errors, setErrors] = useState<ResponseError[] | undefined>(undefined);
    const [loading, setLoading] = useState<boolean>(false);

    const request = async (variables: Variables) => {
        setLoading(true);

        // TODO change this so it works with post, etc.
        // TODO proper error shit
        try {
            const result = await axios.post<Data>(`${apiURL}/${route}`, variables, {});

            console.log("res", result);

            setLoading(false);
            setData(result.data);

            return result;
        } catch (e) {
            // console.log(e, e.response);
            const errors = e.response.data.errors;
            setErrors(e.response.data.errors);
            if (form)
                form.setFields(errors.map((error: ResponseError) => ({ errors: [error.message], name: error.path })));
            throw e.response.data.errors;
        }
    };

    return [request, { data, errors, loading }];
};
