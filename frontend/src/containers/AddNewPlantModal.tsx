import { Form, Modal, Input, Button } from "antd";
import { ModalProps } from "antd/es/modal";
import React from "react";

interface AddNewPlantModalProps extends Pick<ModalProps, "visible" | "onCancel"> {
    onOk: (plantName: string, plantPassword: string) => void;
}

const layout = {
    labelCol: { span: 8 },
    wrapperCol: { span: 16 },
};
const tailLayout = {
    wrapperCol: { offset: 8, span: 16 },
};

const AddNewPlantModal: React.FC<AddNewPlantModalProps> = (props: AddNewPlantModalProps) => {
    const { visible, onOk, onCancel } = props;
    const [form] = Form.useForm();
    const onFinish = (values: any) => {
        console.log("Success:", values);
    };

    const onFinishFailed = (errorInfo: any) => {
        console.log("Failed:", errorInfo);
    };

    return (
        <Modal
            title="Add a new Plant"
            visible={visible}
            okText={"Add"}
            onOk={() =>
                form
                    .validateFields()
                    .then((values) => {
                        form.resetFields();
                        onOk("", "");
                    })
                    .catch((info) => {
                        console.log("Validate Failed:", info);
                    })
            }
            onCancel={onCancel}
        >
            <Form
                form={form}
                {...layout}
                name="basic"
                initialValues={{ remember: true }}
                onFinish={onFinish}
                onFinishFailed={onFinishFailed}
            >
                <Form.Item
                    label="Plant ID"
                    name="plant_id"
                    rules={[{ required: true, message: "Please input the Plant ID!" }]}
                >
                    <Input />
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default AddNewPlantModal;
