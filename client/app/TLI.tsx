
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Timeline, TimelineConnector, TimelineContent, TimelineDot, TimelineItem, TimelineSeparator } from "@mui/lab";
import { PanelRightClose } from "lucide-react";

export function TLI({ setSidebar, eventInfo }: any) {

    function clickOnCard() {
        setSidebar( 
            <div className="sidebar-container">
            <div className="sidebar fixed inset-0 bg-black bg-opacity-50 z-40 flex justify-end" onClick={() => setSidebar(null)}>
        {/* Sidebar container that stops the click event from propagating */}
        <div className="w-1/2 bg-white p-5 overflow-auto z-50" onClick={(e) => e.stopPropagation()}>
            <PanelRightClose className="absolute right-5 top-5 cursor-pointer" onClick={() => setSidebar(null)} />
            <h1 className="text-xl text-center my-5 font-semibold">{eventInfo.title}</h1>
            <img src={eventInfo.image} alt="Baltimore Bridge" className="mx-auto p-5" />
            <p className="text-center my-5 mx-10">{eventInfo.description}</p>
        </div>
        </div>
        </div>
        );
    }

    return (
        <TimelineItem>
        <TimelineSeparator>
          <TimelineDot />
          <TimelineConnector />
        </TimelineSeparator>
        <TimelineContent>
            <Card className="bg-gray-50 flex items-center cp" onClick={clickOnCard}>
                <CardHeader>
                    <CardTitle>{eventInfo.title}</CardTitle>
                    <CardDescription>{eventInfo.date}</CardDescription>
                </CardHeader>
                <CardContent className="h-full p-0">
                    <img src={eventInfo.image} width={300} alt="Baltimore Bridge" className="my-auto" />
                </CardContent>
            </Card>
        </TimelineContent>
      </TimelineItem>
    )
}
