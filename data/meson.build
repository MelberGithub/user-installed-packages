fs = import('fs')

img_files = [
            'img/uip-main.png',
            'img/uip-list.png',
            'img/uip-load.png',
            'img/uip-missing.png',
            'img/uip-apt-install.png',
            ]

help_html = 'help.html'

html_files = [
            'license.html',
            'help.md',
            help_html
            ]


install_data(
    html_files,
    install_dir: get_option('datadir') / package_name
)
install_data(
    img_files,
    install_dir: get_option('datadir') / package_name / 'img'
)

locale = [
        'am', 'ar', 'bg', 'ca', 'cs', 'da', 'de', 'el', 'es_ES',
        'es', 'et', 'fa', 'fil_PH', 'fi', 'fr_BE', 'fr', 'gl_ES',
        'he_IL', 'hi', 'hr', 'hu', 'id', 'is', 'it', 'ja', 'kk',
        'ko', 'lt', 'mr', 'nb_NO', 'nb', 'nl_BE', 'nl', 'pl',
        'pt_BR', 'pt', 'ro', 'ru', 'sk', 'sl', 'sq', 'sr', 'sv',
        'th', 'tr', 'uk', 'vi', 'zh_CN', 'zh_HK', 'zh_TW'
        ]

foreach l: locale
    if not fs.is_file(l / help_html)
        continue
    endif
    install_data( l / help_html,
    install_dir:  get_option('datadir') / package_name / l )
endforeach
