import React from "react";
import { Form, Input, Checkbox, Button } from "antd";
import { FormProps } from "antd/es/form";

interface AddUserFormProps extends FormProps {
    onFinish(values: any): void;
    tailFormItemLayout?: unknown;
    formItemLayout?: unknown;
}

const AddUserForm: React.FC<AddUserFormProps> = (props: AddUserFormProps) => {
    const { onFinish, tailFormItemLayout, formItemLayout, ...formProps } = props;

    return (
        <Form
            style={{ padding: 13 }}
            {...formProps}
            {...formItemLayout}
            name="register"
            onFinish={onFinish}
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
    );
};

export default AddUserForm;
