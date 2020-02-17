
lights = {
    "marked suspicious.": "Highlight",
    "marked spy suspicious.": "Highlight",
    "marked less suspicious.": "Lowlight",
    "marked spy less suspicious.": "Lowlight",
    "marked neutral suspicion.": "Neutral Light",
    "marked spy neutral suspicion.": "Neutral Light",
    "marked default suspicion.": "Default Light",
    "marked spy default suspicion.": "Default Light",
}
lights_abbreviated = {
    "marked suspicious.": "HL",
    "marked spy suspicious.": "HL",
    "marked less suspicious.": "LL",
    "marked spy less suspicious.": "LL",
    "marked neutral suspicion.": "NL",
    "marked spy neutral suspicion.": "NL",
    "marked default suspicion.": "DL",
    "marked spy default suspicion.": "DL",
}


drink_gulps = {
    "gulped drink.",
    "chomped cupcake."
}

drink_sips = {
    "sipped drink.",
    "took last sip of drink.",
    "bit cupcake.",
    "took last bite of cupcake."
}

drink_accepts = {
    "got drink from waiter.",
    "got cupcake from waiter.",
    "got drink from bartender.",
    "got cupcake from bartender.",
}

drink_rejects_tray = {
    "rejected drink from waiter.",
    "rejected cupcake from waiter.",
}
drink_rejects_bar = {
    "rejected drink from bartender.",
    "rejected cupcake from bartender.",
}
drink_rejects = drink_rejects_bar | drink_rejects_tray

drink_requests_tray = {
    "request drink from waiter.",
    "request cupcake from waiter.",
}
drink_requests_bar = {
    "request drink from bartender.",
    "request cupcake from bartender.",
}
drink_requests = drink_requests_tray | drink_requests_bar

drink_finishes = drink_gulps | {
    "took last sip of drink.",
    "took last bite of cupcake."
}
