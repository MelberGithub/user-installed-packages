
about_file      = 'uip-about.py'

exec_files      = [ 
                    package_name,
                ]
libexec_files   = [ 
                    about_file,
                ]

install_data(
    exec_files,
    install_dir: get_option('bindir')
)

install_data(
    libexec_files,
    install_dir: get_option('libexecdir') /  package_name
)

install_symlink(
    package_name,
    install_dir : get_option('libexecdir') /  package_name,
    pointing_to : about_file
)
