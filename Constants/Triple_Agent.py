PARSED_GAME_COUNT = 13476


def search_events(term):
    for ev in all_unique_timeline_events:
        if term in ev:
            print(ev)


all_unique_timeline_events = [
    '45 seconds added to match.',
    'aborted watch check to add time.',
    'action test canceled: contact double agent',
    'action test canceled: purloin guest list',
    'action test canceled: seduce target',
    'action test green: check watch',
    'action test green: contact double agent',
    'action test green: fingerprint ambassador',
    'action test green: inspect statues',
    'action test green: purloin guest list',
    'action test green: seduce target',
    'action test green: swap statue',
    'action test green: transfer microfilm',
    'action test ignored: check watch',
    'action test ignored: contact double agent',
    'action test ignored: fingerprint ambassador',
    'action test ignored: inspect statues',
    'action test ignored: purloin guest list',
    'action test ignored: seduce target',
    'action test ignored: swap statue',
    'action test ignored: transfer microfilm',
    'action test red: check watch',
    'action test red: contact double agent',
    'action test red: fingerprint ambassador',
    'action test red: inspect statues',
    'action test red: purloin guest list',
    'action test red: seduce target',
    'action test red: swap statue',
    'action test red: transfer microfilm',
    'action test white: check watch',
    'action test white: contact double agent',
    'action test white: inspect statues',
    'action test white: purloin guest list',
    'action test white: seduce target',
    'action test white: swap statue',
    'action test white: transfer microfilm',
    'action triggered: bug ambassador',
    'action triggered: check watch',
    'action triggered: contact double agent',
    'action triggered: fingerprint ambassador',
    'action triggered: inspect statues',
    'action triggered: purloin guest list',
    'action triggered: seduce target',
    'action triggered: swap statue',
    'action triggered: transfer microfilm',
    'all statues inspected.',
    'ambassador cast.',
    'ambassador\'s personal space violated.',
    'banana bread aborted.',
    'banana bread uttered.',
    'bartender offered cupcake.',
    'bartender offered drink.',
    'bartender picked next customer.',
    'begin flirtation with seduction target.',
    'begin planting bug while standing.',
    'begin planting bug while walking.',
    'bit cupcake.',
    'bug ambassador enabled.',
    'bug ambassador selected.',
    'bug transitioned from standing to walking.',
    'bugged ambassador while standing.',
    'bugged ambassador while walking.',
    'cast member picked up pending statue.',
    'character picked up pending statue.',
    'chomped cupcake.',
    'civilian cast.',
    'contact double agent enabled.',
    'contact double agent selected.',
    'delegated purloin timer expired.',
    'delegated purloin to dr. m.',
    'delegated purloin to dr. n.',
    'delegated purloin to mr. a.',
    'delegated purloin to mr. c.',
    'delegated purloin to mr. d.',
    'delegated purloin to mr. g.',
    'delegated purloin to mr. i.',
    'delegated purloin to mr. k.',
    'delegated purloin to mr. p.',
    'delegated purloin to mr. q.',
    'delegated purloin to mr. s.',
    'delegated purloin to mr. u.',
    'delegated purloin to ms. b.',
    'delegated purloin to ms. e.',
    'delegated purloin to ms. f.',
    'delegated purloin to ms. h.',
    'delegated purloin to ms. j.',
    'delegated purloin to ms. l.',
    'delegated purloin to ms. o.',
    'delegated purloin to ms. r.',
    'delegated purloin to ms. t.',
    'delegating purloin guest list.',
    'demand drink from bartender.',
    'double agent cast.',
    'double agent contacted.',
    'double agent joined conversation with spy.',
    'double agent left conversation with spy.',
    'dropped statue.',
    'failed flirt with seduction target.',
    'failed planting bug while walking.',
    'fake banana bread started.',
    'fake banana bread uttered.',
    'fingerprint ambassador enabled.',
    'fingerprint ambassador selected.',
    'fingerprinted ambassador.',
    'fingerprinted book.',
    'fingerprinted briefcase.',
    'fingerprinted cupcake.',
    'fingerprinted drink.',
    'fingerprinted statue.',
    'fingerprinting failed.',
    'flirt with seduction target: 100%',
    'flirt with seduction target: 17%',
    'flirt with seduction target: 18%',
    'flirt with seduction target: 19%',
    'flirt with seduction target: 20%',
    'flirt with seduction target: 21%',
    'flirt with seduction target: 22%',
    'flirt with seduction target: 23%',
    'flirt with seduction target: 24%',
    'flirt with seduction target: 25%',
    'flirt with seduction target: 26%',
    'flirt with seduction target: 27%',
    'flirt with seduction target: 28%',
    'flirt with seduction target: 29%',
    'flirt with seduction target: 30%',
    'flirt with seduction target: 31%',
    'flirt with seduction target: 32%',
    'flirt with seduction target: 33%',
    'flirt with seduction target: 34%',
    'flirt with seduction target: 35%',
    'flirt with seduction target: 36%',
    'flirt with seduction target: 37%',
    'flirt with seduction target: 38%',
    'flirt with seduction target: 39%',
    'flirt with seduction target: 40%',
    'flirt with seduction target: 41%',
    'flirt with seduction target: 42%',
    'flirt with seduction target: 43%',
    'flirt with seduction target: 44%',
    'flirt with seduction target: 45%',
    'flirt with seduction target: 46%',
    'flirt with seduction target: 47%',
    'flirt with seduction target: 48%',
    'flirt with seduction target: 49%',
    'flirt with seduction target: 50%',
    'flirt with seduction target: 51%',
    'flirt with seduction target: 52%',
    'flirt with seduction target: 53%',
    'flirt with seduction target: 54%',
    'flirt with seduction target: 55%',
    'flirt with seduction target: 56%',
    'flirt with seduction target: 57%',
    'flirt with seduction target: 58%',
    'flirt with seduction target: 59%',
    'flirt with seduction target: 60%',
    'flirt with seduction target: 61%',
    'flirt with seduction target: 62%',
    'flirt with seduction target: 63%',
    'flirt with seduction target: 64%',
    'flirt with seduction target: 65%',
    'flirt with seduction target: 66%',
    'flirt with seduction target: 67%',
    'flirt with seduction target: 68%',
    'flirt with seduction target: 69%',
    'flirt with seduction target: 70%',
    'flirt with seduction target: 71%',
    'flirt with seduction target: 72%',
    'flirt with seduction target: 73%',
    'flirt with seduction target: 74%',
    'flirt with seduction target: 75%',
    'flirt with seduction target: 76%',
    'flirt with seduction target: 77%',
    'flirt with seduction target: 78%',
    'flirt with seduction target: 79%',
    'flirt with seduction target: 80%',
    'flirt with seduction target: 81%',
    'flirt with seduction target: 82%',
    'flirt with seduction target: 83%',
    'flirt with seduction target: 84%',
    'flirt with seduction target: 85%',
    'flirt with seduction target: 86%',
    'flirt with seduction target: 87%',
    'flirt with seduction target: 88%',
    'flirt with seduction target: 89%',
    'flirt with seduction target: 90%',
    'flirt with seduction target: 91%',
    'flirt with seduction target: 92%',
    'flirt with seduction target: 93%',
    'flirt with seduction target: 94%',
    'flirt with seduction target: 95%',
    'flirt with seduction target: 96%',
    'flirt with seduction target: 97%',
    'flirt with seduction target: 98%',
    'flirt with seduction target: 99%',
    'flirtation cooldown expired.',
    'game started.',
    'get book from bookcase.',
    'got cupcake from bartender.',
    'got cupcake from waiter.',
    'got drink from bartender.',
    'got drink from waiter.',
    'guest list purloin pending.',
    'guest list purloined.',
    'guest list return pending.',
    'guest list returned.',
    'gulped drink.',
    'held statue inspected.',
    'hide microfilm in book.',
    'inspect 1 statue enabled.',
    'inspect 1 statue selected.',
    'inspect 2 statues enabled.',
    'inspect 2 statues selected.',
    'inspect 3 statues enabled.',
    'inspect 3 statues selected.',
    'inspection interrupted.',
    'interrupted speaker.',
    'left alone while attempting banana bread.',
    'left statue inspected.',
    'marked book.',
    'marked less suspicious.',
    'marked neutral suspicion.',
    'marked spy less suspicious.',
    'marked spy neutral suspicion.',
    'marked spy suspicious.',
    'marked suspicious.',
    'missions completed successfully.',
    'missions completed. 10 second countdown.',
    'missions completed. countdown pending.',
    'overtime!',
    'picked up fingerprintable briefcase (difficult).',
    'picked up fingerprintable briefcase.',
    'picked up fingerprintable statue (difficult).',
    'picked up fingerprintable statue.',
    'picked up statue.',
    'purloin guest list aborted.',
    'purloin guest list enabled.',
    'purloin guest list selected.',
    'put back statue.',
    'put book in bookcase.',
    'read book.',
    'real banana bread started.',
    'rejected cupcake from bartender.',
    'rejected cupcake from waiter.',
    'rejected drink from bartender.',
    'rejected drink from waiter.',
    'remove microfilm from book.',
    'request cupcake from bartender.',
    'request cupcake from waiter.',
    'request drink from bartender.',
    'request drink from waiter.',
    'right statue inspected.',
    'seduce target enabled.',
    'seduce target selected.',
    'seduction canceled.',
    'seduction target cast.',
    'sipped drink.',
    'sniper shot civilian.',
    'sniper shot spy.',
    'sniper shot too late for sync.',
    'spy cast.',
    'spy enters conversation.',
    'spy joined conversation with double agent.',
    'spy leaves conversation.',
    'spy left conversation with double agent.',
    'spy picks up briefcase.',
    'spy player takes control from ai.',
    'spy puts down briefcase.',
    'spy ran out of time.',
    'spy returns briefcase.',
    'started fingerprinting book.',
    'started fingerprinting briefcase.',
    'started fingerprinting cupcake.',
    'started fingerprinting drink.',
    'started fingerprinting statue.',
    'started talking.',
    'statue inspection interrupted.',
    'statue swap pending.',
    'statue swapped.',
    'stopped talking.',
    'suspected double agent cast.',
    'swap statue enabled.',
    'swap statue selected.',
    'target seduced.',
    'took last bite of cupcake.',
    'took last sip of drink.',
    'took shot.',
    'transfer microfilm enabled.',
    'transfer microfilm selected.',
    'transferred microfilm.',
    'waiter gave up.',
    'waiter offered cupcake.',
    'waiter offered drink.',
    'waiter stopped offering cupcake.',
    'waiter stopped offering drink.',
    'watch checked to add time.',
    'watch checked.'
]

