
fs = import('fs')

img_files       = [
                'uip-main.png',
                'uip-list.png',
                'uip-load.png',
                'uip-missing.png',
                'uip-apt-install.png',
                ]

locale = [
        'am', 'ar', 'bg', 'ca', 'cs', 'da', 'de', 'el', 'es_ES',
        'es', 'et', 'fa', 'fil_PH', 'fi', 'fr_BE', 'fr', 'gl_ES',
        'he_IL', 'hi', 'hr', 'hu', 'id', 'is', 'it', 'ja', 'kk',
        'ko', 'lt', 'mr', 'nb_NO', 'nb', 'nl_BE', 'nl', 'pl',
        'pt_BR', 'pt', 'ro', 'ru', 'sk', 'sl', 'sq', 'sr', 'sv',
        'th', 'tr', 'uk', 'vi', 'zh_CN', 'zh_HK', 'zh_TW'
        ]


foreach i: img_files
    if not fs.is_file('img' / i)
        continue
    endif

    install_data('img' / i,
            install_dir: get_option('datadir') / package_name / 'img')
endforeach

r = run_command( [ './make-help' ],
         capture: true, check: true)

#output = r.stdout().strip()
#outerr = r.stderr().strip()
#message(output)
#message(outerr)

foreach l: locale
        foreach i: img_files
            if not fs.is_file('img' / l / i)
                continue
            endif
            install_data('img' / l / i,
                    install_dir: get_option('datadir') / package_name / 'img' / l)
        endforeach

        if not fs.is_file('help' / l / 'help.html')
            continue
        endif
        install_data('help' / l / 'help.html',
            install_dir:  get_option('datadir') / package_name / 'help' / l )
endforeach

if fs.is_file('help.html')
    install_data('help.html',
        install_dir: get_option('datadir') / package_name)
endif

