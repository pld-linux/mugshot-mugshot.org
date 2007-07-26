Summary:	Companion software for mugshot.org
Name:		mugshot
Version:	1.1.45
Release:	1
License:	GPL
Group:		Applications/Networking
URL:		http://mugshot.org/
Source0:	http://developer.mugshot.org/download/sources/linux/%{name}-%{version}.tar.gz
# Source0-md5:	2bb9f3f9ba0c34a6869749223d921ea9
Patch0: %{name}-as-needed.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	GConf2-devel >= 2.8
BuildRequires:	curl-devel >= 7.15
BuildRequires:	dbus-devel >= 0.61
BuildRequires:	dbus-glib-devel >= 0.61
BuildRequires:	desktop-file-utils
BuildRequires:	glib2-devel >= 2.6
BuildRequires:	gnome-desktop-devel >= 2.10.0
BuildRequires:	gnome-vfs2-devel
BuildRequires:	gtk+2-devel >= 2.6
BuildRequires:	libjpeg-devel >= 6b
BuildRequires:	libssh2-devel
BuildRequires:	loudmouth-devel >= 1.0.3
BuildRequires:	pcre-devel >= 6.3
BuildRequires:	xorg-lib-libXScrnSaver-devel
BuildRequires:	xulrunner-devel >= 1.5.0.4
Requires(post):	GConf2
Requires(post):	gtk+2
Requires(pre):	GConf2
Requires(preun):	GConf2
Requires:	loudmouth >= 1.0.3

%description
Mugshot works with the server at mugshot.org to extend the panel, web
browser, music player and other parts of the desktop with a "live
social experience" and interoperation with online services you and
your friends use. It's fun and easy.


%prep
%setup -q
%patch0 -p1

%build
%{__aclocal}
%{__automake}
%{__autoconf}
%configure \
	--with-gecko-headers=%{_includedir}/xulrunner \
	--with-gecko-idl=%{_includedir}/xulrunner/idl \
	--with-xpidl=%{_bindir}/xpidl

%{__make}


%install
rm -rf $RPM_BUILD_ROOT
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
%{__make} install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

# Don't package a .la file for the component .so
rm -f $RPM_BUILD_ROOT%{_libdir}/mugshot/firefox/components/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install mugshot-uri-handler.schemas
%update_icon_cache hicolor

%preun
%gconf_schema_uninstall mugshot-uri-handler.schemas

%postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/mugshot
%attr(755,root,root) %{_bindir}/mugshot-uri-handler
%{_iconsdir}/hicolor/16x16/apps/*.png
%{_iconsdir}/hicolor/22x22/apps/*.png
%{_iconsdir}/hicolor/24x24/apps/*.png
%{_iconsdir}/hicolor/32x32/apps/*.png
%{_iconsdir}/hicolor/48x48/apps/*.png
%{_iconsdir}/hicolor/128x128/apps/*.png
%{_datadir}/mugshot
%ghost %{_datadir}/mugshot/version
%{_libdir}/mugshot
%{_datadir}/dbus-1/services/*.service
%{_desktopdir}/mugshot.desktop
%{_datadir}/gnome/autostart/mugshot.desktop
%{_sysconfdir}/gconf/schemas/*.schemas
