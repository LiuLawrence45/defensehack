
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Timeline, TimelineConnector, TimelineContent, TimelineDot, TimelineItem, TimelineSeparator } from "@mui/lab"
import { TLISide } from "./TLISide";

export function TLI({ setSidebar, eventInfo }: any) {

    function clickOnCard() {
        setSidebar(
            <TLISide eventInfo={eventInfo} setSidebar={setSidebar} />
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