player_list_scl_5 = {'Cartwright/steam', 'InfamousCupcake/steam', 'Vac58/steam', 'falconhit', 'Rai/steam', 'royalflush',
                     'iggythegrifter', 'degran', 'sgnurf', 'Ryooo/steam', 'Tabsies/steam', 'wodar', 'Watermeat/steam',
                     'dbdkmezz', 'Sun Bro/steam', 'linkvanyali', 'gmantsang', 'howiie', 'AndiVx/steam', 'alteffor',
                     'ThatOdinaryPlayer/steam', 'humankirby', 'Yglini/steam', 'umbertofinito', 'pox', 'ekajarmstro',
                     'orac', 'brskaylor', 'quicklime', 'smonteGaming/steam', 'Tortuga-Man/steam', 'fancypants',
                     'Legorve Genine/steam', 'paratroopa', 'warningtrack', 'hunu', 'Kotte/steam', 'Alexare/steam',
                     'soolseem', 'zerodoom', 'krazycaley', 'gabrio/steam', 'OpiWrites/steam', 'Smiddy/steam',
                     'Vlady/steam', 'monaters', 'sykosloth', 'skrewwl00se', 'arturiax', 'Hectic/steam',
                     'Ranmilia/steam', 'Silverthorn/steam', 'davidw', 'checker', 'Calvin Schoolidge/steam',
                     'spedmonkey', 'amlabella', 'pwndnoob', 'Rooks/steam', 'TheSmiddy/steam', 'tge', 'ninjafairy',
                     'tflameee/steam', 'jd105l', 'Kmars133/steam', 'dels', 'dowsey', 'ml726', 'canadianbacon', 'rooks',
                     'Max Edward Snax/steam', 'sergioc89', 'cleetose', 'the_usual_toaster/steam', 'Libro/steam',
                     'portalfreek', 'yeesh', 'magicdoer1', 'furbyfubar', 'dukit', 'jyaty', 'Harren/steam', 'yerand',
                     'Sheph/steam', 'phimagen/steam', 'Pizzelio/steam', 'scallions', 'lazybear', 'bananaconda',
                     'PixelBandit/steam', 'mrrgrs', 'mintyrug', 'turnout8', 'belial', 'daheadhunter', 'slappydavis',
                     'turnipboy', 'juliusb', 'pofke', 'rta', 'ventuskitsune', 'magician1099', 'kcmmmmm', 'alibi',
                     'ascendbeyond', 'mrtwister'}
