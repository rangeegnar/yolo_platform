from django.forms import RadioSelect


class ColorSelect(RadioSelect):
    template_name = 'layout/widgets/color_radio/radio.html'
    option_template_name = 'layout/widgets/color_radio/radio_option.html'