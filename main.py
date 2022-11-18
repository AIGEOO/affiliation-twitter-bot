from src.AccountOperations import AccountOperations

if __name__ == "__main__":
    try:
        bot = AccountOperations()
        bot.start()
    except Exception as e:
        print(e)