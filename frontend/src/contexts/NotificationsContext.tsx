import React, { createContext } from "react";

export interface NotificationsContextProps {
    registerNotificationSubscriber(refetch_function: () => any): number;
    deregisterNotificationSubscriber(subscriber: number): void;
    refetchAll(): void;
}

export default React.createContext<NotificationsContextProps>({
    refetchAll: () => {},
    deregisterNotificationSubscriber: (subscriber: number) => {},
    registerNotificationSubscriber: (refetch_function: () => any): number => {
        return 0;
    },
});
