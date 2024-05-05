'use client';

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { PanelRightClose, Sparkle } from "lucide-react";
import { useEffect, useState } from "react";
import { ChatBubble } from "./ChatBubble";
import { ScrollArea } from "@/components/ui/scroll-area";
import { BarLoader } from "react-spinners";
import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

const BASE_URL = "https://vl-nat-sec-hackathon-may-2024.s3.us-east-2.amazonaws.com";

function getChats(telegram: any, twitter: any) {
    let res = [];
    for (let t of telegram) {
        res.push({
            message: t.translation,
            senderName: t.name,
            senderPicture: 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Default_pfp.svg/680px-Default_pfp.svg.png',
            attachment: BASE_URL + "/" + t.attachment_urls.split(',')[0]
        });
    }
    for (let t of twitter) {
        res.push({
            message: "",
            senderName: "",
            senderPicture: 'https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Default_pfp.svg/680px-Default_pfp.svg.png',
            attachment: t
        });
    }
    return res;
}

export function TLISide({ eventInfo, setSidebar }: any) {

    const [description, setDescription] = useState(eventInfo.description);
    const [chatValue, setChatValue] = useState('');
    const [insights, setInsights] = useState<any>([]);

    eventInfo.chats = getChats(eventInfo.telegram_posts, eventInfo.twitter_posts[0][1]);

    function onSend() {
        console.log("Sending message");
        setChatValue('');
    }

    useEffect(() => {

    const controller = new AbortController();
    const signal = controller.signal;

    fetch('http://10.1.60.171:8080/insights?id=' + eventInfo._id, { signal, method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id: eventInfo._id }) })
        .then(response => response.json())
        .then(data => {
            setInsights(JSON.parse(data.insights));
            console.log(data);
        })
        .catch(error => {
            if (error.name === 'AbortError') {
                console.log('Fetch aborted');
            } else {
                console.error('Fetch error:', error);
            }
        });

        return () => {
            controller.abort();
        };

    }, []);

    return (
        <div className="sidebar-container h-full">
    <div className="sidebar fixed inset-0 bg-black bg-opacity-50 z-40 flex justify-end" onClick={() => setSidebar(null)}>
        <div className="flex flex-col w-1/2 h-full bg-white p-5 overflow-auto z-50" onClick={(e) => e.stopPropagation()}>
            <Tabs defaultValue="event" className="h-full">
                <TabsList className="w-full">
                    <TabsTrigger value="event" className="px-4">Event</TabsTrigger>
                    <TabsTrigger value="chats" className="px-4">Chats</TabsTrigger>
                    <TabsTrigger value="insights" className="px-4">Insights</TabsTrigger>
                </TabsList>
                <TabsContent value="event" className="items-end">
                    <div className="flex flex-col overflow-auto flex-grow">
                        <h1 className="text-xl text-center my-5 font-semibold">{eventInfo.event}</h1>
                        <img src={eventInfo.image} className="mx-auto p-3" style={{ maxHeight: '200px', flexShrink: 0 }} />
                        <p className="text-center my-5 mx-10">{description}</p>
                    </div>
                    <div className="flex flex-col">
                        <div className="flex flex-row items-center justify-center space-x-2">
                            <Input value={chatValue} onChange={(e) => setChatValue(e.target.value)} type="text" placeholder="Ask anything..." className="flex-1" onKeyDown={event => {
                                if (event.key === "Enter") {
                                    onSend();
                                }
                            }} />
                            <Button onClick={onSend}>Send</Button>
                        </div>
                    </div>
                </TabsContent>
                <TabsContent value="chats">
                    <div className="flex flex-col flex-grow">
                        <ScrollArea>
                            {eventInfo.chats.map((chat: any, index: number) => (
                                <div key={index}>
                                    <ChatBubble key={index} message={chat.message} senderName={chat.senderName} senderImage={chat.senderPicture} attachment={chat.attachment} />
                                </div>
                            ))}
                        </ScrollArea>
                    </div>
                </TabsContent>
                <TabsContent value="insights">

                    {insights.length === 0 && (
                        <BarLoader className="mx-auto" />
                    )}
                    <div className="flex flex-col flex-grow h-full justify-start">

                    {insights && (
                        <div className="flex h-full flex-col items-start justify-start py-6">
                            {insights.map((insight: any, index: number) => (
                                <div key={index} className="flex items-center">
                                    <Sparkle className="mx-2 mr-4" size={40} />
                                    <Card>
                                        <CardHeader>
                                            <CardDescription className="my-3">{insight}</CardDescription>
                                        </CardHeader>
                                    </Card>
                                </div>
                            ))}
                        </div>
                    )}

                    </div>
                    <div className="flex flex-col flex-grow h-full items-center justify-center">
                        {!insights && (
                            <div>
                                <h1 className="text-xl my-3">Generating...</h1>
                                <BarLoader />
                            </div>
                        )}
                    </div>
                </TabsContent>
            </Tabs>
        </div>
    </div>
</div>

    )    
}
