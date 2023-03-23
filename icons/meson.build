
fs = import('fs')

icondir = get_option('datadir') / 'icons'
pixmaps = get_option('datadir') / 'pixmaps'

icon_names = [
               package_name,
             ]

sizes = [ 8, 16, 22, 24, 32, 48, 64, 96, 128, 256, 512 ]

foreach icon_name: icon_names

    png = '@0@.png'.format(icon_name)
    foreach s: sizes
        sd = s.to_string()
        if not fs.is_dir(sd)
            continue
        endif
        
        if not fs.is_file(sd / png)
            continue
        endif
        
        sxs = '@0@x@0@'.format(s.to_string())
        install_data(sd / png,
            install_dir: icondir / 'hicolor' / sxs / 'apps')
        
        if s == 64
            install_data(sd / png,
                install_dir: pixmaps)
        endif
    endforeach

    sd  = 'scalable'
    svg = '@0@.svg'.format(icon_name)
    if not fs.is_dir(sd)
        continue
    endif
    if not fs.is_file(sd / svg)
        continue
    endif
    install_data(sd / svg,
            install_dir: icondir / 'hicolor' / sd)
    install_data(sd / svg,
            install_dir: icondir / 'hicolor' / sd / 'apps')

endforeach
