%{!?_httpd_modconfdir: %{expand: %%global _httpd_modconfdir %%{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_confdir: %{expand: %%global _httpd_confdir %{_sysconfdir}/httpd/conf.d}}
%{!?_httpd_moddir: %{expand: %%global _httpd_moddir %%{_libdir}/httpd/modules}}
%{!?_httpd_mmn: %{expand: %%global _httpd_mmn %%(cat %{_includedir}/httpd/.mmn || echo 0-0)}}

%global httpd_pkg_cache_dir /var/cache/httpd/mod_auth_openidc

Name:           mod_auth_openidc
Version:        2.4.0.3
Release:        2
Summary:        OpenID Connect Relying Party module for Apache 2.x HTTP Server
License:        ASL 2.0
URL:            https://github.com/zmartzone/mod_auth_openidc
Source0:        https://github.com/zmartzone/mod_auth_openidc/archive/v%{version}.tar.gz

BuildRequires:  gcc httpd-devel openssl-devel curl-devel jansson-devel
BuildRequires:  pcre-devel autoconf automake cjose-devel jq-devel
Requires:       httpd-mmn = %{_httpd_mmn}

%description
This module enables an Apache 2.x web server to operate as
an OpenID Connect Relying Party(RP) to an OpenID Connect Provider(OP).

%prep
%autosetup -p1

%build
export MODULES_DIR=%{_httpd_moddir}
export APXS2_OPTS='-S LIBEXECDIR=${MODULES_DIR}'
autoreconf
%configure --with-jq=/usr/lib64/ --without-hiredis
make %{?_smp_mflags}

%check
export MODULES_DIR=%{_httpd_moddir}
export APXS2_OPTS='-S LIBEXECDIR=${MODULES_DIR}'
make test

%install
install -d $RPM_BUILD_ROOT%{_httpd_moddir}
make install MODULES_DIR=$RPM_BUILD_ROOT%{_httpd_moddir}

install -m 755 -d $RPM_BUILD_ROOT%{_httpd_modconfdir}
echo 'LoadModule auth_openidc_module modules/mod_auth_openidc.so' > \
        $RPM_BUILD_ROOT%{_httpd_modconfdir}/10-auth_openidc.conf

install -m 755 -d $RPM_BUILD_ROOT%{_httpd_confdir}
install -m 644 auth_openidc.conf $RPM_BUILD_ROOT%{_httpd_confdir}
sed -i 's!/var/cache/apache2/!/var/cache/httpd/!' $RPM_BUILD_ROOT%{_httpd_confdir}/auth_openidc.conf
install -m 700 -d $RPM_BUILD_ROOT%{httpd_pkg_cache_dir}/{metadata,cache}

%files
%doc ChangeLog AUTHORS README.md LICENSE.txt
%{_httpd_moddir}/mod_auth_openidc.so
%config(noreplace) %{_httpd_modconfdir}/10-auth_openidc.conf
%config(noreplace) %{_httpd_confdir}/auth_openidc.conf
%dir %attr(0700, apache, apache) %{httpd_pkg_cache_dir}
%dir %attr(0700, apache, apache) %{httpd_pkg_cache_dir}/{metadata,cache}

%changelog
* Fri Apr 24 2020 Captain Wei <captain.a.wei@gmail.com> 2.4.0.3-2
- Package init
