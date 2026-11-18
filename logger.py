import sqlite3, datetime

class Logger:

    _instance = None

    def __new__(cls):

        #   
        if cls._instance is None:
            # cree l"objet (premiere fois)
            cls._instance = super().__new__(cls)
            # initialise pas de __init__
            cls._instance._initialiser()
        return cls._instance



    def _initialiser(self):
        self.connexion = sqlite3.connect("logs.db")
        self.connexion.execute(
            "CREATE TABLE IF NOT EXISTS logs (ts TEXT, message TEXT)"
        )
        self.connexion.commit()

    # def __init__(self):
    #     self.connexion = sqlite3.connect("logs.db")
    #     self.connexion.execute(
    #         "CREATE TABLE IF NOT EXISTS logs (ts TEXT, message TEXT)"
    #     )
    #     self.connexion.commit()

    def log(self, message: str) -> None:
        ts = datetime.datetime.now().isoformat()
        self.connexion.execute("INSERT INTO logs VALUES (?, ?)", (ts, message))
        self.connexion.commit()
        print(f"[{ts}] {message}")

    def tous_les_logs(self) -> list[tuple]:
        return self.connexion.execute("SELECT * FROM logs").fetchall()


#verification

l1 = Logger()
l1.log("démarrage")

l2 = Logger()
l2.log("conversion terminée")

# is compare l'espace memoire

print(l1 is l2)              # True
print(len(l1.tous_les_logs()))  # 2 — les deux logs dans la même BD