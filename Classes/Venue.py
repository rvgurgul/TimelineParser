
class Venue:

    def __init__(self, name, info_dict):
        self.name = name
        # these are properties of the venues themselves (not including guests or time)
        self.suspected_double_agents = info_dict["agents"]
        self.conversations = info_dict["conversations"]
        self.bookshelves = info_dict["bookshelves"]
        self.paintings = info_dict["paintings"]
        self.inspects = info_dict["inspects"]
        self.missions = info_dict["loadout"]
        self.statues = info_dict["statues"]
        self.windows = info_dict["windows"]
        self.bar_pads = info_dict["bar"]
        self.tray = self.bar_pads == 0
        self.bar = not self.tray

    def minimal_visit_inspect(self):
        return 1 + self.inspects not in self.statues  # 1 + (0 or 1)

    def printables(self):
        # briefcase + drink + statues + books
        return 2 + sum(self.statues) + len(self.bookshelves)

    def floor_pads(self):
        return self.windows + self.bar_pads + self.paintings + \
               len(self.conversations) + sum(self.statues) + len(self.bookshelves)

    def __str__(self):
        return self.name


__moderne = ("Bug", "Contact", "Transfer", "Inspect", "Swap", "Seduce", "Purloin", "Fingerprint")
__terrace = ("Bug", "Contact", "Inspect", "Swap", "Seduce", "Purloin", "Fingerprint")
__pullman = ("Bug", "Contact", "Transfer", "Seduce", "Purloin", "Fingerprint")
__balcony = ("Bug", "Contact", "Seduce", "Purloin", "Fingerprint")

__large = ["Large"]
__small = ["Small"]

Aquarium = Venue(name="Aquarium", info_dict={
    "high_view_angle": True,
    "bar": 3,
    "statues": [2]*4,
    "inspects": 3,
    "bookshelves": ['Green', 'Blue'],
    "conversations": __large*3,
    "paintings": 0,
    "windows": 5,
    "agents": 2,
    "loadout": __moderne
})
Balcony = Venue(name="Balcony", info_dict={
    "high_view_angle": True,
    "bar": False,
    "statues": [],
    "inspects": 0,
    "bookshelves": [],
    "conversations": __large,
    "paintings": 0,
    "windows": 2,
    "agents": 0,
    "loadout": __balcony
})
Ballroom = Venue(name="Ballroom", info_dict={
    "high_view_angle": False,
    "bar": False,
    "statues": [3]*2,
    "inspects": 3,
    "bookshelves": ['Blue', 'Green'],
    "conversations": __large*5,
    "paintings": 2,
    "windows": 6,
    "agents": 2,
    "loadout": __moderne
})
Courtyard = Venue(name="Courtyard", info_dict={
    "high_view_angle": True,
    "bar": False,
    "statues": [2]*2,
    "inspects": 2,
    "bookshelves": [],
    "conversations": __large*2+__small*2,
    "paintings": 0,
    "windows": 4,
    "agents": 2,
    "loadout": __terrace
})
Gallery = Venue(name="Gallery", info_dict={
    "high_view_angle": True,
    "bar": False,
    "statues": [2]*2,
    "inspects": 3,
    "bookshelves": ['Green', 'Blue'],
    "conversations": __large+__small,
    "paintings": 8,
    "windows": 2,
    "agents": 2,
    "loadout": __moderne
})
Highrise = Venue(name="High-Rise", info_dict={
    "high_view_angle": False,
    "bar": False,
    "statues": [2, 3, 2],
    "inspects": 3,
    "bookshelves": ['Blue', 'Green'],
    "conversations": __large*2,
    "paintings": 1,
    "windows": 3,
    "agents": 2,
    "loadout": __moderne
})
Library = Venue(name="Library", info_dict={
    "high_view_angle": True,
    "bar": False,
    "statues": [3]*2,
    "inspects": 3,
    "bookshelves": ['Blue', 'Green', 'Green', 'Yellow'],
    "conversations": __large*4,
    "paintings": 3,
    "windows": 4,
    "agents": 3,
    "loadout": __moderne
})
Moderne = Venue(name="Moderne", info_dict={
    "high_view_angle": False,
    "bar": True,
    "statues": [2]*3,
    "inspects": 3,
    "bookshelves": ['Red', 'Blue', 'Green'],
    "conversations": __large*4,
    "paintings": 0,
    "windows": 3,
    "agents": 3,
    "loadout": __moderne
})
Pub = Venue(name="Pub", info_dict={
    "high_view_angle": True,
    "bar": 3,
    "statues": [1]*2,
    "inspects": 1,
    "bookshelves": [],
    "conversations": __large*4,
    "paintings": 0,
    "windows": 3,
    "agents": 2,
    "loadout": __terrace
})
Redwoods = Venue(name="Redwoods", info_dict={
    "high_view_angle": False,
    "bar": True,
    "statues": [1, 2, 2, 1],
    "inspects": 3,
    "bookshelves": ['Blue', 'Green', 'Red'],
    "conversations": __large+__small*2,
    "paintings": 0,
    "windows": 5,
    "agents": 2,
    "loadout": __moderne
})
Teien = Venue(name="Teien", info_dict={
    "high_view_angle": False,
    "bar": False,
    "statues": [3]*2,
    "inspects": 3,
    "bookshelves": ['Green', 'Blue'],
    "conversations": __small*2,
    "paintings": 0,
    "windows": 5,
    "agents": 2,
    "loadout": __moderne
})
Terrace = Venue(name="Terrace", info_dict={
    "high_view_angle": True,
    "bar": True,
    "statues": [2]*2,
    "inspects": 3,
    "bookshelves": [],
    "conversations": __large*2,
    "paintings": 0,
    "windows": 3,
    "agents": 1,
    "loadout": __terrace
})
DoubleModern = Venue(name="Double Modern", info_dict={
    "high_view_angle": True,
    "bar": False,
    "statues": [],
    "inspects": 0,
    "bookshelves": [],
    "conversations": __large*2,
    "paintings": 0,
    "windows": 3,
    "agents": 1,
    "loadout": __balcony
})
Veranda = Venue(name="Veranda", info_dict={
    "high_view_angle": False,
    "bar": False,
    "statues": [2]*4,
    "inspects": 3,
    "bookshelves": ['Green', 'Red', 'Blue'],
    "conversations": __small*5,
    "paintings": 0,
    "windows": 7,
    "agents": 3,
    "loadout": __moderne
})

Venues = {
    "Aquarium":     Aquarium,
    "Balcony":      Balcony,
    "Ballroom":     Ballroom,
    "Courtyard":    Courtyard,
    "Gallery":      Gallery,
    "High-Rise":    Highrise,
    "Library":      Library,
    "Moderne":      Moderne,
    "Pub":          Pub,
    "Redwoods":     Redwoods,
    "Teien":        Teien,
    "Terrace":      Terrace,
    "Terrace_old":  DoubleModern,
    "Veranda":      Veranda,
}

