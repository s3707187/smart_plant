import React, { useContext } from "react";
import { Typography, Popconfirm } from "antd";
import { useHistory } from "react-router-dom";

import AuthContex, { getRole, getUserID } from "../contexts/AuthContex";
import NotificationsContext from "../contexts/NotificationsContext";
import { useGet, usePost } from "../utils/apiHooks";

const { Link } = Typography;

interface PlantSettingsBodyComponentProps {
    plantID: number;
    maintainer?: string;
    topLoading?: boolean;
    refetch(): void;
}

const PlantSettingsBodyComponent: React.FC<PlantSettingsBodyComponentProps> = (
    props: PlantSettingsBodyComponentProps
) => {
    const history = useHistory();

    const { maintainer, plantID: plant_id, refetch, topLoading } = props;
    const { token } = useContext(AuthContex);
    const current_user = token && getUserID(token);

    const [DeletePlant] = usePost<{}, { plant_id: number }>("delete_plant");

    const deletePlant = async () => {
        await DeletePlant({ plant_id }).then(() => {
            history.push("/");
        });
    };

    const [RemovePlantMaintainer, { loading: removeLoading }] = usePost<
        {},
        { linked_user: string; plant_id: number; link_type: "plant_viewer" | "maintenance" }
    >("remove_plant_link");

    const [AddPlantMaintainer, { loading: addLoading }] = usePost<
        {},
        { user_to_link: string; user_link_type: string; plant_id: number }
    >("add_plant_link");

    const { refetchAll: refetch_notificaitons } = useContext(NotificationsContext);

    const toggleMaintenance = async () => {
        if (token && maintainer == undefined)
            await AddPlantMaintainer({
                user_to_link: getUserID(token),
                user_link_type: "maintenance",
                plant_id,
            });
        else if (maintainer != undefined) {
            await RemovePlantMaintainer({
                linked_user: maintainer,
                link_type: "maintenance",
                plant_id,
            });
        }
        refetch();
        refetch_notificaitons();
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

            {token && getRole(token) === "admin" && (
                <Link disabled={addLoading || removeLoading || topLoading} onClick={toggleMaintenance}>
                    {maintainer != undefined && maintainer === current_user
                        ? "Deassign admin from "
                        : "Assign yourself to "}
                    plant maintenance.
                </Link>
            )}
        </div>
    );
};

export default PlantSettingsBodyComponent;
