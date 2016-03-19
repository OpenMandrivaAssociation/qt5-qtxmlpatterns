%define api %(echo %{version} |cut -d. -f1)
%define major %api
%define beta %nil

%define qtminor %(echo %{version} |cut -d. -f2)
%define qtsubminor %(echo %{version} |cut -d. -f3)

%define qtxmlpatterns %mklibname qt%{api}xmlpatterns %{major}
%define qtxmlpatternsd %mklibname qt%{api}xmlpatterns -d
%define qtxmlpatterns_p_d %mklibname qt%{api}xmlpatterns-private -d

%define _qt5_prefix %{_libdir}/qt%{api}

Name:		qt5-qtxmlpatterns
Version:	5.5.1
%if "%{beta}" != ""
Release:	1.%{beta}.1
%define qttarballdir qtxmlpatterns-opensource-src-%{version}-%{beta}
Source0:	http://download.qt.io/development_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}-%{beta}/submodules/%{qttarballdir}.tar.xz
%else
Release:	3
%define qttarballdir qtxmlpatterns-opensource-src-%{version}
Source0:	http://download.qt.io/official_releases/qt/%(echo %{version}|cut -d. -f1-2)/%{version}/submodules/%{qttarballdir}.tar.xz
%endif
Summary:	Qt GUI toolkit
Group:		Development/KDE and Qt
License:	LGPLv2 with exceptions or GPLv3 with exceptions and GFDL
URL:		http://www.qt.io
BuildRequires:	pkgconfig(Qt5Core) = %{version}
BuildRequires:	pkgconfig(Qt5Network) = %{version}
BuildRequires:	pkgconfig(Qt5Gui) = %{version}
BuildRequires:	pkgconfig(Qt5Widgets) = %{version}
BuildRequires:	qmake5 = %{version}

%description
The QtXmlPatterns module provides support for XPath, XQuery, XSLT and
XML Schema validation.

#------------------------------------------------------------------------------

%package -n	%{qtxmlpatterns}
Summary:	Qt%{api} Component Library
Group:		System/Libraries
Requires:	%{name}-xmlpatterns = %{version}

%description -n %{qtxmlpatterns}
Qt%{api} Component Library.

The QtXmlPatterns module provides support for XPath, XQuery, XSLT and
XML Schema validation.

%files -n %{qtxmlpatterns}
%{_qt5_libdir}/libQt5XmlPatterns.so.%{api}*

#------------------------------------------------------------------------------

%package	xmlpatterns
Summary:	Qt%{api} Xmlpatterns Utility
Group:		Development/KDE and Qt
Provides:	qt5-xmlpatterns = %version-%release
Requires: 	%{qtxmlpatterns} = %version-%release

%description xmlpatterns
Qt%{api} Xmlpatterns Utility.

The QtXmlPatterns module provides support for XPath, XQuery, XSLT and 
XML Schema validation.

%files xmlpatterns
%{_qt5_bindir}/xmlpatterns

#------------------------------------------------------------------------------

%package -n	%{qtxmlpatternsd}
Summary:	Devel files needed to build apps based on QtXmlPatterns
Group:		Development/KDE and Qt
Requires:	%{qtxmlpatterns} = %version

%description -n %{qtxmlpatternsd}
Devel files needed to build apps based on QtXmlPatterns.

%files -n	%{qtxmlpatternsd}
%{_qt5_bindir}/xmlpatternsvalidator
%{_qt5_libdir}/libQt5XmlPatterns.prl
%{_qt5_libdir}/libQt5XmlPatterns.so
%{_qt5_libdir}/pkgconfig/Qt5XmlPatterns.pc
%{_qt5_includedir}/QtXmlPatterns
%exclude %{_qt5_includedir}/QtXmlPatterns/%version
%{_qt5_libdir}/cmake/*
%{_qt5_prefix}/mkspecs/modules/*
%{_qt5_exampledir}/xmlpatterns

#------------------------------------------------------------------------------

%package -n	%{qtxmlpatterns_p_d}
Summary:	Devel files needed to build apps based on QtXmlPatterns
Group:		Development/KDE and Qt
Provides:	qt5-qtxmlpatterns-private-devel = %version
Requires:	%{qtxmlpatternsd} = %version
Requires:	pkgconfig(Qt5Core) = %version

%description -n %{qtxmlpatterns_p_d}
Devel files needed to build apps based on QtXmlPatterns.

%files -n %{qtxmlpatterns_p_d}
%{_qt5_includedir}/QtXmlPatterns/%version

#------------------------------------------------------------------------------

%prep
%setup -q -n %qttarballdir

%build
%qmake_qt5

%make
#------------------------------------------------------------------------------

%install
%makeinstall_std INSTALL_ROOT=%{buildroot}

install -d %{buildroot}/%{_qt5_docdir}

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

# .la and .a files, die, die, die.
rm -f %{buildroot}%{_qt5_libdir}/lib*.la
rm -f %{buildroot}%{_qt5_libdir}/lib*.a
