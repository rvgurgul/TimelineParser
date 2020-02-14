from Classes.Parser import Parser


desired = [
    'demand drink from bartender.',
    'request drink from bartender.',
    'got drink from bartender.',
    'rejected drink from bartender.',
    'request drink from waiter.',
    'got drink from waiter.',
    'rejected drink from waiter.',
    'waiter gave up',
    'sipped drink.',
    'took last sip of drink.',
    'gulped drink.',

    'demand cupcake from bartender.',
    'request cupcake from bartender.',
    'got cupcake from bartender.',
    'rejected cupcake from bartender.',
    'request cupcake from waiter.',
    'got cupcake from waiter.',
    'rejected cupcake from waiter.',
    'bit cupcake',
    'took last bite of cupcake.',
    'chomped cupcake.',

    'picked up statue.',
    'put back statue.',

    'spy enters conversation.',
    'spy leaves conversation.',
    'started talking.',
    'interrupted speaker.',

    'spy picks up briefcase.',
    'spy puts down briefcase.',
    'spy returns briefcase.',

    'get book from bookcase.',
    'put book in bookcase.',
    'read book.',

    'action triggered: bug ambassador',
    'action triggered: check watch',
    'action triggered: contact double agent',
    'action triggered: fingerprint ambassador',
    'action triggered: inspect statues',
    'action triggered: purloin guest list',
    'action triggered: seduce target',
    'action triggered: swap statue',
    'action triggered: transfer microfilm'
]


class CountdownActivity(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Countdown Activity")
        if not game.reaches_mwc:
            self.complete = True
        else:
            self.countdown = False

    def parse(self, event):
        if self.complete:
            return

        if not self.countdown:
            if "missions completed. 10 second countdown." in event.desc:
                self.countdown = True
        else:
            if "GameEnd" in event.categories:
                self.complete = True
            elif event.actor == "spy":
                self.results.append(event.desc)


class ContactActivity(Parser):

    def __init__(self, game):
        Parser.__init__(self, "Contact Activity")
        self.contacted = False

    def parse(self, event):
        if not self.contacted:
            if "banana bread uttered." in event.desc:
                self.contacted = event.time
        else:
            if event.time < self.contacted + 10:
                self.results.append(event.desc)
            else:
                self.contacted = False
