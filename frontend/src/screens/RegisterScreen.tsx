import React, { useState } from "react";
import { Form, Input, Tooltip, Cascader, Select, Row, Col, Checkbox, Button, AutoComplete, Layout } from "antd";
import { QuestionCircleOutlined } from "@ant-design/icons";
import { setAccessToken, setRefreshToken } from "../app/token";
import AddUserForm from "../containers/AddUserForm";
import { usePost } from "../utils/apiHooks";

const { Option } = Select;

const formItemLayout = {
    labelCol: {
        xs: { span: 24 },
        sm: { span: 8 },
    },
    wrapperCol: {
        xs: { span: 24 },
        sm: { span: 16 },
    },
};
const tailFormItemLayout = {
    wrapperCol: {
        xs: {
            span: 24,
            offset: 0,
        },
        sm: {
            span: 16,
            offset: 8,
        },
    },
};

interface RegisterProps {}

const RegisterScreen: React.FC<RegisterProps> = (props: RegisterProps) => {
    const [form] = Form.useForm();
    const [Register, { data, loading, errors }] = usePost<
        { refresh_token: string; access_token: string },
        {
            username: string;
            password: string;
            first_name: string;
            last_name: string;
            email: string;
        }
    >("register", form);

    const onFinish = async (values: any) => {
        console.log("Received values of form: ", values);
        try {
            const res = await Register({
                username: values.username,
                password: values.password,
                first_name: values.first_name,
                last_name: values.last_name,
                email: values.email,
            });

            await Promise.all([setRefreshToken(res.data.refresh_token), setAccessToken(res.data.access_token)]);
        } catch (e) {}
    };

    return (
        <Layout>
            <Layout.Content
                style={{
                    margin: 20,
                    display: "flex",
                    flexDirection: "column",
                    // alignItems: "center",
                    // justifyContent: "center",
                }}
            >
                <AddUserForm
                    onFinish={onFinish}
                    form={form}
                    formItemLayout={formItemLayout}
                    tailFormItemLayout={tailFormItemLayout}
                />
            </Layout.Content>
        </Layout>
    );
};

export default RegisterScreen;