player_list_scl_4 = {'c9high', 's76561198018620847/steam', 'monaters', 'ohgodaguy', 'realofoxtrot', 'Smiddy/steam',
                     'portalfreek', 'sikeeatric', 'Watermeat/steam', 'cleetose', 'josiemccoy', 'amlabella', 'sgnurf',
                     'degran', 'cameraman', 'scallions', 'mistajinxy', 'waterhouse', 'drawnonward',
                     'the_usual_toaster/steam', 'quicklime', 'royalflush', 'mastrblastr/steam',
                     's76561198202214763/steam', 'nanthelas', 'varanas', 'slappydavis', 'jyaty', 'fourliberties',
                     'gregdebonis', 'elvisnake', 's76561197960665911/steam', 'xryanmacx', 'magician1099', 'turnipboy',
                     'yerand', 'rta', 'humankirby', 'pox', 'smonteGaming/steam', 'brskaylor', 'Frostie/steam', 'hjkatz',
                     'jecat', 'trevor', 'isauragard', 'toamini', 'yoric', 'iggythegrifter', 'plastikqs', 'catnip',
                     'cronk', 's76561197962409465/steam', 'turnout8', 'steph', 'baldrick', 'warningtrack', 'tristram',
                     'dowsey', 'mrrgrs', 'moon', 'fancypants', 'james1221', 'dukit', 'bloom', 'magicdoer1', 'jinetic',
                     'gmantsang', 'davidw', 's76561198045758510/steam', 'strobo', 'butterscotch', 'walliard',
                     'darkersolstice', 'checker', 'mvem', 'teetery', 'falconhit', 'sharper', 'c0vered/steam',
                     'redscharlach', 'bitbandingpig', 'badplayer', 's76561198028019690/steam', 'paragon12321',
                     's76561197993456144/steam', 'pires', 'Sheph/steam', 'krazycaley', 'incnone', 'Ryooo*/steam',
                     's76561197998032388/steam', 'xemnes', 'pofke', 's76561197962211538/steam', 'arturiax', 'kcmmmmm',
                     'and', 'soolseem', 'kaplow', 'marimo', 'trollikene', 'motionblur', 'doomedbunnies',
                     's76561198054993175/steam', 'TheAlpacalypse/steam', 'zerodoom', 'bayushi', 'Ryooo/steam',
                     'lazybear', 'pwndnoob', 'jackoburst', 'TarekMak/steam', 'Cerinn/steam', 'belial',
                     'pressftopayrespect', 'canadianbacon', 'dbdkmezz', 'skrewwl00se', 'whitenoise', 'leftylink',
                     'wodar', 'pash1k', 's76561197995352411/steam', 'Joez/steam', 'Max Edward Snax/steam', 'basshead',
                     'c00n', 'Alexare/steam', 'ml726', 'essem'}

