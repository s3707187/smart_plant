import React from "react";
import { useGet } from "../utils/apiHooks";

interface DashboardScreenProps {}

const DashboardScreen: React.FC<DashboardScreenProps> = (props: DashboardScreenProps) => {
    const { data, loading, errors } = useGet("dashboard");

    if (loading) {
        return <p>Loading ...</p>;
    } else if (errors) {
        return <p>Errors!</p>;
    }

    return null;
};

export default DashboardScreen;
