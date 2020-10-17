import { Layout, Form, Button, Input } from "antd";
import React from "react";
import { usePost } from "../utils/apiHooks";

const layout = {
    labelCol: { span: 8 },
    wrapperCol: { span: 15 },
};
const tailLayout = {
    wrapperCol: { offset: 8, span: 15 },
};

interface ForgotPasswordScreenProps {}

const ForgotPasswordScreen: React.FC<ForgotPasswordScreenProps> = (props: ForgotPasswordScreenProps) => {
    const [form] = Form.useForm();

    const [ForgotPassword] = usePost<{}, { user_to_reset: string }>("reset_user_password", form);
    const onFinish = async (values: any) => {
        await ForgotPassword({ user_to_reset: values.user_to_reset });
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
                <Form form={form} onFinish={onFinish}>
                    <Form.Item
                        {...layout}
                        label="Username"
                        name="user_to_reset"
                        rules={[{ required: true, message: "Please input your username!" }]}
                    >
                        <Input />
                    </Form.Item>

                    <Form.Item {...tailLayout}>
                        <Button type="primary" htmlType="submit">
                            Submit
                        </Button>
                    </Form.Item>
                </Form>
            </Layout.Content>
        </Layout>
    );
};

export default ForgotPasswordScreen;
