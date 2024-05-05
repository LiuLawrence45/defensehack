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

export function TLISide({ eventInfo, setSidebar }: any) {

    const [description, setDescription] = useState(eventInfo.description);
    const [chatValue, setChatValue] = useState('');
    const [insights, setInsights] = useState<any>([
            {
                title: "Look at bridge inspections",
                description: "Often, bridge collapses like this are caused by structural issues. Take a look at any documents for bridge inspections.",
            }
        ]);

    function onSend() {
        console.log("Sending message");
        setChatValue('');
    }

    useEffect(() => {

    const controller = new AbortController();
    const signal = controller.signal;

    fetch('/api/insights', { signal, method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ eventId: eventInfo.id }) })
        .then(response => response.json())
        .then(data => {
            setInsights(data.insights);
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
                        <h1 className="text-xl text-center my-5 font-semibold">{eventInfo.title}</h1>
                        <img src={eventInfo.image} alt="Baltimore Bridge" className="mx-auto p-3" style={{ maxHeight: '200px', flexShrink: 0 }} />
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
                                <div>
                                    <ChatBubble key={index} message={chat.message} senderName={chat.senderName} senderImage={chat.senderPicture} attachment={chat.attachment} />
                                </div>
                            ))}
                        </ScrollArea>
                    </div>
                </TabsContent>
                <TabsContent value="insights">
                    <div className="flex flex-col flex-grow h-full justify-start">
                        
                        {insights && (
                            <div className="flex h-full items-center justify-start py-6">
                                <Sparkle className="mx-2 mr-4" size={40} />
                                {insights.map((insight: any, index: number) => (
                                    <Card key={index}>
                                        <CardHeader>
                                            <CardTitle className="my-3">{insight.title}</CardTitle>
                                            <CardDescription>{insight.description}</CardDescription>
                                        </CardHeader>
                                    </Card>
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
