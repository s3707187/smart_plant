import React, { useState } from "react";
import PlantUserAccessComponent from "../components/PlantUserAccessComponent.native";
import PlantUserAccessInputComponent from "../components/PlantUserAccessInputComponent";
import { useGet, usePost } from "../utils/apiHooks";
import { Layout, Typography, Menu } from "antd";
import { CloseCircleOutlined } from "@ant-design/icons";

const { Title, Text, Link } = Typography;

interface PlantUsersContainerProps {
    plant_id: number;
}

const PlantUsersContainer: React.FC<PlantUsersContainerProps> = (props: PlantUsersContainerProps) => {
    const { plant_id } = props;

    const { data: member_data, errors: e, refetch } = useGet<string[], { plant_id: number }>("get_plant_members", {
        plant_id,
    });
    const [AddNewUser, { errors }] = usePost<
        unknown,
        {
            user_to_link: string;
            user_link_type: string;
            plant_id: number;
        }
    >("add_plant_link");

    const [RemoveUser, { errors: er }] = usePost<
        unknown,
        {
            linked_user: string;
            plant_id: number;
        }
    >("remove_plant_link");

    const [isAddingNewPerson, setAddingNewPerson] = useState<boolean>(false);
    const [name, setName] = useState("");

    // console.log("member", member_data, e);
    console.log(name);
    return (
        <div
            style={{
                margin: 20,
                display: "flex",

                flexDirection: "column",
                alignItems: "center",
                justifyContent: "center",
            }}
        >
            <Title level={2}>Access Controls</Title>
            {member_data &&
                member_data.map((linked_user) => (
                    <PlantUserAccessComponent
                        name={linked_user}
                        onDelete={() => {
                            RemoveUser({ linked_user, plant_id }).then(async () => {
                                refetch({ plant_id });
                            });
                        }}
                    />
                ))}
            {/*TODO change this so it works when we get 'access' field.*/}
            {!isAddingNewPerson && (
                <Link
                    onClick={() => {
                        setAddingNewPerson(true);
                    }}
                >
                    Add another user!
                </Link>
            )}
            {isAddingNewPerson && (
                <PlantUserAccessInputComponent
                    name={name}
                    errors={errors}
                    onChange={setName}
                    onCancel={() => {
                        setName("");
                        setAddingNewPerson(false);
                    }}
                    onDone={(user_to_link: string) => {
                        AddNewUser({ plant_id, user_link_type: "plant_viewer", user_to_link }).then(async () => {
                            await refetch({ plant_id });
                            setAddingNewPerson(false);
                            setName("");
                        });
                    }}
                />
            )}
        </div>
    );
};

export default PlantUsersContainer;
