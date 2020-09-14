import React, { useState } from "react";
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
    Borders,
    HighlightArea,
} from "react-vis";
import "react-vis/dist/style.css";

//Colors must be assigned statically to avoid problems with DiscreteLegend
var lightCol = "rgb(227,77,66)";
var moistureCol = "rgb(21,42,161)";
var humidityCol = "rgb(252,146,53)";
var tempCol = "rgb(77, 181, 255)";

interface HistoryVisualisationComponentProps {
    rawData: { date: Date; light: number; temp: number; humidity: number; moisture: number }[];
}

const HistoryVisualisationComponent: React.FC<HistoryVisualisationComponentProps> = (
    props: HistoryVisualisationComponentProps
) => {
    // const { rawData } = props;

    const rawData = [
        {
            date: "2019-09-26 03:41:03",
            light: "0.430988272",
            temp: "0.2214361872",
            humidity: "0.6340036421",
            moisture: "0.3197926486",
        },
        {
            date: "2019-10-05 08:20:19",
            light: "0.5059277718",
            temp: "0.5732436995",
            humidity: "0.3488765762",
            moisture: "0.7413857737",
        },
        {
            date: "2019-09-24 12:15:12",
            light: "0.3636736346",
            temp: "0.7539578363",
            humidity: "0.5433494084",
            moisture: "1.2013330024",
        },
        {
            date: "2019-10-11 01:47:46",
            light: "0.489443414",
            temp: "0.7076915569",
            humidity: "0.2216197106",
            moisture: "0.4643905524",
        },
        {
            date: "2019-09-15 00:42:51",
            light: "0.2597915631",
            temp: "0.1316016524",
            humidity: "0.6874563375",
            moisture: "0.2277765919",
        },
        {
            date: "2019-09-22 16:44:30",
            light: "0.799155468",
            temp: "0.2864362706",
            humidity: "0.6523071007",
            moisture: "0.5593172756",
        },
        {
            date: "2019-10-09 17:31:07",
            light: "0.5597587146",
            temp: "0.0862003878",
            humidity: "0.4164876689",
            moisture: "0.3791512726",
        },
        {
            date: "2019-09-26 05:05:07",
            light: "0.3605969993",
            temp: "0.2270091137",
            humidity: "0.5664242949",
            moisture: "0.3231399518",
        },
        {
            date: "2019-09-20 19:14:12",
            light: "0.1653390742",
            temp: "0.3934067561",
            humidity: "0.877180755",
            moisture: "0.4060110607",
        },
        {
            date: "2019-10-03 09:21:18",
            light: "0.8131513488",
            temp: "0.320669964",
            humidity: "0.6257401026",
            moisture: "0.3428963777",
        },
        {
            date: "2019-09-21 16:17:19",
            light: "0.4476761287",
            temp: "0.2698638064",
            humidity: "0.0558081062",
            moisture: "0.6062405625",
        },
        {
            date: "2019-10-05 03:12:24",
            light: "0.5292967673",
            temp: "0.6672563606",
            humidity: "0.1787336401",
            moisture: "0.2530660752",
        },
        {
            date: "2019-09-21 20:25:21",
            light: "0.5789194872",
            temp: "0.6913182428",
            humidity: "0.6235048574",
            moisture: "0.5427296725",
        },
        {
            date: "2019-09-28 04:16:59",
            light: "0.663530221",
            temp: "0.7440738371",
            humidity: "0.4225622232",
            moisture: "0.5764833831",
        },
        {
            date: "2019-10-02 18:54:23",
            light: "0.5133988484",
            temp: "0.5828441702",
            humidity: "0.5555287169",
            moisture: "0.6850242494",
        },
        {
            date: "2019-09-27 08:22:15",
            light: "0.583258617",
            temp: "0.7148953827",
            humidity: "0.1149391691",
            moisture: "0.531334449",
        },
        {
            date: "2019-10-01 02:21:16",
            light: "0.58644032",
            temp: "0.2282773187",
            humidity: "0.571403992",
            moisture: "0.2604550209",
        },
        {
            date: "2019-10-03 06:11:23",
            light: "0.3607455291",
            temp: "0.6265517394",
            humidity: "0.7089188594",
            moisture: "0.9038497856",
        },
        {
            date: "2019-09-22 15:09:27",
            light: "0.7580693389",
            temp: "0.6664798125",
            humidity: "0.8384471747",
            moisture: "0.5968479485",
        },
        {
            date: "2019-10-06 02:45:38",
            light: "0.529323814",
            temp: "0.2824449438",
            humidity: "0.3234727577",
            moisture: "0.3355279411",
        },
        {
            date: "2019-09-14 18:41:43",
            light: "0.3720555777",
            temp: "0.7733323978",
            humidity: "0.0062080021",
            moisture: "0.2023692301",
        },
        {
            date: "2019-09-29 12:09:39",
            light: "0.8511958263",
            temp: "0.1653076017",
            humidity: "0.5176004228",
            moisture: "0.379361329",
        },
        {
            date: "2019-09-26 21:48:49",
            light: "0.3390806152",
            temp: "0.2030156721",
            humidity: "0.8957116321",
            moisture: "0.7308064268",
        },
        {
            date: "2019-09-17 23:59:30",
            light: "0.6672958425",
            temp: "0.6981576932",
            humidity: "-0.0009363181",
            moisture: "0.4367591055",
        },
        {
            date: "2019-09-19 03:21:04",
            light: "0.4128541321",
            temp: "0.6418865973",
            humidity: "0.4341522021",
            moisture: "0.7864300464",
        },
        {
            date: "2019-09-17 11:43:39",
            light: "0.7346531827",
            temp: "0.4272332798",
            humidity: "0.4659552675",
            moisture: "0.381459744",
        },
        {
            date: "2019-10-10 17:50:55",
            light: "0.6674548381",
            temp: "0.3241292665",
            humidity: "0.5601306526",
            moisture: "0.4675411015",
        },
        {
            date: "2019-09-30 03:22:13",
            light: "0.5738470302",
            temp: "0.4341680216",
            humidity: "0.4433239915",
            moisture: "0.7530240842",
        },
        {
            date: "2019-10-01 04:32:33",
            light: "0.351330707",
            temp: "0.169015249",
            humidity: "0.1355146461",
            moisture: "0.3840795158",
        },
        {
            date: "2019-10-10 09:54:07",
            light: "0.4773715091",
            temp: "0.4175261454",
            humidity: "0.2863856178",
            moisture: "0.5531019396",
        },
        {
            date: "2019-09-13 00:14:24",
            light: "0.2058338731",
            temp: "0.3770735257",
            humidity: "0.7681638252",
            moisture: "0.1931698822",
        },
        {
            date: "2019-10-01 21:16:33",
            light: "0.4031581381",
            temp: "0.4910699256",
            humidity: "0.1885105653",
            moisture: "0.5364316434",
        },
        {
            date: "2019-10-05 10:55:06",
            light: "0.7982368151",
            temp: "0.5070379306",
            humidity: "0.6244276606",
            moisture: "0.427452629",
        },
        {
            date: "2019-09-24 03:29:55",
            light: "-0.127135359",
            temp: "0.2749977481",
            humidity: "0.480178497",
            moisture: "0.0867178504",
        },
        {
            date: "2019-10-03 08:09:35",
            light: "0.7618758207",
            temp: "0.3875685825",
            humidity: "0.4539951515",
            moisture: "0.3780938387",
        },
        {
            date: "2019-10-07 22:11:37",
            light: "0.2137048216",
            temp: "0.6129024613",
            humidity: "0.6621433796",
            moisture: "0.6073273636",
        },
        {
            date: "2019-10-07 18:23:10",
            light: "0.2875090578",
            temp: "0.5933018934",
            humidity: "0.4682575644",
            moisture: "0.5695998375",
        },
        {
            date: "2019-09-21 08:10:42",
            light: "0.5496103554",
            temp: "0.9433575614",
            humidity: "0.3369469478",
            moisture: "0.2577788576",
        },
        {
            date: "2019-09-13 23:18:37",
            light: "0.530207408",
            temp: "0.4008425126",
            humidity: "0.7536491832",
            moisture: "0.9698916977",
        },
        {
            date: "2019-09-17 18:26:20",
            light: "-0.206107098",
            temp: "0.123391674",
            humidity: "0.6998889932",
            moisture: "0.8581386762",
        },
        {
            date: "2019-09-21 00:47:26",
            light: "0.6850133387",
            temp: "0.7686755881",
            humidity: "0.2263642307",
            moisture: "0.6696624052",
        },
        {
            date: "2019-09-16 21:09:30",
            light: "0.4316440126",
            temp: "0.8245551627",
            humidity: "0.2333788797",
            moisture: "0.01120043",
        },
        {
            date: "2019-10-02 11:49:05",
            light: "0.470519907",
            temp: "0.58492578",
            humidity: "0.6791840494",
            moisture: "0.2233490968",
        },
        {
            date: "2019-09-27 00:54:07",
            light: "0.2466647348",
            temp: "0.5360622187",
            humidity: "0.611967225",
            moisture: "0.9017114939",
        },
        {
            date: "2019-09-20 07:12:40",
            light: "0.6385665525",
            temp: "0.452039979",
            humidity: "0.8396629642",
            moisture: "0.5102129462",
        },
        {
            date: "2019-10-01 03:00:17",
            light: "0.6965972286",
            temp: "0.4750960314",
            humidity: "0.6258506278",
            moisture: "0.5571883201",
        },
        {
            date: "2019-10-12 21:54:29",
            light: "0.6623840733",
            temp: "0.5826297003",
            humidity: "0.6294108068",
            moisture: "0.3924567333",
        },
        {
            date: "2019-09-24 19:53:22",
            light: "0.4565550073",
            temp: "0.492716925",
            humidity: "0.1766380468",
            moisture: "0.007765675",
        },
        {
            date: "2019-10-05 14:07:51",
            light: "0.2709191364",
            temp: "0.4637710224",
            humidity: "0.2131065852",
            moisture: "0.9671297874",
        },
        {
            date: "2019-10-08 06:33:18",
            light: "0.4182373031",
            temp: "0.2156953752",
            humidity: "0.6346080109",
            moisture: "0.5439124727",
        },
        {
            date: "2019-09-20 12:27:05",
            light: "0.5280507872",
            temp: "0.4772703151",
            humidity: "0.4634126314",
            moisture: "0.0406792074",
        },
        {
            date: "2019-09-16 01:09:35",
            light: "0.7110477196",
            temp: "0.3884285906",
            humidity: "0.6025955299",
            moisture: "1.019791466",
        },
        {
            date: "2019-09-28 09:05:51",
            light: "0.9458123277",
            temp: "0.368148892",
            humidity: "0.389408166",
            moisture: "0.24048897",
        },
        {
            date: "2019-10-08 12:17:57",
            light: "0.1550131254",
            temp: "0.4424344397",
            humidity: "0.7382019099",
            moisture: "0.4656655014",
        },
        {
            date: "2019-09-16 06:27:48",
            light: "0.6688053112",
            temp: "0.6016784145",
            humidity: "0.5322469213",
            moisture: "0.6783224091",
        },
        {
            date: "2019-10-07 19:44:07",
            light: "0.4844576937",
            temp: "0.4606013604",
            humidity: "0.7894637229",
            moisture: "0.2717908633",
        },
        {
            date: "2019-09-24 01:08:31",
            light: "0.2516294051",
            temp: "0.4495033833",
            humidity: "0.5753126257",
            moisture: "0.7821624627",
        },
        {
            date: "2019-10-05 21:57:08",
            light: "0.8234631619",
            temp: "0.2617342063",
            humidity: "0.293138407",
            moisture: "0.4854241269",
        },
        {
            date: "2019-09-15 19:17:00",
            light: "0.330135853",
            temp: "0.298439793",
            humidity: "0.5728391956",
            moisture: "0.4116034826",
        },
        {
            date: "2019-09-22 22:53:52",
            light: "0.3264693485",
            temp: "0.466135496",
            humidity: "0.4033272188",
            moisture: "0.3175263368",
        },
        {
            date: "2019-09-19 05:52:36",
            light: "0.4337182173",
            temp: "0.6913113306",
            humidity: "0.7391513524",
            moisture: "0.5301653182",
        },
        {
            date: "2019-10-08 01:32:43",
            light: "0.5476250498",
            temp: "0.9225833969",
            humidity: "0.4352868963",
            moisture: "0.0581124522",
        },
        {
            date: "2019-10-05 07:49:34",
            light: "0.7130901372",
            temp: "0.6033281111",
            humidity: "0.1502257303",
            moisture: "0.4840678128",
        },
        {
            date: "2019-09-28 23:40:31",
            light: "0.5010048118",
            temp: "0.6083609895",
            humidity: "0.5551385076",
            moisture: "0.5199704796",
        },
        {
            date: "2019-10-01 17:48:08",
            light: "0.41482831",
            temp: "0.5258178723",
            humidity: "0.6500926153",
            moisture: "0.32363908",
        },
        {
            date: "2019-10-07 18:40:30",
            light: "0.882740363",
            temp: "0.0721313171",
            humidity: "0.3949992127",
            moisture: "0.3673269346",
        },
        {
            date: "2019-10-02 08:42:19",
            light: "0.74428318",
            temp: "0.6511838734",
            humidity: "0.7404816811",
            moisture: "0.689006213",
        },
        {
            date: "2019-10-03 11:05:56",
            light: "0.5924063812",
            temp: "0.4713306702",
            humidity: "0.5957133153",
            moisture: "0.763739935",
        },
        {
            date: "2019-10-12 17:56:07",
            light: "0.6790570817",
            temp: "0.4266139315",
            humidity: "-0.1106404117",
            moisture: "0.5514120359",
        },
        {
            date: "2019-09-15 21:53:14",
            light: "0.4452593314",
            temp: "0.7902603393",
            humidity: "0.4769449545",
            moisture: "0.5248755373",
        },
        {
            date: "2019-09-24 02:45:40",
            light: "0.5034792832",
            temp: "0.6207143075",
            humidity: "0.5247262747",
            moisture: "0.1928661754",
        },
        {
            date: "2019-10-01 18:45:08",
            light: "0.5658515725",
            temp: "0.1780649848",
            humidity: "0.6508516305",
            moisture: "0.702538541",
        },
        {
            date: "2019-09-26 21:46:40",
            light: "0.2207080252",
            temp: "0.7220711707",
            humidity: "0.6049322169",
            moisture: "0.2735888077",
        },
        {
            date: "2019-10-09 16:16:01",
            light: "0.6176356739",
            temp: "0.2467055541",
            humidity: "0.3822964936",
            moisture: "0.462640841",
        },
        {
            date: "2019-09-14 13:01:31",
            light: "0.3092892202",
            temp: "-0.1871306819",
            humidity: "0.696861595",
            moisture: "0.2365360422",
        },
        {
            date: "2019-10-10 00:20:11",
            light: "0.1928311538",
            temp: "0.4286425874",
            humidity: "0.6294445004",
            moisture: "0.4746543672",
        },
        {
            date: "2019-09-15 00:42:17",
            light: "0.1887090903",
            temp: "0.7014610377",
            humidity: "0.8288207114",
            moisture: "0.6024169807",
        },
        {
            date: "2019-10-04 11:25:10",
            light: "0.3009251444",
            temp: "0.5106748349",
            humidity: "0.6277110125",
            moisture: "0.388478368",
        },
        {
            date: "2019-10-05 21:11:59",
            light: "0.5534728432",
            temp: "0.4803413814",
            humidity: "0.3412112543",
            moisture: "0.7978261983",
        },
        {
            date: "2019-10-03 14:11:34",
            light: "0.3561798169",
            temp: "0.4004688861",
            humidity: "0.4681201192",
            moisture: "0.2120717222",
        },
        {
            date: "2019-10-07 05:58:23",
            light: "0.5031892639",
            temp: "0.7230870113",
            humidity: "0.3256836406",
            moisture: "0.6623890627",
        },
        {
            date: "2019-10-11 23:44:38",
            light: "0.6529631074",
            temp: "0.5280867476",
            humidity: "0.5022644282",
            moisture: "0.7811902863",
        },
        {
            date: "2019-10-05 12:20:07",
            light: "0.4017701557",
            temp: "0.858833639",
            humidity: "0.360112792",
            moisture: "0.6248733441",
        },
        {
            date: "2019-09-27 12:04:55",
            light: "0.3489142247",
            temp: "0.5769883861",
            humidity: "0.4032621821",
            moisture: "1.0137960503",
        },
        {
            date: "2019-09-13 20:57:16",
            light: "0.6840072575",
            temp: "0.6780874867",
            humidity: "0.5689085094",
            moisture: "0.7806728676",
        },
        {
            date: "2019-09-25 15:00:45",
            light: "0.4767404737",
            temp: "0.7896674524",
            humidity: "0.5091872173",
            moisture: "0.4355996895",
        },
        {
            date: "2019-10-11 10:42:51",
            light: "0.0397602423",
            temp: "0.7530838953",
            humidity: "0.2606332641",
            moisture: "0.5315871934",
        },
        {
            date: "2019-09-16 17:06:11",
            light: "0.5770304353",
            temp: "0.4921684631",
            humidity: "0.7031453049",
            moisture: "0.2983949089",
        },
        {
            date: "2019-10-10 08:12:05",
            light: "0.6480474802",
            temp: "0.8601922682",
            humidity: "0.4098644187",
            moisture: "0.1933597402",
        },
        {
            date: "2019-09-16 04:39:12",
            light: "0.2702996833",
            temp: "0.6504291093",
            humidity: "0.5877177001",
            moisture: "0.4391673192",
        },
        {
            date: "2019-10-02 19:11:46",
            light: "0.283222165",
            temp: "0.0519834104",
            humidity: "0.5137285152",
            moisture: "0.3539683961",
        },
        {
            date: "2019-10-08 00:17:24",
            light: "0.2344589605",
            temp: "0.5475482696",
            humidity: "0.285889397",
            moisture: "0.3730344559",
        },
        {
            date: "2019-10-10 14:19:37",
            light: "0.4723471827",
            temp: "0.3858593857",
            humidity: "0.3603410893",
            moisture: "0.4029560535",
        },
        {
            date: "2019-10-12 01:13:28",
            light: "0.6229206948",
            temp: "0.5073177623",
            humidity: "0.5701530172",
            moisture: "0.8006506681",
        },
        {
            date: "2019-10-04 14:06:28",
            light: "0.323248891",
            temp: "0.7612135311",
            humidity: "0.3832620513",
            moisture: "0.0921838579",
        },
        {
            date: "2019-10-08 00:51:54",
            light: "0.3979739362",
            temp: "0.580478407",
            humidity: "0.3029942922",
            moisture: "-0.0539480905",
        },
        {
            date: "2019-09-30 08:24:38",
            light: "0.2945391337",
            temp: "0.6578555271",
            humidity: "0.3633705787",
            moisture: "0.4033387795",
        },
        {
            date: "2019-09-27 06:03:40",
            light: "0.1364854152",
            temp: "0.7870134662",
            humidity: "0.9138317356",
            moisture: "0.6931467379",
        },
        {
            date: "2019-10-08 03:40:18",
            light: "0.2269825221",
            temp: "0.4550357887",
            humidity: "0.7695307065",
            moisture: "0.475451777",
        },
        {
            date: "2019-09-12 11:27:08",
            light: "0.3782229686",
            temp: "0.5596802472",
            humidity: "0.7918380734",
            moisture: "0.4736500521",
        },
    ];
    const [lightVisible, setLightVisible] = useState<boolean>(false);
    const [humidityVisible, setHumidityVisible] = useState<boolean>(false);
    const [moistureVisible, setMoistureVisible] = useState<boolean>(false);
    const [temperatureVisible, setTemperatureVisible] = useState<boolean>(false);
    const [lastDrawLocation, setLastDrawLocation] = useState<HighlightArea | null>(null);

    const clickHandler = (item: unknown, i: number) => {
        //TODO
        // series[i].disabled = !series[i].disabled;
        // this.setState({ series });
        //console.log(i)
        console.log(item, i);
    };

    /*
@TODO: THINGS I DO NOT KNOW HOW TO PORT TO TYPESCRIPT
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
    rawData.sort(dateCompare);

    function toUseableData(
        rawData: [{ date: Date; light: number; temp: number; humidity: number; moisture: number }]
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

    //@ts-ignore
    const { lightSeries, humiditySeries, moistureSeries, tempSeries } = toUseableData(rawData);

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
                    //@ts-ignore
                    tickFormat={function tickFormat(d) {
                        const date = new Date(d);
                        //console.log(date.toISOString())
                        return date.toISOString().substr(5, 5);
                    }}
                />
                <YAxis />
            </XYPlot>
        </div>
    );
};

export default HistoryVisualisationComponent;
