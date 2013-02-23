from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

import suggestions.models as models

@login_required(login_url="/suggestions/login/")
def main_page(request):

    # check in user, get user data
    netid = request.META['USER']
    if (models.Voter.objects.filter(user_netid = netid).exists()):
        current_user = models.Voter.objects.get(user_netid = netid)
        current_user.logged_in()
    else:
        current_user = models.Voter(user_netid = netid)
        current_user.save()

    # get list of suggestions
    suggestion_list = models.Suggestion.objects.filter(is_chosen=False, is_completed=False)
    # make a list of tags as strings.
    suggestion_tags  = {}
    for suggestion in suggestion_list:
        suggestion_tags[int(suggestion.pk)] = []
        map(lambda x: suggestion_tags[int(suggestion.pk)].append(x.name),
            list(suggestion.tags.all()))
    for suggestion in suggestion_list:
        suggestion.tag_list = suggestion_tags[suggestion.pk]

    return render_to_response("www/suggestions.html",
                              {
                                "user_data" : current_user, 
                                "suggestion_list" : suggestion_list,
                              },
                              RequestContext(request)
                             )

@login_required(login_url="/suggestions/login/")
def submit_suggestion(request):
    try:
        title       = request.POST.get('suggestion_title')
        description = request.POST.get('suggestion_description')

        netid       = request.META['USER']
        creator     = models.Voter.objects.get(user_netid = netid)

        tags         = request.POST.getlist('suggestion_tags')
        tag_obj_list = []
        for tag in tags:
          if (models.Tag.objects.filter(name = tag).exists()):
            tag_obj_list.append(models.Tag.objects.get(name = tag))
          else:
            new_tag = models.Tag(name = tag)
            new_tag.save()
            tag_obj_list.append(new_tag)

        suggestion  = models.Suggestion(title       = title,
                                        description = description,
                                        creator     = creator,
                                       )
        suggestion.save()
        for tag_obj in tag_obj_list:
            suggestion.tags.add(tag_obj)

        return redirect("/suggestions/")
    except:
      return HttpResponse("error")

@login_required(login_url="/suggestions/login/")
def cast_vote(request):
    try:
        netid    = request.META['USER']
        cast_by  = models.Voter.objects.get(user_netid = netid)

        vote_id  = request.POST.get('vote_id')
        cast_for = models.Suggestion.objects.get(pk = vote_id)

        vote        = models.Vote(cast_by  = cast_by,
                                  cast_for = cast_for
                                 )

        vote.save()
        cast_by.cast_vote()
        cast_for.receive_vote()
        return redirect("/suggestions/")
    except:
        return HttpResponse("error")
