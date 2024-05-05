from datetime import datetime

TWITTER_PROMPT = """
Given the a context, generate a comma separated list of one or two word keywords that would be relevant to search for for this context and are specific enough (ie, choose specific unique keywords, entities, or locations). Please make sure your queries are very targeted and will return relevant results. For example, if a location is abbreviated DPR, you should search for some sort of clarifying term (ie, Ukraine DPR) instead of just JPG because JPG is too ambigious. Or, if the example is relevant to russian, you should search ("russia" + something else) instead of just russia since russia is too broad.

Use the context and the description to disambiguate locations when possible. For example, in the context of ukraine, DPR refers to Donetsk People's republic (though you may want to just query Donetsk). However, also make sure you are not too specific, for example, if referring to a specific type of hardware or device, use the general term (ie, S300 instead of S300PS).

For example:

Given the following context:

Event description: Ukrainian military radars and launchers were destroyed in Kharkov near the Russain border
Event examples: 
Un s-300 del ejército Ucraniano en la frontera con Rusia, fue destruído por un ataque aéreo ruso en Kharkov cerca de la frontera con #Rusia ,toda la tripulación pereció.
A Russian #S300 SAM system was destroyed near #Mariupol , - said the city's mayor's adviser Petro Andryushchenko. #Ukraine
According to him, the attack took place in the triangle between Kalchik, Granitnoye and Zareya.
Destruction of an enemy radar and S-300 launcher in the Kharkov area.
Russian intelligence and missile forces did an excellent job. Thanks to their well-coordinated work, the Ukrainian Nazis are minus another S-300 (launcher and radar), as well as personnel.
Show more
Excellent work of our reconnaissance and strike complex, mercilessly and non-stop destroying the enemy on the Belgorod border and in the Kharkov region.
This time, death from heaven overtook the 40V6M radar tower, the S-300 launcher and the personnel who serviced this equipment. This will happen to all our enemies sooner or later, there is no third option.

Generate the following keywords:

keywords: ["s300","40V6M","Kharkov","Belgorod"]

Given the following context:

Event description: ⚡️Over the past 24 hours, Ukrainian armed forces have shelled residential areas of the DPR

Generate the following keywords:

keywords: ["DPR ukraine","ukraine shelling", "Donetsk shelling"]

Given this context:

{context}

Generate the following keywords:
"""

TWITTER_ANALYSIS = """
Given a tweet, determine if the tweet is directly relevant for the event and context below. Return only true or false

For example:

Given the following tweet:

💥 1 ru S300 air defense system was destroyed near currently occupied Ru 🇺🇦 Mariupol, 🇺🇦 Pyotr Andryushchenko
According to him, the attack was carried out in the triangle between Kalchik, Granitny & Zarya. “Last night it was very hot in the triangle. Hence

Given the following context:

Event description: Ukrainian military radars and launchers were destroyed in Kharkov near the Russain border
Event examples: 
Un s-300 del ejército Ucraniano en la frontera con Rusia, fue destruído por un ataque aéreo ruso en Kharkov cerca de la frontera con #Rusia ,toda la tripulación pereció.
A Russian #S300 SAM system was destroyed near #Mariupol , - said the city's mayor's adviser Petro Andryushchenko. #Ukraine
According to him, the attack took place in the triangle between Kalchik, Granitnoye and Zareya.
Destruction of an enemy radar and S-300 launcher in the Kharkov area.
Russian intelligence and missile forces did an excellent job. Thanks to their well-coordinated work, the Ukrainian Nazis are minus another S-300 (launcher and radar), as well as personnel.
Show more
Excellent work of our reconnaissance and strike complex, mercilessly and non-stop destroying the enemy on the Belgorod border and in the Kharkov region.
This time, death from heaven overtook the 40V6M radar tower, the S-300 launcher and the personnel who serviced this equipment. This will happen to all our enemies sooner or later, there is no third option.

Output:

relevant: true

Given the following tweet:

Flare and chaff dispensers have always existed. That’s why S300 missiles were landing in civi buildings from the start of the war. Two changes have taken place though (1) reduced tank for more explosives as max range not required (2) increased accuracy of gps against EW.

Given the following context:

Event description: Ukrainian military radars and launchers were destroyed in Kharkov near the Russain border
Event examples: 
Un s-300 del ejército Ucraniano en la frontera con Rusia, fue destruído por un ataque aéreo ruso en Kharkov cerca de la frontera con #Rusia ,toda la tripulación pereció.
A Russian #S300 SAM system was destroyed near #Mariupol , - said the city's mayor's adviser Petro Andryushchenko. #Ukraine
According to him, the attack took place in the triangle between Kalchik, Granitnoye and Zareya.
Destruction of an enemy radar and S-300 launcher in the Kharkov area.
Russian intelligence and missile forces did an excellent job. Thanks to their well-coordinated work, the Ukrainian Nazis are minus another S-300 (launcher and radar), as well as personnel.
Show more
Excellent work of our reconnaissance and strike complex, mercilessly and non-stop destroying the enemy on the Belgorod border and in the Kharkov region.
This time, death from heaven overtook the 40V6M radar tower, the S-300 launcher and the personnel who serviced this equipment. This will happen to all our enemies sooner or later, there is no third option.

Output:

relevant: false

Given the following tweet:

{tweet}

Given the following context:

{context}

Output:

"""

