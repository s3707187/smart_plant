import React from "react";
import { Typography, Popconfirm } from "antd";
import { useHistory } from "react-router-dom";
import { usePost } from "../utils/apiHooks";

const { Link } = Typography;

interface PlantSettingsBodyComponentProps {
    plantID: number;
}

const PlantSettingsBodyComponent: React.FC<PlantSettingsBodyComponentProps> = (
    props: PlantSettingsBodyComponentProps
) => {
    const history = useHistory();
    const { plantID: plant_id } = props;

    const [DeletePlant] = usePost<{}, { plant_id: number }>("delete_plant");

    const deletePlant = async () => {
        await DeletePlant({ plant_id }).then(() => {
            history.push("/");
        });
    };

    return (
        <>
            <Popconfirm
                placement="left"
                title={"Are you sure you want to delete this plant?"}
                onConfirm={deletePlant}
                okText="Yes"
                cancelText="No"
            >
                <Link data-cy="delete_plant_confirm" type={"danger"}>Delete Plant</Link>
            </Popconfirm>
        </>
    );
};

export default PlantSettingsBodyComponent;
