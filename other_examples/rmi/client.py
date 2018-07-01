import Pyro4

name = "Bia"
greeting_maker = Pyro4.Proxy("PYRONAME:example.greeting")
print("Estou no cliente")
print(greeting_maker.get_fortune(name))