SUMMARIZE = """
Given a list of text data related to the following event, generate a summary of the event in a bullet point format. Be as specific as possible. When there is conflicting information, use the event information first, and then the context. If there is conflicting information in the context, use the one that is mentioned the most amount of times. Try to include any important/relevant information found in the context, such as numbers, make/models of weapons, etc. Also include any tangential information provided, such as other areas/things impacted, other parts of impacted, extent, 

For example, given the following event:

Event description: ⚡️Over the past 24 hours, Ukrainian armed forces have shelled residential areas of the DPR

Context:
Three civilians wounded in DPR during day as result of Ukraine’s shelling attacks https://t.co/RmP7v3SwIc
Blitzing news 🚨: Three civilians wounded in DPR during day as result of Ukraine’s shelling attacks - BreakingNews https://t.co/4Ah9h0DFet
Ukrainian troops fired 13 155-mm shells at Gorlovka and Donetsk, the DPR office at the Joint Center for Control and Coordination of Issues Related to War Crimes of Ukraine (JCCC) reported. “Shelling was recorded from the AFU in the direction: 08.45 - the settlement
@nour_odeh FYI, the only Palestine equivalent occupation in Ukraine is the attempted ethnic cleansing of S & E Ukraine's ethnic Russian/Russian speaking population by Kiev's racist fascist regime.It's the DPR & LPR regions being brutalised, & Russia came to to stop their genocide by Kiev
Three civilians wounded in DPR during day as result of Ukraine’s shelling attacks https://t.co/RmP7v3SwIc
Blitzing news 🚨: Three civilians wounded in DPR during day as result of Ukraine’s shelling attacks - BreakingNews https://t.co/4Ah9h0DFet
Another ukranian shelling of civilians in Donetsk region. In village, a house completly destroyed, woman is dead https://t.co/JKRyb7UFV9
Ukrainian troops fired 13 155-mm shells at Gorlovka and Donetsk, the DPR office at the Joint Center for Control and Coordination of Issues Related to War Crimes of Ukraine (JCCC) reported. “Shelling was recorded from the AFU in the direction: 08.45 - the settlement
The investigator is investigating the injury of a civilian in the west of Donetsk due to shelling by the Ukrainian Armed Forceshttps://t.co/23gvdxm194

Generate the following output:

Ukraine forces shell residential areas of DPR
- 3 civilians wounded in DPR
- 13 155-mm shells launched at Gorlovka and Donetsk
- Investigators are investigating civilian injuries

Given the following event:

Event details: Destruction of Radar and S-300 Launcher near Zmiev
Event descriptionL: The 40V6M universal tower with the 30N6 illumination and guidance radar, as well as the S-300PS air defense missile launcher of the Ukrainian army near the city of Zmiev in the Kharkov region, were destroyed. The footage captured the impact of an air-detonated missile on the tower and the subsequent detonation of solid fuel in the missile launcher

Context:

Generate the following output:
The destruction of the S300 south of Kharkov already paying dividends
Ukrainian supporters like NAFO will say this Iskander hit a "Decoy" or some other dumb shit. However, this is a full S300 Air defense  battery, including its radar.  #Ukraine #Russia  #Iskander #UkraineWar #UkraineWarNews #UkraineRussiaWar #NAFOfellas #UkraineFrontLines #Zelensky https://t.co/nflB7KNt8q
Destruction of a crucial Ukrainian S300 radar tower and launcher  The radar was already on fire when this Tornado-S missile hit https://t.co/rTQbvAgDx1
@MrClarkyofAxel @WarVehicle @DrazaM33 this one had ammunition given the explosion. In addition, these systems are relatively effective against Kh-101 type cruise missiles. This is a loss that Ukraine will not be able to replace.
Russian strike on a TEL and 30N6 engagement radar on a 40V6M mast, part of a Ukrainian S-300PS air defense system. Near Kostyantivka, Kharkiv Oblast, around 56 km from the border.  https://t.co/BaZMOe3JDF https://t.co/kEWIhQO3zL
#UkraineRussiaWar #Sevastopol #Avdeevka #Robotyne #Bakhmut   🇷🇺 Video of the defeat of the S-300PS under Zmiev by two operational-tactical quasi-ballistic missiles 9M723-1 of the Iskander-M complex.   The 30N6 illumination radar located on the 40V6M universal tower, designed to… https://t.co/0P5yVs8A8f
According to the Ministry of Defense, three Su-25 aircraft of the Ukrowehrmacht were destroyed at the Voznesensk airport in the Nikolaev region. In addition, a 40V6M illumination and guidance radar, a combat vehicle, a low-altitude detector and 3 S-300 air defense launchers were destroyed https://t.co/BZndzsBEhB
@squatsons &gt; Neither, in fact it was an S-300 and a 40V6M tower with 30N6 illumination radar.  All 3 were taking out in a single day.  1 S-300 was hit in one location in Kharkov.  1 Patriot hit in another location in Kharkov  1 NASAMS hit in another location in Kharkov.
#UkraineRussiaWar #Sevastopol #Avdeevka #Robotyne #Bakhmut   🇷🇺 Video of the defeat of the S-300PS under Zmiev by two operational-tactical quasi-ballistic missiles 9M723-1 of the Iskander-M complex.   The 30N6 illumination radar located on the 40V6M universal tower, designed to… https://t.co/0P5yVs8A8f

Generate the following output:

Russian forces destroy Ukrainian radar and S-300 launcher near Zmiev, Kharkov region
- 40V6M universal tower with 30N6 illumination and guidance radar destroyed
- 1 to 3 S-300 missle launchers were destroyed, and 1 Patriot and 1 NASAMS were affected
- Attack carried out with air-detonating missiles, either Iskander or Tornado-S
- Radar was located at coordinates 49.72241181360301, 36.36809829269529 near Kostyantsivka, about 56 km from Russian border
- Ukrainian personnel manning the equipment also killed in strike
- Loss of S-300 system will impact Ukraine's ability to defend against Russian cruise missiles like Kh-101

Given the following event:

{context}

Context:

{data}

Generate the output:
"""

