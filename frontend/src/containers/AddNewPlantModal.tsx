import { Form, Modal, Input, Button } from "antd";
import { ModalProps } from "antd/es/modal";
import React from "react";
import { usePost } from "../utils/apiHooks";

interface AddNewPlantModalProps extends Pick<ModalProps, "visible" | "onCancel"> {
    onOk: () => void;
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
    const [CreatePlant] = usePost<{}, { plant_name: string; plant_health: string; plant_type: string }>(
        "register_plant",
        form
    );
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
                    .then(async (values) => {
                        await CreatePlant({
                            plant_health: "healthy",
                            plant_name: values.plant_name,
                            plant_type: values.plant_type,
                        });
                        onOk();
                        form.resetFields();
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
                initialValues={{ remember: true }}
                onFinish={onFinish}
                onFinishFailed={onFinishFailed}
            >
                <Form.Item
                    label="Plant Name"
                    name="plant_name"
                    rules={[{ required: true, message: "Please input the Plant Name!" }]}
                >
                    <Input />
                </Form.Item>
                <Form.Item
                    label="Plant Type"
                    name="plant_type"
                    rules={[{ required: true, message: "Please input the Plant ID!" }]}
                >
                    <Input />
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default AddNewPlantModal;
