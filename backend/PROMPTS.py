TWITTER_PROMPT = """
Given the a context, generate a comma separated list of one or two word keywords that would be relevant to search for for this context and are specific enough (ie, choose specific unique keywords, entities, or locations). Please make sure your queries are very targeted and will return relevant results. For example, if a location is abbreviated DPR, you should search for some sort of clarifying term (ie, Ukraine DPR) instead of just JPG because JPG is too ambigious. Or, if the example is relevant to russian, you should search ("russia" + something else) instead of just russia since russia is too broad.

Use the context and the description to disambiguate locations when possible. For example, in the context of ukraine, DPR refers to Donetsk People's republic (though you may want to just query Donetsk)

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
Given a list of text data related to the following event, generate a summary of the event in a bullet point format.

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

{context}

Context:

{data}

Generate the output:
"""