EXTRACT_EVENT = """
Given a text, extract the location of the event, and the event description, and the word-for-word exact snippets from the given context that are relevant and not redundant. Return the list of strings as a properly formatted list for context.
There may be noise or irrelevant context provided. Based on the surrounding context, you can ignore certain information

For example, given this text:

🏍In Evpatoria, a motorcyclist flew into a road fence and died. As reported by the State Traffic Safety Inspectorate of the Ministry of Internal Affairs of the Republic of Kazakhstan, on March 27, on the Simferopol-Evpatoria highway, an 18-year-old Suzuki motorcycle driver did not choose a safe speed when rounding the road, which is why he crashed into a road fence. He died from the injuries he received at the scene of the accident.All the circumstances of what happened are now being clarified. Photo: State Traffic Safety Inspectorate of the Ministry of Internal Affairs of the Republic of Kazakhstan@crimea24new
Similar text at index 1238:
An 18-year-old motorcyclist died in an accident near Evpatoria. On the night of March 27, the driver of a Suzuki motorcycle, on the Simferopol-Evpatoria road from the city of Saki, lost control and ran into a metal fence.The motorcycle driver died at the scene of the accident from his injuries.State Traffic Inspectorate of Crimea
Similar text at index 2425:
🏍In Evpatoria, a motorcyclist flew into a road fence and died. As reported by the State Traffic Safety Inspectorate of the Ministry of Internal Affairs of the Republic of Kazakhstan, on March 27, on the Simferopol-Evpatoria highway, an 18-year-old Suzuki motorcycle driver did not choose a safe speed when rounding the road, which is why he crashed into a road fence. He died from the injuries he received at the scene of the accident.All the circumstances of what happened are now being clarified. Photo: State Traffic Safety Inspectorate of the Ministry of Internal Affairs for the Republic of Crimea 24 |@tvcrimea24
Similar text at index 5138:
An 18-year-old Suzuki motorcycle driver died at night on the Simferopol-Evpatoria highway. The young man lost control and crashed into a fence

Return:

location: Simferopol-Evpatoria highway
event: 18-year-old Suzuki motorcycle driver dies after losing control and crashing into fence on highway near Evpatoria
context: ["In Evpatoria, a motorcyclist flew into a road fence and died. As reported by the State Traffic Safety Inspectorate of the Ministry of Internal Affairs of the Republic of Kazakhstan, on March 27, on the Simferopol-Evpatoria highway, an 18-year-old Suzuki motorcycle driver did not choose a safe speed when rounding the road, which is why he crashed into a road fence. He died from the injuries he received at the scene of the accident.All the circumstances of what happened are now being clarified. Photo: State Traffic Safety Inspectorate of the Ministry of Internal Affairs for the Republic of Crimea 24 |@tvcrimea24"]

Given: 

{context}

Return:
"""


QUERY_PROMPT = """
Given a natural language query, decompose the query into a structured query object with the following fields:

start_date: datetime
end_date: datetime
location: str
topic: str

If not start/end date is passed, return the past year. Today is {date}

For example, given this query:

Find everything happening in Ukraine over the past 2 days

Return:

start_date: 2024-02-28T00:00:00.000Z
end_date: 2024-03-01T00:00:00.000Z
location: Ukraine
topic: ukraine

Given this query:

What has happened with SP300 missles in Ukraine?

Return:

start_date: 2023-05-04T00:00:00.000Z
end_date: 2024-05-04T00:00:00.000Z
location: Ukraine
topic: sp300 missiles

Given this query:

{context}

Return:

""".replace("date", datetime.now().strftime("%Y-%m-%d"))