event_participant_list = {
    "SCL4": player_list_scl_4,
    "SCL5": player_list_scl_5
}

event_division_list = {'SCL5 Hazards_Promos_Finals', 'Summer Cup 2019 Group P', 'Winter Cup 2020 Vixen',
                       'Summer Cup 2019 Group H', 'SCL5 Challenger', 'Summer Cup 2019 Group L', 'Winter Cup 2019',
                       'Summer Cup 2019 Group J', 'Winter Cup 2020 Prancer', 'SCL5 Bronze', 'Summer Cup 2019 Group E',
                       'Winter Cup 2020 Bracket', 'Spooky Invitational Group D', 'SCL5 Diamond', 'SCL4 Silver',
                       'Summer Cup 2018', 'Summer Cup 2019 Group I', 'Spooky Invitational Group A',
                       'SCL4 Hazards_Promos_Finals', 'Winter Cup 2020 Blitzen', 'SCL5 Gold', 'SCL5 Silver',
                       'SCL4 Bronze', 'SCL4 Diamond', 'SCL5 Oak', 'Crew Battles', 'Summer Cup 2019 Group C',
                       'Winter Cup 2020 Cupid', 'SCL4 Copper', 'SCL4 ChallengerTournament', 'SCL5 Obsidian',
                       'Summer Cup 2019 Group O', 'SCL5 Iron', 'SCL5 ToP', 'SCL4 Gold', 'Summer Cup 2019 Bracket',
                       'SCL4 Challenger', 'Winter Cup 2020 Dasher', 'SCL5 Platinum', 'Spooky Invitational Bracket',
                       'Summer Cup 2019 Group M', 'Winter Cup 2020 Donner', 'Summer Cup 2019 Group D',
                       'Winter Cup 2020 Coment', 'Summer Cup 2019 Group B', 'Summer Cup 2019 Group K',
                       'Spooky Invitational Group B', 'Summer Cup 2019 Group N', 'SCL5 Copper',
                       'Summer Cup 2019 Group A', 'SCL4 Platinum', 'Winter Cup 2020 Dancer', 'SCL4 Iron',
                       'Spooky Invitational Group C', 'Summer Cup 2019 Group G', 'Summer Cup 2019 Group F'}

