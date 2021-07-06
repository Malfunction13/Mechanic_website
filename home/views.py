from django.shortcuts import render
from django.utils.safestring import mark_safe


def home(request):
    context = {
    'gmaps': mark_safe('''<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d23459.16169293781!2d23.305848859910306!3d42.69535181659373!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x40aa856dd1517c85%3A0xffb5a61b370ddfaa!2sSofia%20Center%2C%20Sofia!5e0!3m2!1sen!2sbg!4v1611580025430!5m2!1sen!2sbg"
     width="100%" height="100%" frameborder="0" 
     style="border:0; overflow:hidden; border-radius:5px; min-height:400px" allowfullscreen="" tabindex="0"></iframe>''')
               }

    return render(request, 'home/home.html', context)


def about(request):
    context = {
        "title": "About"
    }
    return render(request, 'home/about.html', context)

#
# context = {'g_maps': mark_safe('''<div class="mapouter"><div class="gmap_canvas"><iframe width="100%" height="100%" id="gmap_canvas"
#  src="https://maps.google.com/maps?q=university%20of%20san%20francisco&t=&z=13&ie=UTF8&iwloc=&output=embed"
#   frameborder="0"  scrolling="no" marginheight="0" marginwidth="0"></iframe>
#   <a href="https://embedgooglemap.net/mapv2/"></a></div>
#   <style>.mapouter{position:relative;text-align:center;height:100%;width:100%;}.gmap_canvas
#    {overflow:hidden;background:none!important;height:100%;width:100%;}</style></div>''')
#            }