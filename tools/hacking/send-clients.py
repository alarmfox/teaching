import sys
from webexpythonsdk import WebexAPI

# Access token for authenticating with the Webex API
access_token = "ZjljZTE5MGQtOTY4MS00OWYxLWExZmEtOWVlZDgyMmE4MWEwZGNkZWYyMWMtMWMx_PF84_9db17efa-dc2f-4ca3-90ae-30a52866391a"

# Check if the access token is provided
if access_token is None:
    print("Missing access token")
    sys.exit(1)

# Initialize the Webex API client with the access token
api = WebexAPI(access_token=access_token)

students = [
    "ariannarusso95.ar@gmail.com",
    "arturotesta007@gmail.com",
    "carlo.cirillo04@gmail.com",
    "carotenutochiara@hotmail.com",
    "castaldogiuseppe8@gmail.com",
    "claudiaverdetti@outlook.it",
    "comentale.luca1996@gmail.com",
    "didonato.andrea.info@gmail.com",
    # "do.picariello@studenti.unina.it",
    "federica.ferro.it@gmail.com",
    "gio.depertis@studenti.unina.it",
    "giu.botti98@gmail.com",
    "jhonathan.ragucci@gmail.com",
    "marcotroiano1801@gmail.com",
    "mariogus1999@gmail.com",
    "m.borgstrom@studenti.unina.it",
    "mc25012005@gmail.com",
    "orianabuccelli1@gmail.com",
    "riccardo.brescia@gmail.com",
    "riccardocarta3@gmail.com",
    "salvatore.derosa16@studenti.unina.it",
    "sebastianjo2011@gmail.com",
    "simonedl1999@gmail.com",
    "simoneparente10@gmail.com",
    "m.ciamarra@studenti.unina.it",
    "ilarialessio02@gmail.com",
]

# students = ["giuseppe@capass.org"] * 10

print(len(students), "students")

off = 10
dry = True

for i, student in enumerate(students):
    f = f"./wg-confs/client{i + off}.conf"
    print("Sending", f, "to", student, end="...")
    if not dry:
        api.messages.create(
            toPersonEmail=student,
            files=[f],
            text="This is your VPN configuration file, import this in your Kali Linux machine and follow the instructor.",
        )
    print("done!")
