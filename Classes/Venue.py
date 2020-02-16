
class Venue:

    def __init__(self, name, info_dict):
        self.name = name
        # these are properties of the venues themselves (not including guests or time)
        self.suspected_double_agents = info_dict["agents"]
        self.conversations = info_dict["conversation"]
        self.bookshelves = info_dict["bookshelves"]
        self.paintings = info_dict["paintings"]
        self.inspects = info_dict["inspects"]
        self.statues = info_dict["statues"]
        self.windows = info_dict["windows"]
        self.bar = info_dict["bar"]
        self.tray = not self.bar

    def minimal_visit_inspect(self):
        return 1 + self.inspects not in self.statues  # 1 + (0 or 1)

    def printables(self):
        # briefcase + drink + statues + books
        return 2 + sum(self.statues) + len(self.bookshelves)


Aquarium = Venue(name="Aquarium", info_dict={
    "high_view_angle": True,
    "bar": True,
    "statues": [2]*4,
    "inspects": 3,
    "bookshelves": ['Green', 'Blue'],
    "conversations": 3,
    "paintings": 0,
    "windows": 5,
    "agents": 2,
})
Balcony = Venue(name="Balcony", info_dict={
    "high_view_angle": True,
    "bar": False,
    "statues": [],
    "inspects": 0,
    "bookshelves": [],
    "conversations": 1,
    "paintings": 0,
    "windows": 2,
    "agents": 0,
})
Ballroom = Venue(name="Ballroom", info_dict={
    "high_view_angle": False,
    "bar": False,
    "statues": [3]*2,
    "inspects": 3,
    "bookshelves": ['Blue', 'Green'],
    "conversations": 5,
    "paintings": 2,
    "windows": 6,
    "agents": 2,
})
Courtyard = Venue(name="Courtyard", info_dict={
    "high_view_angle": True,
    "bar": False,
    "statues": [2]*2,
    "inspects": 2,
    "bookshelves": [],
    "conversations": 4,
    "paintings": 0,
    "windows": 4,
    "agents": 2,
})
Gallery = Venue(name="Gallery", info_dict={
    "high_view_angle": True,
    "bar": False,
    "statues": [2]*2,
    "inspects": 3,
    "bookshelves": ['Green', 'Blue'],
    "conversations": 2,
    "paintings": 8,
    "windows": 2,
    "agents": 2,
})
Highrise = Venue(name="High-Rise", info_dict={
    "high_view_angle": False,
    "bar": False,
    "statues": [2, 3, 2],
    "inspects": 3,
    "bookshelves": ['Blue', 'Green'],
    "conversations": 2,
    "paintings": 1,
    "windows": 3,
    "agents": 2,
})
Library = Venue(name="Library", info_dict={
    "high_view_angle": True,
    "bar": False,
    "statues": [3]*2,
    "inspects": 3,
    "bookshelves": ['Blue', 'Green', 'Yellow'],
    "conversations": 4,
    "paintings": 3,
    "windows": 4,
    "agents": 3,
})
Moderne = Venue(name="Moderne", info_dict={
    "high_view_angle": False,
    "bar": True,
    "statues": [2]*3,
    "inspects": 3,
    "bookshelves": ['Red', 'Blue', 'Green'],
    "conversations": 4,
    "paintings": 0,
    "windows": 3,
    "agents": 3,
})
Pub = Venue(name="Pub", info_dict={
    "high_view_angle": True,
    "bar": True,
    "statues": [1]*2,
    "inspects": 1,
    "bookshelves": [],
    "conversations": 4,
    "paintings": 0,
    "windows": 3,
    "agents": 2,
})
Redwoods = Venue(name="Redwoods", info_dict={
    "high_view_angle": False,
    "bar": True,
    "statues": [1, 2, 2, 1],
    "inspects": 3,
    "bookshelves": ['Blue', 'Green', 'Red'],
    "conversations": 3,
    "paintings": 0,
    "windows": 5,
    "agents": 2,
})
Teien = Venue(name="Teien", info_dict={
    "high_view_angle": False,
    "bar": False,
    "statues": [3]*2,
    "inspects": 3,
    "bookshelves": ['Green', 'Blue'],
    "conversations": 2,
    "paintings": 0,
    "windows": 5,
    "agents": 2,
})
Terrace = Venue(name="Terrace", info_dict={
    "high_view_angle": True,
    "bar": True,
    "statues": [2]*2,
    "inspects": 3,
    "bookshelves": [],
    "conversations": 2,
    "paintings": 0,
    "windows": 3,
    "agents": 1,
})
Terrace_DM = Venue(name="Terrace (OLD)", info_dict={
    "high_view_angle": True,
    "bar": False,
    "statues": [],
    "inspects": 0,
    "bookshelves": [],
    "conversations": 2,
    "paintings": 0,
    "windows": 3,
    "agents": 1,
})
Veranda = Venue(name="Veranda", info_dict={
    "high_view_angle": False,
    "bar": False,
    "statues": [2]*4,
    "inspects": 3,
    "bookshelves": ['Green', 'Red', 'Blue'],
    "conversations": 5,
    "paintings": 0,
    "windows": 7,
    "agents": 3,
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
    "Terrace_old":  Terrace_DM,
    "Veranda":      Veranda,
}

