import src.thread.server as server


with socketserver.UnixStreamServer(server.addres, server.ServerHandeler) as addres:
    addres.send("wazaaa")
