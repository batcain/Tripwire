from BatDrone import GatherLogs

instance = GatherLogs("YOUR-BOT-TOKEN-HERE")

instance.createHandler("denied", instance.denied)
instance.createHandler("granted", instance.granted)

instance.update.start_polling()
