TWITTER_PROMPT = """
Given the a context, generate a comma separated list of one or two word keywords that would be relevant to search for for this context and are specific enough.

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

["s300","40V6M","Kharkov","Belgorod", "russian attack"]

Given this context:

{context}

Generate the following keywords:
"""

TWITTER_ANALYSIS = """
Given a tweet, determine if the tweet is directly relevant for the event and context below. Return only True or False

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

True

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

False

Given the following tweet:

{tweet}

Given the following context:

{context}

"""