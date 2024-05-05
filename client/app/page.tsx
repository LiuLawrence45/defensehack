'use client';

import { Card, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { EventTL } from "./EventTL";
import { Search } from "@/components/ui/SearchBar";
import { useState, useEffect } from "react";
import { ScrollArea } from "@/components/ui/scroll-area";
//import EarthModel from "./EarthModel";
import Globe from "react-globe.gl";


export default function Home() {

  const [searchTerm, setSearchTerm] = useState<string | null>(null);
  const [placeholder, setPlaceholder] = useState<string>('');
  const [sidebarContent, setSidebarContent] = useState<any>(null);

  function handleSearch(searchTerm: string) {
    console.log('set search term');
    setSearchTerm(searchTerm);
  }

  useEffect(() => {
    const phs = ['Tell me about the Baltimore Bridge Collapse', 'Tell me about the Russia-Ukraine War', 'Tell me about the Columbia protests'];
    let currInd = 0;
    setPlaceholder(phs[currInd] + '...');
    setInterval(() => {
      currInd++;
      currInd %= phs.length;
      setPlaceholder(phs[currInd] + '...');
    }, 3000)
  }, []);

  return (
    <div className="w-full h-full flex flex-col">
    {!searchTerm && (
      <div className="h-full flex flex-col justify-center items-center">
        <h1 className="font-semibold text-2xl m-2">Welcome to EightEye</h1>
        <p className="text-lg">Search for an event to get started</p>
      </div>
    )}
    <div className="container h-full w-full flex flex-row p-0 justify-start">
      <div className="h-full w-full flex flex-col justify-end">
        {searchTerm && (
        <ScrollArea className="h-full">
        {searchTerm && (
          <EventTL key={searchTerm} searchTerm={searchTerm} setSidebar={setSidebarContent} />
        )}
        </ScrollArea>
        )}
        <div className="w-full flex justify-center">
          <Search placeholder={placeholder} handleSearch={handleSearch} className="justify-center" />
        </div>
      </div>
      <div className="w-1 h-full bg-gray-100"></div>
      {sidebarContent}
    </div>
    </div>
  );
}
