import json
import os

class Storage:
    def __init__(self, path):
        self.path = path
        if not os.path.exists(path):
            with open(path, "w") as f:
                json.dump({}, f)

    def _load(self):
        with open(self.path, "r") as f:
            return json.load(f)

    def _save(self, data):
        with open(self.path, "w") as f:
            json.dump(data, f, indent=2)

    def set_consent(self, user_id, consent):
        data = self._load()
        if user_id not in data:
            data[user_id] = {"consent": consent, "bets": []}
        else:
            data[user_id]["consent"] = consent
        self._save(data)

    def has_consent(self, user_id):
        data = self._load()
        return data.get(user_id, {}).get("consent", False)

    def add_bet(self, user_id, amount, frequency):
        data = self._load()
        if user_id not in data:
            data[user_id] = {"consent": False, "bets": []}
        data[user_id]["bets"].append({"amount": amount, "frequency": frequency})
        self._save(data)

    def get_user_data(self, user_id):
        data = self._load()
        user = data.get(user_id)
        if not user or not user["bets"]:
            return None
        last_bet = user["bets"][-1]
        return {"amount": last_bet["amount"], "frequency": last_bet["frequency"]}
