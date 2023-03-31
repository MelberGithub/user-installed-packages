
inames = [
         package_name,
         ]

sizes = [ 8, 16, 22, 24, 32, 48, 64, 96, 128, 256, 512 ]

icon_dir = get_option('datadir') / 'icons'
pix_maps = get_option('datadir') / 'pixmaps'

fs = import('fs')
foreach iname: inames

    ipng = '@0@.png'.format(iname)
    isvg = '@0@.svg'.format(iname)

    if not fs.is_file(isvg)
        continue
    endif

    foreach size: sizes
        s = size.to_string()
        spng = '@0@-@1@.png'.format(iname, s)
        install_data(
                configure_file(
                    input:  isvg,
                    output: spng,
                    command: [ 'inkscape',
                            '-h', s,
                            '-w', s,
                            '-o', spng,
                            '@INPUT@',
                            ],
                    ),
                rename: ipng,
                install_dir: icon_dir / 'hicolor' / '@0@x@0@'.format(s) / 'apps',
                )

        if size == 64
            install_symlink(
                    ipng,
                    install_dir : get_option('datadir') / 'pixmaps',
                    pointing_to : '../icons/hicolor' / '@0@x@0@'.format(s) / 'apps' / ipng,
                    )
        endif

    endforeach

    install_data(
        isvg,
        install_dir: icon_dir / 'hicolor' / 'scalable' / 'apps'
        )

endforeach
