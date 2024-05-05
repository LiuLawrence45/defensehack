'use client';

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { PanelRightClose } from "lucide-react";
import { useState } from "react";

export function TLISide({ eventInfo, setSidebar }: any) {

    const [description, setDescription] = useState(eventInfo.description);
    const [chatValue, setChatValue] = useState('');

    function onSend() {
        console.log("Sending message");
        setChatValue('');
    }

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

            </Tabs>
        </div>
    </div>
</div>

    )    
}
