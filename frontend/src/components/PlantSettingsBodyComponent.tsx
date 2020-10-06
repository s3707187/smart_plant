import React, { useContext } from "react";
import { Typography, Popconfirm } from "antd";
import { useHistory } from "react-router-dom";
import AuthContex, { getRole } from "../contexts/AuthContex";
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
    const { token } = useContext(AuthContex);

    const [DeletePlant] = usePost<{}, { plant_id: number }>("delete_plant");

    const deletePlant = async () => {
        await DeletePlant({ plant_id }).then(() => {
            history.push("/");
        });
    };

    return (
        <div style={{ display: "flex", flexDirection: "column" }}>
            <Popconfirm
                placement="left"
                title={"Are you sure you want to delete this plant?"}
                onConfirm={deletePlant}
                okText="Yes"
                cancelText="No"
            >
                <Link type={"danger"}>Delete Plant</Link>
            </Popconfirm>
            {token && getRole(token) === "admin" && <Link>Assign yourself to plant maintenance.</Link>}
        </div>
    );
};

export default PlantSettingsBodyComponent;
