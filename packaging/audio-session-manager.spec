Name:       audio-session-manager
Summary:    Audio Session Manager
%if 0%{?tizen_profile_mobile}
Version:    0.2.8
Release:    0
%else
Version:    0.3.14
Release:    0
VCS:        framework/multimedia/audio-session-manager#audio-session-manager-0.3.5_1-11-g0cbf3d180a6cd7c7d979ec07a765a2a756cebac1
%endif
Group:      System/Libraries
License:    Apache License, Version 2.0
URL:        http://source.tizen.org
Source0:    %{name}-%{version}.tar.gz
Requires(post): /sbin/ldconfig
Requires(post): /usr/bin/vconftool
Requires(postun): /sbin/ldconfig
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(mm-common)
%if "%{_repository}" == "mobile"
BuildRequires:  pkgconfig(sysman)
%endif
BuildRequires:  pkgconfig(vconf)
BuildRequires:  pkgconfig(security-server)


%description
audio-session-manager development package 



%package devel
Summary:    Audio-session-manager package  (devel)
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}

%description devel
Audio-session-manager development package  (devel)


%package sdk-devel
Summary:    auido-session-manager development package for sdk release
Group:      Development/Libraries
Requires:   %{name}-devel = %{version}-%{release}

%description sdk-devel
auido-session-manager development package for sdk release for audio-session


%prep
%setup -q -n audio-session-manager-%{version}


%build
%if 0%{?tizen_profile_mobile}
cd mobile
%else
cd wearable
%endif
%autogen --disable-static --noconfigure
LDFLAGS="$LDFLAGS -Wl,--rpath=%{prefix}/lib -Wl,--hash-style=both -Wl,--as-needed "; export LDFLAGS
CFLAGS="%{optflags} -fvisibility=hidden -DMM_DEBUG_FLAG -DEXPORT_API=\"__attribute__((visibility(\\\"default\\\")))\"" ; export CFLAGS
%if 0%{?tizen_profile_mobile}
%configure --disable-static --enable-security
%else
%configure --disable-static --disable-security
%endif
make %{?jobs:-j%jobs}

%install
rm -rf %{buildroot}

%if 0%{?tizen_profile_mobile}
cd mobile
%else
cd wearable
%endif

mkdir -p %{buildroot}/usr/share/license
cp LICENSE.APLv2 %{buildroot}/usr/share/license/%{name}
%make_install



%post 
/sbin/ldconfig

%if 0%{?tizen_profile_mobile}
vconftool set -t int memory/Sound/SoundStatus "0" -g 29 -f -i
%else
vconftool set -t int memory/Sound/SoundStatus "0" -i -s system::vconf_multimedia
%endif

%postun 
/sbin/ldconfig

%files
%if 0%{?tizen_profile_mobile}
%manifest mobile/audio-session-manager.manifest
%else
%manifest wearable/audio-session-manager.manifest
%endif
%defattr(-,root,root,-)
%{_libdir}/libaudio-session-mgr.so.*
%{_bindir}/asm_testsuite
%{_datadir}/license/%{name}

%files devel
%defattr(-,root,root,-)
%{_includedir}/mmf/audio-session-manager-types.h
%{_includedir}/mmf/audio-session-manager.h


%files sdk-devel
%defattr(-,root,root,-)
%{_includedir}/mmf/audio-session-manager-types.h
%{_includedir}/mmf/audio-session-manager.h
%{_libdir}/libaudio-session-mgr.so
%{_libdir}/pkgconfig/audio-session-mgr.pc


