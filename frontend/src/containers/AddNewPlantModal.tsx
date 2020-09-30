import { Form, Modal, Input, Button, Select } from "antd";
import { ModalProps } from "antd/es/modal";
import React from "react";
import { usePost } from "../utils/apiHooks";

interface AddNewPlantModalProps extends Pick<ModalProps, "visible" | "onCancel"> {
    onOk: () => void;
    role: "admin" | "user" | undefined;
}

const layout = {
    labelCol: { span: 8 },
    wrapperCol: { span: 16 },
};
const tailLayout = {
    wrapperCol: { offset: 8, span: 16 },
};

const AddNewPlantModal: React.FC<AddNewPlantModalProps> = (props: AddNewPlantModalProps) => {
    const { visible, onOk, onCancel, role } = props;
    const [form] = Form.useForm();
    const [CreatePlant] = usePost<
        {},
        { plant_name: string; plant_health: string; plant_type: string; plant_owner?: string }
    >("register_plant", form);
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
                            ...values,
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
                {role === "admin" && (
                    <Form.Item
                        label="Plant Owner"
                        name="plant_owner"
                        rules={[{ required: true, message: "Please input the user who will own this plant!" }]}
                    >
                        <Input />
                    </Form.Item>
                )}
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
                    rules={[{ required: true, message: "Please select a plant type!" }]}
                >
                    <Select placeholder="Select a option and change input text above">
                        <Select.Option value="Cactus type">Cactus type</Select.Option>
                        <Select.Option value="Flowering type">Flowering type</Select.Option>
                        <Select.Option value="Foliage type">Foliage type</Select.Option>
                    </Select>
                </Form.Item>
            </Form>
        </Modal>
    );
};

export default AddNewPlantModal;
