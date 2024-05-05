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
const BASE_URL = "https://vl-nat-sec-hackathon-may-2024.s3.us-east-2.amazonaws.com";

export function EventTL({ searchTerm, setSidebar }: any) {

    const [loaded, setLoaded] = useState(false);
    const [events, setEvents] = useState([]);
    const globeRef = useRef<any>(null);
    const [targetCoords, setTargetCoords] = useState<any>(null);

    useEffect(() => {
        const abortController = new AbortController(); // Create an instance of AbortController
        const signal = abortController.signal; // Obtain the signal to pass to fetch

        fetch('http://10.1.60.171:8080/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: searchTerm }),
            signal: signal // Pass the abort signal to fetch
        })
        .then(response => {
            if (response.ok) return response.json();
            throw new Error('Network response was not ok.');
        })
        .then(data => {
            console.log(data);
            setTargetCoords({
                lat: data[0].location.coordinates[1],
                lng: data[0].location.coordinates[0],
                altitude: 0.1
            });
            data.sort((a: any, b: any) => {
                if (a.time < b.time) return -1;
                if (a.time > b.time) return 1;
                return 0;
            });
            for (let event of data) {
                for (let chat of event.telegram_posts) {
                    if (chat.attachment_urls) {
                        event.image = BASE_URL + '/' + chat.attachment_urls.split(',')[0];
                        break;
                    }
                }
                if (!event.image && event.twitter_posts[0][1].length > 0) {
                    event.image = event.twitter_posts[0][1][0];
                }
                event.description = event.twitter_posts[0][0];
            }
            setTimeout(() => {
                setEvents(data);
                setLoaded(true);
            }, 3000);
        })
        .catch(error => {
            if (error.name !== 'AbortError') {
                console.error("Fetch error: ", error);
            }
        });

        setLoaded(false);

        return () => {
            abortController.abort(); // Cleanup function that aborts the fetch operation
        };
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

    console.log(events);

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
    
      {events.map((event, index) => {
        return <TLI key={index} eventInfo={event} setSidebar={setSidebar} />
      })}
      
      <p className="text-center text-gray-400">Now</p>
      
    </Timeline>
    </div>
    );

    return loaded ? timeline : loading;
}
