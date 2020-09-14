import React from "react";
//@ts-ignore
import {
    XYPlot,
    XAxis,
    YAxis,
    VerticalGridLines,
    HorizontalGridLines,
    LineSeries,
    AreaSeries,
    Highlight,
    DiscreteColorLegend,
    Borders
} from 'react-vis';
import "react-vis/dist/style.css";

//Colors must be assigned statically to avoid problems with DiscreteLegend
var lightCol = "rgb(227,77,66)"
var moistureCol = "rgb(21,42,161"
var humidityCol = "rgb(252,146,53)"
var tempCol = "rgb(77, 181, 255)"




interface HistoryVisualisationComponentProps {
    rawData: [{ date: string, light: string, temp: string, humidity: string, moisture: string }]
}

const HistoryVisualisationComponent: React.FC<HistoryVisualisationComponentProps> = (
    props: HistoryVisualisationComponentProps
) => {

    const rawData = props
    const { series, lastDrawLocation } = this.state;

    /*
    @TODO: THINGS I DO NOT KNOW HOW TO PORT TO TYPESCRIPT

    METHODS
    function clickHandler = (item, i) => {
        const { series } = this.state;
        series[i].disabled = !series[i].disabled;
        this.setState({ series });
        //console.log(i)
    };

    STATE
    
    state = {
        series: [
          { title: "Light", disabled: false, color: lightCol },
          { title: "Humidity", disabled: false, color: humidityCol },
          { title: "Moisture", disabled: false, color: moistureCol },
          { title: "Temperature", disabled: false, color: tempCol }
        ],
        lastDrawLocation: null,
      };

    
    
    */


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
    rawData.sort(dateCompare)

    function toUseableData(rawData) {
        var lightSeries = []
        var humiditySeries = []
        var moistureSeries = []
        var tempSeries = []

        for (let row of rawData) {
            //Datetime conversion
            let dt = row.date.split(/[- :]/);
            let date = new Date(Date.UTC(dt[0], dt[1] - 1, dt[2], dt[3], dt[4], dt[5]));
            lightSeries.push({ x: date, y: parseFloat(row.light) })
            humiditySeries.push({ x: date, y: parseFloat(row.humidity) })
            moistureSeries.push({ x: date, y: parseFloat(row.moisture) })
            tempSeries.push({ x: date, y: parseFloat(row.temp) })
        }
    }

    const { series, lastDrawLocation } = this.state;


    var allData = toUseableData(rawData)
    var lightData = allData[0]//.sort(dateCompare)
    var humidityData = allData[1]//.sort(dateCompare)
    var moistureData = allData[2]//.sort(dateCompare)
    var tempData = allData[3]//.sort(dateCompare)
    var firstDate = lightData[0].x
    var lastDate = lightData[lightData.length - 1].x

    const { series, lastDrawLocation } = this.state;


    return (

        <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
            <DiscreteColorLegend
                //@ts-ignore
                onItemClick={this.clickHandler}
                //colorType="literal"
                items={series}
                orientation="horizontal"
            />
            <XYPlot
                //TODO: Update width/height
                width={800}
                height={300}
                yDomain={[0, 1]}
                xType="time"
                animation
                xDomain={
                    //@ts-ignore
                    lastDrawLocation && [
                        //@ts-ignore
                        lastDrawLocation.left,
                        //@ts-ignore
                        lastDrawLocation.right
                    ]
                }
                //@ts-ignore
                yDomain={
                    //@ts-ignore
                    [0, 1]

                }>
                <VerticalGridLines />


                <AreaSeries
                    className="healthy-range"
                    color="rgba(114,210,172,0.8)"
                    data={[
                        //@ts-ignore
                        { x: lastDrawLocation == null ? firstDate : lastDrawLocation.left, y: 0.63, y0: 0.37 },
                        { x: lastDate, y: 0.63, y0: 0.37 }
                    ]}
                />
                <LineSeries
                    className="light"
                    color={lightCol}
                    opacity={series[0].disabled ? 0.1 : 1}
                    data={lightData}
                />
                <LineSeries
                    className="humidity"
                    color={humidityCol}
                    opacity={series[1].disabled ? 0.1 : 1}
                    data={humidityData}
                />
                <LineSeries
                    className="moisture"
                    color={moistureCol}
                    opacity={series[2].disabled ? 0.1 : 1}
                    data={moistureData}
                />
                <LineSeries
                    className="temp"
                    color={tempCol}
                    opacity={series[3].disabled ? 0.1 : 1}
                    data={tempData}
                />
                <Highlight
                    //@ts-ignore
                    onBrushEnd={area => this.setState({ lastDrawLocation: area })}
                    //@ts-ignore
                    onDrag={area => {
                        this.setState({
                            lastDrawLocation: {
                                //@ts-ignore
                                bottom: lastDrawLocation.bottom + (area.top - area.bottom),
                                //@ts-ignore
                                left: lastDrawLocation.left - (area.right - area.left),
                                //@ts-ignore
                                right: lastDrawLocation.right - (area.right - area.left),
                                //@ts-ignore
                                top: lastDrawLocation.top + (area.top - area.bottom)
                            }
                        });
                    }}
                />
                <Borders style={{ all: { fill: '#fff' } }} />
                <XAxis
                    tickTotal={10}
                    //@ts-ignore
                    tickFormat={function tickFormat(d) {
                        const date = new Date(d)
                        //console.log(date.toISOString())
                        return date.toISOString().substr(5, 5)
                    }}
                />
                <YAxis />
            </XYPlot>

        </div>
    );
};

export default HistoryVisualisationComponent;
