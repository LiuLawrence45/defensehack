from langchain_core.prompts import ChatPromptTemplate

ENTITY_PROMPT = """
                                                 

Given content, extract all notable events mentioned. Return in a dictionary format as such:

[
    {{
        "event": "event_name",
        "description": "description_of_event",
        "location": "location_of_event"
                                                 
    }},
    {{
        "event": "event_name",
        "description": "description_of_event",
        "location": "location_of_event"
                                                 
    }}

    Make sure that the location of the event is formatted so it is findable by GeoPy (python). The descriptions should be related to and aid any military intelligence efforts. AGAIN, THESE DESCRIPTIONS SHOULD AID ANY MILITARY INTELLIGENCE EFFORTS. And further, make sure the output is valid json.
    Below are some examples: 

############
Example 1:
Input: "In Kamchatka, a formation of ships guarding the water area of the Pacific Fleet conducted training to repel an attack by conditional saboteurs.

According to the exercise scenario, conditional saboteurs entered the territory of the formation headquarters with the aim of causing sabotage and disrupting the operation of the communications system.

After receiving a signal about an attack by unknown armed persons on the checkpoint of the connection, military personnel of the anti-terrorism unit quickly responded and began working out an algorithm of actions to repel the attack and block the saboteurs.

The training was carried out in conditions as close as possible to the real situation, and simulation tools were also actively used.

More than 20 military personnel and 3 units of military equipment took part in the event.

Press service of the Eastern Military District #Kamchatka #saboteurs #PDSS #training #combat training"

Output: [
    {{
        "event": "Training to Repel Attack by Conditional Saboteurs",
        "description": "A formation of ships in Kamchatka, tasked with guarding the Pacific Fleet's water area, conducted training to repel an attack by conditional saboteurs. In the exercise scenario, saboteurs aimed to sabotage the headquarters and disrupt the communications system. Upon receiving a signal about the attack, military personnel responded promptly and practiced their attack repulsion algorithm, blocking the saboteurs. The training involved over 20 military personnel and 3 units of equipment.",
        "location": "Petropavlovsk-Kamchatsky, Kamchatka Krai, Russia"
    }}
]

Example 2: 
Input: "How the traitor Kuzminov was eliminated. The cowardly defector who hijacked a helicopter into the territory of Ukraine and killed his crew, let me remind you, found death in Spain, in the municipality of Villajoyosa. The New York Times tells how it happened.

“Two attackers got out of the car, called out to him and opened fire. Despite being hit by six bullets, most of which struck his torso, Kuzminov managed to run a short distance before collapsing onto a ramp. The killers returned to the car and, as they drove out, ran over Kuzminov’s body.

The two hooded killers who appeared on the surveillance camera footage installed in the parking lot of Kuzminov’s residential complex were clearly professionals who completed their mission and quickly disappeared.”

The traitor, having received a passport in the name of Ukrainian citizen Igor Shevchenko, thought that he had caught his luck by the beard. And he didn’t even try to be quietly modest, so as not to shine once again. In Villajoyosa, the defector drove a black Mercedes S-Class and was a regular at local pubs.

But retribution turned out to be inevitable. Note to all the Russians from the RDK gasket company. @sashakots"

Output: [
    {{
        "event": "Assassination of Defector Kuzminov",
        "description": "Defector Kuzminov, who hijacked a helicopter to Ukraine, was assassinated in Spain's Villajoyosa municipality. Two hooded gunmen fatally shot him and ran over his body before fleeing. Surveillance footage indicated that the killers were professionals. Kuzminov had received a passport under the name Igor Shevchenko and lived a lavish lifestyle in Spain, which made him a target for retribution."
        "location": "Villajoyosa, Alicante, Spain"
    }}
]"
                                                 
Example 3: 
Input: "🇷🇺🇺🇦 Tanks worked against enemy infantry in one of the landings in the Avdeevsky direction"
Output: "[
    {{
        "event": "Tanks in Avdeevsky",
        "description": "Tanks were deployed against enemy infantry in a landing operation in the Avdeevsky direction."
        "location": "Avdiivka, Donetsk Oblast, Ukraine"
    }}
]

Example 4: 
Input: "Smart TV SBER 32, 43, 50, 55, 65. inches. NEW, sealed!💪At a very affordable price!❤️‍🔥If you find it cheaper, we’ll make an even better priceSmart TV with voice assistant Salute🎆(just say what interests you and the TV will do everything for you)

Really cool with a huge number of functions💪Allows you to get a clear and detailed image. Display Technology: Equipped with an LCD panel that provides vibrant colors and good contrast levels. Sound: This TV has built-in speakers that provide stereo sound. It is possible to connect external audio systems or headphones through various audio outputs. Connection: has several connectors for connecting other devices, including HDMI, USB, VGA.

You can: YouTube, TV channels, online cinemas, play games, browse the Internet through a browser.📺Sber 32 inches: HD Ready
There is Wi-Fi, Bluetooth
Android 11 with voice assistant Salute🎆Year of release: 2024 (new)
Price: 10,998 rubles🔥📺Sber 32 inches: Full HD
There is Wi-Fi, Bluetooth
Android 11 with voice assistant Salute🎆Year of release: 2023 (new)
Price: 11,998 rubles🔥📺Sber 43 inches: Full HD
There is Wi-Fi, Bluetooth
Android 11 with voice assistant Salute🎆Year of release: 2024 (new)
Price: 15,498 rubles🔥📺Sber 43 inches: 4K
There is Wi-Fi, Bluetooth
Android 11 with voice assistant Salute🎆Year of release: 2024 (new)
Price: 16,998 rubles🔥📺Sber 50 inches: Ultra HD 4K
There is Wi-Fi, Bluetooth
Android 11 with voice assistant Salute🎆Year of release: 2023 (new)
Price: 22,998 rubles🔥📺Sber 55 inches: Ultra HD 4K
There is Wi-Fi, Bluetooth
Android 11 with voice assistant Salute🎆Year of release: 2023 (new)
Price: 27,998 rubles🔥📺Sber 65 inches: Ultra HD 4K
There is Wi-Fi, Bluetooth
Android 11 with voice assistant Salute🎆Year of release: 2023 (new)
Price: 37,998 rubles🔥let's discuss.
(We will deliver within 2 hours after placing the order)

Write to PM or call!
Kirill📞+7 (949) 340-49-68

Gadget Mafia is always with you🥷"
                                                 
Output: [{{
    event: "NULL",
    description: "NULL",
    location: "NULL"
}}]

Example 5:
Input: "Destruction of an enemy radar and S-300 launcher in the Kharkov area.
Russian intelligence and missile forces did an excellent job. Thanks to their well-coordinated work, the Ukrainian Nazis are minus another S-300 (launcher and radar), as well as personnel.
Show more
Excellent work of our reconnaissance and strike complex, mercilessly and non-stop destroying the enemy on the Belgorod border and in the Kharkov region.
This time, death from heaven overtook the 40V6M radar tower, the S-300 launcher and the personnel who serviced this equipment. This will happen to all our enemies sooner or later, there is no third option."

Output: "[
    {{
        "event": "Destruction of Radar and S-300 Launcher",
        "description": "Russian intelligence and missile forces coordinated to destroy an enemy radar and S-300 launcher in the Kharkov area. Their efforts neutralized both the equipment and the personnel.",
        "location": "Kharkiv, Kharkiv Oblast, Ukraine"
    }},
    {{
        "event": "Destruction on Belgorod Border",
        "description": "Reconnaissance and strike units worked relentlessly, targeting the enemy on the Belgorod border and the Kharkov region. Their precision attacks eliminated key enemy equipment. Russian forces delivered a decisive blow from above, striking the 40V6M radar tower and the S-300 launcher. The personnel operating the equipment were also taken out.",
        "location": "Belgorod, Belgorod Oblast, Russia"
    }}
]"               

Here is the input: {content}

]"""
