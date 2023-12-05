from django.shortcuts import render
from django.views import View


class AboutView(View):
    template_name = 'pages/about.html'
    page_name = "pages:about"

    def get(self, request):
        return render(request, self.template_name,
                      {
                          'page_name': self.page_name
                      })


class RulesView(View):
    template_name = 'pages/rules.html'
    page_name = "pages:rules"

    def get(self, request):
        return render(request, self.template_name,
                      {
                          'page_name': self.page_name
                      })


def handler404(request, exception):
    return render(request, 'pages/404.html', status=404)


def handler500(request):
    return render(request, 'pages/500.html', status=500)


def handler403(request, exception):
    return render(request, 'pages/403csrf.html', status=403)
