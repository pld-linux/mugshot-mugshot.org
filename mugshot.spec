Summary:	Companion software for mugshot.org
Summary(pl.UTF-8):	Oprogramowanie towarzyszące dla mugshot.org
Name:		mugshot
Version:	1.1.58
Release:	1
License:	GPL
Group:		X11/Applications/Networking
Source0:	http://download.mugshot.org/client/sources/linux/%{name}-%{version}.tar.gz
# Source0-md5:	3506a6873bd24b339abd6d2fc44218fb
Patch1:		%{name}-firefox.patch
URL:		http://mugshot.org/
BuildRequires:	GConf2-devel >= 2.8
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
BuildRequires:	curl-devel >= 7.15
BuildRequires:	dbus-devel >= 1.0
BuildRequires:	dbus-glib-devel >= 0.61
BuildRequires:	desktop-file-utils
BuildRequires:	glib2-devel >= 1:2.6
BuildRequires:	gnome-desktop-devel >= 2.10.0
BuildRequires:	gnome-vfs2-devel >= 2.0
BuildRequires:	gtk+2-devel >= 2:2.10
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	loudmouth-devel >= 1.0.3
BuildRequires:	pcre-devel >= 6.3
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	xorg-lib-libXScrnSaver-devel
BuildRequires:	xulrunner-devel >= 1.5.0.4
Requires(post,postun):	gtk+2
Requires(post,postun):	hicolor-icon-theme
Requires(post,preun):	GConf2
Requires:	loudmouth >= 1.0.3
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Mugshot works with the server at mugshot.org to extend the panel, web
browser, music player and other parts of the desktop with a "live
social experience" and interoperation with online services you and
your friends use. It's fun and easy.

%description -l pl.UTF-8
Mugshot współpracuje z serwerem mugshot.org w celu rozszerzenia
panelu, przeglądarki WWW, odtwarzacza muzyki i innych części
środowiska o "żywe doświadczenia towarzyskie" oraz współpracę z
serwisami online wykorzystywanymi przez użytkownika i jego znajomych.
Jest zabawny i prosty w użyciu.

%package libs
Summary:	Mugshot shared libraries
Summary(pl.UTF-8):	Współdzielone biblioteki Mugshota
Group:		Libraries

%description libs
Mugshot shared libraries.

%description libs -l pl.UTF-8
Współdzielone biblioteki Mugshota.

%package devel
Summary:	Mugshot header files
Summary(pl.UTF-8):	Pliki nagłówkowe Mugshota
Group:		X11/Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Mugshot header files.

%description devel -l pl.UTF-8
Pliki nagłówkowe Mugshota.

%prep
%setup -q
%patch1 -p1

%build
%{__libtoolize}
%{__aclocal}
%{__automake}
%{__autoheader}
%{__autoconf}
%configure \
	--with-gecko-headers=%{_includedir}/xulrunner \
	--with-gecko-idl=%{_includedir}/xulrunner/idl \
	--with-xpidl=%{_bindir}/xpidl

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

# Don't package a .la file for the component .so
rm -f $RPM_BUILD_ROOT%{_libdir}/mugshot/firefox/components/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install mugshot-uri-handler.schemas
%update_icon_cache hicolor

%{_datadir}/%{name}/firefox-update.sh install

%preun
%gconf_schema_uninstall mugshot-uri-handler.schemas

%{_datadir}/%{name}/firefox-update.sh remove

%postun
%update_icon_cache hicolor

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mugshot
%attr(755,root,root) %{_bindir}/mugshot-uri-handler
%dir %{_libdir}/mugshot
%dir %{_libdir}/mugshot/firefox
%{_libdir}/mugshot/firefox/chrome
%{_libdir}/mugshot/firefox/chrome.manifest
%dir %{_libdir}/mugshot/firefox/components
%{_libdir}/mugshot/firefox/components/*.xpt
%attr(755,root,root) %{_libdir}/mugshot/firefox/components/*.so
%{_libdir}/mugshot/firefox/defaults
%{_libdir}/mugshot/firefox/install.rdf
%dir %{_datadir}/mugshot
%{_datadir}/mugshot/version
%attr(755,root,root) %{_datadir}/mugshot/firefox-update.sh
%{_datadir}/dbus-1/services/*.service
%{_desktopdir}/mugshot.desktop
%{_iconsdir}/hicolor/*/apps/*.png
%{_datadir}/gnome/autostart/mugshot-autostart.desktop
%{_sysconfdir}/gconf/schemas/*.schemas

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libddm-1.so.*.*.*

%files devel
%defattr(644,root,root,755)
%{_includedir}/ddm-1
%attr(755,root,root) %{_libdir}/libddm-1.so
%{_libdir}/libddm-1.la
%{_pkgconfigdir}/ddm-1.pc
