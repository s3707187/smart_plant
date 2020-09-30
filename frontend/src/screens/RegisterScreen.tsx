import React, { useState } from "react";
import { Form, Input, Tooltip, Cascader, Select, Row, Col, Checkbox, Button, AutoComplete, Layout } from "antd";
import { QuestionCircleOutlined } from "@ant-design/icons";
import { setAccessToken, setRefreshToken } from "../app/token";
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
                <Form
                    style={{ padding: 13 }}
                    {...formItemLayout}
                    form={form}
                    name="register"
                    onFinish={onFinish}
                    initialValues={{
                        residence: ["zhejiang", "hangzhou", "xihu"],
                        prefix: "86",
                    }}
                    scrollToFirstError
                >
                    <Form.Item
                        name="email"
                        label="E-mail"
                        rules={[
                            {
                                type: "email",
                                message: "The input is not valid E-mail!",
                            },
                            {
                                required: true,
                                message: "Please input your E-mail!",
                            },
                        ]}
                    >
                        <Input />
                    </Form.Item>

                    <Form.Item
                        name="username"
                        label="Username"
                        rules={[
                            {
                                required: true,
                                message: "Please input your username!",
                            },
                        ]}
                    >
                        <Input />
                    </Form.Item>

                    <Form.Item
                        name="password"
                        label="Password"
                        rules={[
                            {
                                required: true,
                                message: "Please input your password!",
                            },
                        ]}
                        hasFeedback
                    >
                        <Input.Password />
                    </Form.Item>

                    <Form.Item
                        name="confirm"
                        label="Confirm Password"
                        dependencies={["password"]}
                        hasFeedback
                        rules={[
                            {
                                required: true,
                                message: "Please confirm your password!",
                            },
                            ({ getFieldValue }) => ({
                                validator(rule, value) {
                                    if (!value || getFieldValue("password") === value) {
                                        return Promise.resolve();
                                    }
                                    return Promise.reject("The two passwords that you entered do not match!");
                                },
                            }),
                        ]}
                    >
                        <Input.Password />
                    </Form.Item>

                    <Form.Item
                        name="first_name"
                        label="Given Name"
                        rules={[{ required: true, message: "Please input your given name!", whitespace: true }]}
                    >
                        <Input />
                    </Form.Item>
                    <Form.Item
                        name="last_name"
                        label="Family Name"
                        rules={[{ required: true, message: "Please input your family name!", whitespace: true }]}
                    >
                        <Input />
                    </Form.Item>

                    <Form.Item
                        name="agreement"
                        valuePropName="checked"
                        rules={[
                            {
                                validator: (_, value) =>
                                    value ? Promise.resolve() : Promise.reject("Should accept agreement"),
                            },
                        ]}
                        {...tailFormItemLayout}
                    >
                        <Checkbox>
                            I have read the <a href="">agreement</a>
                        </Checkbox>
                    </Form.Item>
                    <Form.Item {...tailFormItemLayout}>
                        <Button type="primary" htmlType="submit">
                            Register
                        </Button>
                    </Form.Item>
                </Form>
            </Layout.Content>
        </Layout>
    );
};

export default RegisterScreen;
