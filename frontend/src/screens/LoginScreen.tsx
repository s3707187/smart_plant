import React, { useEffect, useState } from "react";
import { Form, Input, Button, Checkbox } from "antd";
import { getAccessToken, setAccessToken, setRefreshToken } from "../app/token";
import { ResponseData, usePost } from "../utils/apiHooks";

const layout = {
    labelCol: { span: 8 },
    wrapperCol: { span: 15 },
};
const tailLayout = {
    wrapperCol: { offset: 8, span: 15 },
};

interface LoginScreenProps {}
type Response = { access_token: string; refresh_token: string };

const LoginScreen: React.FC<LoginScreenProps> = (props: LoginScreenProps) => {
    const [Login, { data, loading, errors }] = usePost<Response>("login");

    const onFinish = async (values: any) => {
        console.log("Success:", values);

        const res = await Login({
            username: values.username,
            password: values.password,
        });

        await Promise.all([setRefreshToken(res.data.refresh_token), setAccessToken(res.data.access_token)]);
        console.log("PROMISE SETTLED");
    };

    const onFinishFailed = (errorInfo: any) => {
        console.log("Failed:", errorInfo);
    };

    return (
        <Form
            {...layout}
            name="basic"
            initialValues={{ remember: true }}
            onFinish={onFinish}
            onFinishFailed={onFinishFailed}
        >
            <Form.Item
                label="Username"
                name="username"
                rules={[{ required: true, message: "Please input your username!" }]}
            >
                <Input />
            </Form.Item>

            <Form.Item
                label="Password"
                name="password"
                rules={[{ required: true, message: "Please input your password!" }]}
            >
                <Input.Password />
            </Form.Item>

            <Form.Item {...tailLayout} name="remember" valuePropName="checked">
                <Checkbox>Remember me</Checkbox>
            </Form.Item>

            <Form.Item {...tailLayout}>
                <Button type="primary" htmlType="submit">
                    Submit
                </Button>
            </Form.Item>
        </Form>
    );
};

export default LoginScreen;
