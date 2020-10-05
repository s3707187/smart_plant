import React, { useEffect, useState } from "react";
import { Form, Input, Button, Checkbox, Layout } from "antd";
import { getAccessToken, setAccessToken, setRefreshToken } from "../app/token";
import { ResponseData, ResponseError, usePost } from "../utils/apiHooks";

const layout = {
    labelCol: { span: 8 },
    wrapperCol: { span: 15 },
};
const tailLayout = {
    wrapperCol: { offset: 8, span: 15 },
};

interface LoginScreenProps { }
type Response = { access_token: string; refresh_token: string };

const LoginScreen: React.FC<LoginScreenProps> = (props: LoginScreenProps) => {
    const [form] = Form.useForm();
    const [Login, { data, loading, errors }] = usePost<Response>("login", form);

    const onFinish = async (values: any) => {
        console.log("Success:", values);
        try {
            const res = await Login({
                username: values.username,
                password: values.password,
            });
            await Promise.all([setRefreshToken(res.data.refresh_token), setAccessToken(res.data.access_token)]);
        } catch (e) { }

        console.log("PROMISE SETTLED");
    };

    const onFinishFailed = (errorInfo: any) => {
        console.log("Failed:", errorInfo);
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
                <Form
                    {...layout}
                    style={{ padding: 13 }}
                    form={form}
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
                        <Button data-cy="test" type="primary" htmlType="submit">
                            Submit
                        </Button>
                    </Form.Item>
                </Form>
            </Layout.Content>
        </Layout>
    );
};

export default LoginScreen;
