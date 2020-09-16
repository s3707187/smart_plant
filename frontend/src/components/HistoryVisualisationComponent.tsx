import React, { useState } from "react";
import {
    XYPlot,
    XAxis,
    YAxis,
    VerticalGridLines,
    LineSeries,
    AreaSeries,
    Highlight,
    DiscreteColorLegend,
    Borders,
    HighlightArea,
} from "react-vis";
import "react-vis/dist/style.css";

//Colors must be assigned statically to avoid problems with DiscreteLegend
const lightCol = "rgb(227,77,66)";
const moistureCol = "rgb(21,42,161)";
const humidityCol = "rgb(252,146,53)";
const tempCol = "rgb(77, 181, 255)";

interface HistoryVisualisationComponentProps {
    rawData: { date: Date; light: number; temp: number; humidity: number; moisture: number }[];
}

const HistoryVisualisationComponent: React.FC<HistoryVisualisationComponentProps> = (
    props: HistoryVisualisationComponentProps
) => {
    const { rawData } = props;

    const [lightVisible, setLightVisible] = useState<boolean>(false);
    const [humidityVisible, setHumidityVisible] = useState<boolean>(false);
    const [moistureVisible, setMoistureVisible] = useState<boolean>(false);
    const [temperatureVisible, setTemperatureVisible] = useState<boolean>(false);
    const [lastDrawLocation, setLastDrawLocation] = useState<HighlightArea | null>(null);

    const clickHandler = (item: { title: string; disabled: boolean; color: string }, i: number) => {
        const { title } = item;

        if (title === "Light") {
            setLightVisible(!lightVisible);
        } else if (title === "Temperature") {
            setTemperatureVisible(!temperatureVisible);
        } else if (title === "Humidity") {
            setHumidityVisible(!humidityVisible);
        } else if (title === "Moisture") {
            setMoistureVisible(!moistureVisible);
        }
    };

    // Modified from https://stackoverflow.com/questions/1129216/sort-array-of-objects-by-string-property-value
    //@ts-ignore
    function dateCompare(a, b) {
        if (a.date < b.date) {
            return -1;
        }
        if (a.date > b.date) {
            return 1;
        }
        return 0;
    }
    rawData.sort(dateCompare);

    function toUseableData(
        rawData: { date: Date; light: number; temp: number; humidity: number; moisture: number }[]
    ) {
        const lightSeries: { x: Date; y: number }[] = [];
        const humiditySeries: { x: Date; y: number }[] = [];
        const moistureSeries: { x: Date; y: number }[] = [];
        const tempSeries: { x: Date; y: number }[] = [];

        for (let row of rawData) {
            const { date, light, moisture, humidity, temp } = row;
            lightSeries.push({ x: date, y: light });
            humiditySeries.push({ x: date, y: humidity });
            moistureSeries.push({ x: date, y: moisture });
            tempSeries.push({ x: date, y: temp });
        }

        return { lightSeries, humiditySeries, moistureSeries, tempSeries };
    }

    const { lightSeries, humiditySeries, moistureSeries, tempSeries } = toUseableData(rawData);

    // TODO no data here will throw error
    const firstDate = lightSeries[0].x;
    const lastDate = lightSeries[lightSeries.length - 1].x;

    return (
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <DiscreteColorLegend
                //@ts-ignore
                onItemClick={clickHandler}
                //colorType="literal"
                items={[
                    { title: "Light", disabled: lightVisible, color: lightCol },
                    { title: "Humidity", disabled: humidityVisible, color: humidityCol },
                    { title: "Moisture", disabled: moistureVisible, color: moistureCol },
                    { title: "Temperature", disabled: temperatureVisible, color: tempCol },
                ]}
                orientation="horizontal"
            />

            <XYPlot
                width={800}
                height={300}
                yDomain={[0, 1]}
                xType="time"
                animation
                xDomain={lastDrawLocation && [lastDrawLocation.left, lastDrawLocation.right]}
            >
                <VerticalGridLines />

                <AreaSeries
                    className="healthy-range"
                    color="rgba(114,210,172,0.8)"
                    // @ts-ignore
                    data={[
                        //@ts-ignore
                        { x: lastDrawLocation == null ? firstDate : lastDrawLocation.left, y: 0.63, y0: 0.37 },
                        { x: lastDate, y: 0.63, y0: 0.37 },
                    ]}
                />
                <LineSeries
                    className="light"
                    color={lightCol}
                    opacity={lightVisible ? 0.1 : 1}
                    // @ts-ignore
                    data={lightSeries}
                />
                <LineSeries
                    className="humidity"
                    color={humidityCol}
                    opacity={humidityVisible ? 0.1 : 1}
                    // @ts-ignore
                    data={humiditySeries}
                />
                <LineSeries
                    className="moisture"
                    color={moistureCol}
                    opacity={moistureVisible ? 0.1 : 1}
                    // @ts-ignore
                    data={moistureSeries}
                />
                <LineSeries
                    className="temp"
                    color={tempCol}
                    opacity={temperatureVisible ? 0.1 : 1}
                    // @ts-ignore
                    data={tempSeries}
                />
                <Highlight
                    onBrushEnd={setLastDrawLocation}
                    onDrag={(area) => {
                        if (area != null && lastDrawLocation != null) {
                            setLastDrawLocation({
                                //@ts-ignore
                                bottom: lastDrawLocation.bottom + (area.top - area.bottom),
                                //@ts-ignore
                                left: lastDrawLocation.left - (area.right - area.left),
                                //@ts-ignore
                                right: lastDrawLocation.right - (area.right - area.left),
                                //@ts-ignore
                                top: lastDrawLocation.top + (area.top - area.bottom),
                            });
                        }
                    }}
                />
                <Borders style={{ all: { fill: "#fff" } }} />
                <XAxis
                    tickTotal={10}
                    tickFormat={(d) => {
                        const date = new Date(d);
                        return date.toISOString().substr(5, 5);
                    }}
                />
                <YAxis />
            </XYPlot>
        </div>
    );
};

export default HistoryVisualisationComponent;