event_list = {
    'Crew Battles': {},
    'SCL4': {'Diamond', 'Hazards_Promos_Finals', 'ChallengerTournament', 'Platinum', 'Bronze', 'Iron', 'Copper', 'Gold', 'Silver', 'Challenger'},
    'SCL5': {'Diamond', 'Hazards_Promos_Finals', 'ToP', 'Obsidian', 'Platinum', 'Bronze', 'Iron', 'Copper', 'Gold', 'Oak', 'Silver', 'Challenger'},
    'Spooky Invitational': {'B', 'Bracket', 'D', 'C', 'A'},
    'Summer Cup 2018': {},
    'Summer Cup 2019': {'B', 'Bracket', 'D', 'E', 'K', 'H', 'C', 'L', 'P', 'N', 'G', 'F', 'J', 'I', 'O', 'A', 'M'},
    'Winter Cup 2019': {},
    'Winter Cup 2020': {'Bracket', 'Prancer', 'Vixen', 'Cupid', 'Blitzen', 'Coment', 'Dasher', 'Donner', 'Dancer'},
}

divisions_list = {'Platinum', 'P', 'Silver', 'Iron', 'B', 'Coment', 'ChallengerTournament', 'I', 'E', 'Oak', 'N',
                  'Dancer', 'Hazards_Promos_Finals', 'F', 'Bronze', 'Challenger', 'Obsidian', 'Dasher', 'C', 'Blitzen',
                  'Donner', 'M', 'Gold', 'Diamond', 'J', 'Vixen', 'A', 'G', 'Prancer', 'O', 'Copper', 'ToP', 'H', 'K',
                  'L', 'Cupid', 'Bracket', 'D'}
