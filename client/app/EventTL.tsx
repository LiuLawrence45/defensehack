'use client';

import { Timeline, TimelineConnector, TimelineContent, TimelineDot, TimelineItem, TimelineSeparator } from "@mui/lab";
import { useState, useEffect, useRef } from 'react';
import { BarLoader } from 'react-spinners';
import Bridge from "./baltimorebridge.webp";
import { TLI } from "./TLI";
import Globe from "react-globe.gl";
import World from "./world.jpg";

const eventInfo = {
    image: Bridge.src,
    title: "Baltimore Bridge an hour before event",
    description: "This photo was taken by an unknown photographer on Telegram about an hour before the bridge collapsed.",
    date: "Mar. 26, 2024 - 4:05PM",
    chats: [
        {
            "senderName": "Joe",
            "message": "Beautiful day, took some flicks of the bridge.",
            "attachment": Bridge.src,
            "senderPicture": "https://placehold.co/200x100"
        }
    ]
};

const events = [eventInfo, eventInfo, eventInfo, eventInfo, eventInfo, eventInfo];

export function EventTL({ searchTerm, setSidebar }: any) {

    const [loaded, setLoaded] = useState(false);
    const globeRef = useRef<any>(null);
    const [targetCoords, setTargetCoords] = useState<any>(null);

    useEffect(() => {
        console.log('search term changed');
        setLoaded(false);
        let t1 = setTimeout(() => {
            setTargetCoords({
                lat: 39.290383,
                lng: -76.612189,
                altitude: 0.1
            });
        }, 5000);
        let t2 = setTimeout(() => {
            setLoaded(true);
        }, 0);

        return () => {
            clearTimeout(t1);
            clearTimeout(t2);
        }
    }, [searchTerm]);

    useEffect(() => {

        let interval = setInterval(() => {
            if (!globeRef.current) return;
            let pov = globeRef.current.pointOfView();
            if (targetCoords) {
                console.log('target coords found')
                let newPov = {
                    lat: pov.lat + (targetCoords.lat - pov.lat) / 15,
                    lng: pov.lng + (targetCoords.lng - pov.lng) / 15,
                    altitude: pov.altitude + (targetCoords.altitude - pov.altitude) / 30
                };
                globeRef.current.pointOfView(newPov);
            } else {
                globeRef.current.pointOfView({
                    lat: pov.lat,
                    lng: pov.lng+0.4,
                    altitude: pov.altitude
                });
            }
        }, 20);

        return () => {
            clearInterval(interval);
        };

    }, [loaded, targetCoords]);

    let loading = (
        <div className="w-full flex justify-center">
            <BarLoader className="absolute" />
            <div className="absolute p-5" style={{top: '1%', bottom: '30%'}}>   
                <Globe 
                backgroundColor="#ffffff"
                globeImageUrl={World.src}
                enablePointerInteraction={false}
                ref={globeRef}
                />
            </div>
        </div>
    );

    let timeline = (
    <div className="h-full flex flex-col justify-center">
      <Timeline position="alternate">
    
      {events.map((eventInfo, index) => {
        return <TLI key={index} eventInfo={eventInfo} setSidebar={setSidebar} />
      })}
      
      <p className="text-center text-gray-400">Now</p>
      
    </Timeline>
    </div>
    );

    console.log(loaded);
    return loaded ? timeline : loading;
}
