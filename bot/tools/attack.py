def attackEntity(bot):
    entity = bot.nearestEntity()

    if entity is None:
        bot.chat("No nearby entities to attack")

    else:
        bot.chat(f"Attacking {entity.name or entity.username}")
        while entity.health > 0:
            bot.attack(entity)