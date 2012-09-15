Summary:	OpenSP - SGML parser
Name:		opensp
Version:	1.5.2
Release:	13
Epoch:		2
License:	Free (Copyright (C) 1999 The OpenJade group)
Group:		Applications/Publishing/SGML
Source0:	http://heanet.dl.sourceforge.net/openjade/OpenSP-%{version}.tar.gz
# Source0-md5:	670b223c5d12cee40c9137be86b6c39b
Patch0:		%{name}-nolibnsl.patch
Patch1:		%{name}-localedir.patch
URL:		http://openjade.sourceforge.net/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
Requires:	sgml-common
Provides:	sgmlparser
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		sgmldir		/usr/share/sgml
%define		_datadir	%{sgmldir}

%description
A library and a set of tools for validating, parsing and manipulating
SGML and XML documents.

%package devel
Summary:	OpenSP header files
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}

%description devel
OpenSP header files and devel documentation.

%prep
%setup -q -n OpenSP-%{version}
%patch0 -p1
%patch1 -p1

%build
%{__gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-doc-build					\
	--disable-static					\
	--enable-default-catalog=%{_sysconfdir}/sgml/catalog	\
	--enable-default-search-path=%{sgmldir}			\
	--enable-http
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	localedir=%{_prefix}/share/locale \
	pkgdocdir=%{_docdir}/%{name}-%{version}

for i in nsgmls sgmlnorm spam spcat spent; do
	ln -sf o$i $RPM_BUILD_ROOT%{_bindir}/$i
done

# sx conficts with sx from lrzsz package
ln -sf osx $RPM_BUILD_ROOT%{_bindir}/sgml2xml

%find_lang OpenSP

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /usr/sbin/ldconfig
%postun -p /usr/sbin/ldconfig

%files -f OpenSP.lang
%defattr(644,root,root,755)
%{_docdir}/%{name}-%{version}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %ghost %{_libdir}/lib*.so.?
%attr(755,root,root) %{_libdir}/lib*.so.*.*.*
%{_datadir}/OpenSP

%files devel
%defattr(644,root,root,755)
%{_includedir}/OpenSP
%attr(755,root,root) %{_libdir}/lib*.so
%{_libdir}/lib*.la

