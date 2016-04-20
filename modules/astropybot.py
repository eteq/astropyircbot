import time

from sopel import module

MAIN_MESSAGE = ("Hi there! Thanks for your interest in Astropy.  We're trying "
                "a new chat medium for Astropy.  We encourage you to try "
                "moving your discussion to our Gitter channel at "
                "https://gitter.im/astropy/astropy. Also note that there's an "
                "IRC<->Gitter bridge avaliable at https://irc.gitter.im/ if "
                "you want to continue using an IRC client.")

# all in seconds
DEFAULT_INTERVAL = 600 # 10 min
MAX_INTERVAL = 3600 * 24 # 24 hours

def get_interval(bot):
    return getattr(bot, 'interval', DEFAULT_INTERVAL)

@module.rule('.*')
def redirect_to_gitter(bot, trigger):
    triggertime = time.time()

    lasttime = getattr(bot, 'last_triggered', triggertime - get_interval(bot) - 1)

    if (triggertime - lasttime) > get_interval(bot):
        bot.say(MAIN_MESSAGE)
        bot.last_triggered = time.time()

@module.commands('calmdown')
def calmdown(bot, trigger):
    bot.say('Sorry.  Will stay silent for {} seconds.'.format(get_interval(bot)), trigger.nick)
    bot.last_triggered = time.time()


@module.commands('reset')
def reset(bot, trigger):
    bot.say("OK, great.  I'm ready and rerring to go!", trigger.nick)
    bot.last_triggered = get_interval(bot) + 1

@module.commands('interval')
def interval(bot, trigger):
    if trigger.groups(2)[1] == 2:
        new_interval = DEFAULT_INTERVAL
    else:
        try:
            new_interval = int(trigger.groups(2)[1])
        except ValueError:
            bot.say("Sorry, I want to help, but I don't know how to figure out what"
                    " interval you wanted based on \"{}\"".format(trigger.groups(2)[1]),
                    trigger.nick)
            return
        new_interval = min(new_interval, MAX_INTERVAL)

    msg = ('OK, new interval will be {} sec ({} min).  You might need to calm '
           'me down or reset me, though.')
    bot.say(msg.format(new_interval, new_interval/60.), trigger.nick)
    bot.interval = new_interval
