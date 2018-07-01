import Pyro4


@Pyro4.expose
class GreetingMaker(object):
    def get_fortune(self, name):
        print("Estou no servidor")
        return "Hello, {0}. Here is your fortune message:\n" \
               "Behold the warranty -- the bold print giveth and the fine print taketh away.".format(
                   name)


daemon = Pyro4.Daemon()
ns = Pyro4.locateNS()
uri = daemon.register(GreetingMaker)
ns.register("example.greeting", str(uri))
print("Ready.")
daemon.requestLoop()
