import time

from sopel import module

MAIN_MESSAGE = ("Hi there! Thanks for your interest in Astropy.  We're trying "
                "a new chat medium for Astropy.  We encourage you to try "
                "moving your discussion to our Gitter channel at "
                "https://gitter.im/astropy/astropy. Also note that there's an "
                "IRC<->Gitter bridge avaliable at https://irc.gitter.im/ if "
                "you want to continue using an IRC client.")

INTERVAL = 600 # in seconds

@module.rule('.*')
def redirect_to_gitter(bot, trigger):
    triggertime = time.time()
    lasttime = getattr(bot, 'last_redirect_to_gitter', triggertime - INTERVAL - 1)

    if (triggertime - lasttime) > INTERVAL:
        bot.say(MAIN_MESSAGE)
        bot.last_redirect_to_gitter = time.time()
