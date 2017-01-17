from django import template

register = template.Library()

@register.simple_tag
def has_answered_question(profile, question_id):
    print("Calling has_answered_question()")
    votes = profile.vote_set.all()
    for vote in votes:
        if vote.question.id == question_id:
            print("Voter has voted on question %s" % question_id)
            return True
    print("not voted")
    return False
