from instapy import InstaPy
import schedule, time
import functools, random
import os


number_to_like_per_hour = 100
tags = ['photo']
comments = ['good']




# ------------------------------------------------------------------------ #

session = InstaPy(username='', password='')\
        .login()\
        .set_upper_follower_count(limit=2500) \
        .set_do_comment(True, percentage=20) \
        .set_comments(comments);

def catch_exceptions(job_func):
    @functools.wraps(job_func)
    def wrapper(*args, **kwargs):
        try:
            return job_func(*args, **kwargs)
        except:
            import traceback
            print(traceback.format_exc())
            cancel_on_failure = True
            if cancel_on_failure:
                return schedule.CancelJob
    return wrapper

@catch_exceptions
def like_a_bunch_of_stuff():
    global session
    global number_to_like_per_hour
    global tags

    random.shuffle(tags)
    number_liked = 0
    
    print('')
    for index in range(len(tags)):
        tag = tags[index]
        number_to_like = (number_to_like_per_hour - number_liked) // (len(tags) - index)

        print(time.asctime(time.localtime()))
        print("  Going to like " + str(number_to_like) + " pictures tagged #" + tag + ".")

        liked, already_liked, inappropriate, commented \
            = session.like_by_tags([tag], amount=number_to_like+12)

        print("  " + str(liked) + " liked, " + str(already_liked) + " already liked, " \
                + str(inappropriate) + " inappropriate, " + str(commented) + " commented.")

        number_liked += liked
        time.sleep(60*5)

    print('Liked ' + str(number_liked) + ' images this hour' \
        + ' (goal was ' + str(number_to_like_per_hour) + ').')


# Run it once first, because scheduler waits one interval.
schedule.every().hour.do(like_a_bunch_of_stuff)
like_a_bunch_of_stuff()

while 1:
    schedule.run_pending()
    time.sleep(1)
