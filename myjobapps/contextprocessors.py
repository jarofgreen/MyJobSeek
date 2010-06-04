"""
A set of request processors that return dictionaries to be merged into a
template context. Each function takes the request object as its only parameter
and returns a dictionary to add to the context.

These are referenced from the setting TEMPLATE_CONTEXT_PROCESSORS and used by
RequestContext.
"""

from models import UserMessage

def userMessages(request):
	if not hasattr(request, 'user') or not request.user.is_authenticated():
		return {}
	messages = UserMessage.objects.filter( User=request.user, isRead=False)
	for m in messages:
		m.isRead = True
		m.save()
	return { 'messages': messages, }
