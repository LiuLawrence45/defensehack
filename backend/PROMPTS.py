TWITTER_PROMPT = """
Given the a context, generate a comma separated list of one or two word keywords that would be relevant to search for for this context.

For example:

Given the following context:

Un s-300 del ejército Ucraniano en la frontera con Rusia, fue destruído por un ataque aéreo ruso en Kharkov cerca de la frontera con #Rusia ,toda la tripulación pereció.
A Russian #S300 SAM system was destroyed near #Mariupol , - said the city's mayor's adviser Petro Andryushchenko. #Ukraine
According to him, the attack took place in the triangle between Kalchik, Granitnoye and Zareya.
Destruction of an enemy radar and S-300 launcher in the Kharkov area.
Russian intelligence and missile forces did an excellent job. Thanks to their well-coordinated work, the Ukrainian Nazis are minus another S-300 (launcher and radar), as well as personnel.
Show more
Excellent work of our reconnaissance and strike complex, mercilessly and non-stop destroying the enemy on the Belgorod border and in the Kharkov region.
This time, death from heaven overtook the 40V6M radar tower, the S-300 launcher and the personnel who serviced this equipment. This will happen to all our enemies sooner or later, there is no third option.

Generate the following keywords:

["s300","40V6M","Kharkov","Belgorod"]

Given this context:

{context}

Generate the following keywords:
"""

