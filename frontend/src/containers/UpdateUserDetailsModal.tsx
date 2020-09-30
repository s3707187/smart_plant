import React from "react";
import { Modal, Form, Input } from "antd";
import { ModalProps } from "antd/es/modal";
import { usePost } from "../utils/apiHooks";

interface UpdateUserDetailsProps extends Pick<ModalProps, "visible" | "onCancel"> {
    onOk: () => void;
    initialValues?: {
        first_name: string;
        last_name: string;
        email: string;
    };
    username: string;
}

const layout = {
    labelCol: { span: 8 },
    wrapperCol: { span: 16 },
};
const tailLayout = {
    wrapperCol: { offset: 8, span: 16 },
};

const UpdateUserDetailsModal: React.FC<UpdateUserDetailsProps> = (props: UpdateUserDetailsProps) => {
    const { visible, onOk, onCancel, initialValues, username } = props;
    const [form] = Form.useForm();
    const [UpdateUser] = usePost<
        {},
        { username: string; password: string; email: string; first_name: string; last_name: string }
    >("update_user_details", form);
    const onFinish = (values: any) => {
        console.log("Success:", values);
    };

    const onFinishFailed = (errorInfo: any) => {
        console.log("Failed:", errorInfo);
    };

    return (
        <Modal
            title="Update your user details"
            visible={visible}
            okText={"Update"}
            onOk={() =>
                form
                    .validateFields()
                    .then(async (values) => {
                        await UpdateUser({
                            password: values.password,
                            first_name: values.first_name,
                            last_name: values.last_name,
                            email: values.email,
                            username,
                        });
                        onOk();
                        // form.resetFields();
                    })
                    .catch((info) => {
                        console.log("Validate Failed:", info);
                    })
            }
            onCancel={(e) => {
                form.resetFields();
                if (onCancel) onCancel(e);
            }}
        >
            <Form
                form={form}
                {...layout}
                name="basic"
                initialValues={initialValues}
                onFinish={onFinish}
                onFinishFailed={onFinishFailed}
            >
                <Form.Item
                    label="Given Name"
                    name="first_name"
                    rules={[{ required: true, message: "Please input your given name!" }]}
                >
                    <Input />
                </Form.Item>
                <Form.Item
                    label="Family Name"
                    name="last_name"
                    rules={[{ required: true, message: "Please input the family Name!" }]}
                >
                    <Input />
                </Form.Item>

                <Form.Item
                    name="email"
                    label="email"
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
                <Form.Item name="password" label="Password" rules={[]} hasFeedback>
                    <Input.Password />
                </Form.Item>
                <Form.Item
                    name="confirm"
                    label="Confirm Password"
                    dependencies={["password"]}
                    hasFeedback
                    rules={[
                        ({ getFieldValue }) => ({
                            validator(rule, value) {
                                if ((!value && !getFieldValue("password")) || getFieldValue("password") === value) {
                                    return Promise.resolve();
                                }
                                return Promise.reject("The two passwords that you entered do not match!");
                            },
                        }),
                    ]}
                >
                    <Input.Password />
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default UpdateUserDetailsModal;
