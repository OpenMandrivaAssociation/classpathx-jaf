%define gcj_support 1
%define section free
%define jafver  1.1

Name:           classpathx-jaf
Version:        1.1.1
Release:        %mkrel 2.5.1
Epoch:          0
Summary:        GNU JavaBeans(tm) Activation Framework

Group:          Development/Java
License:        LGPL
URL:            http://www.gnu.org/software/classpathx/jaf/jaf.html
Source0:        http://ftp.gnu.org/gnu/classpathx/activation-%{version}.tar.bz2
#Source1:       http://ftp.gnu.org/gnu/classpathx/activation-1.0.tar.gz.sig
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
#Vendor:        JPackage Project
#Distribution:  JPackage
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildRequires:  java-devel
BuildArch:      noarch
%endif
Requires(post): update-alternatives
Requires(postun): update-alternatives
BuildRequires:  java-rpmbuild >= 0:1.5
BuildRequires:  java-devel >= 0:1.4.2
Provides:       jaf = 0:%{jafver}
Provides:       activation = 0:%{jafver}
Obsoletes:      gnujaf <= 0:1.0-0.rc1.1jpp

%description
JAF provides a means to type data and locate components suitable for
performing various kinds of action on it. It extends the UNIX standard
mime.types and mailcap mechanisms for Java.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java
Provides:       jaf-javadoc = 0:%{jafver}
Provides:       activation-javadoc = 0:%{jafver}
Obsoletes:      gnujaf-javadoc <= 0:1.0-0.rc1.1jpp
BuildRequires:  java-javadoc

%description    javadoc
%{summary}.

%prep
%setup -q -n activation-%{version}

%build
export JAVAC=%{javac}
export JAR=%{jar}
export JAVADOC=%{javadoc}
%{configure2_5x}
%{__make}
%{__make} javadoc JAVADOCFLAGS="-link %{_javadocdir}/java"

%install
%{__rm} -rf %{buildroot}
%{makeinstall_std}
pushd %{buildroot}%{_javadir}
%{__mv} activation.jar %{name}-%{version}.jar
%{__ln_s} %{name}-%{version}.jar %{name}.jar
%{__ln_s} %{name}-%{version}.jar jaf.jar
%{__ln_s} %{name}-%{version}.jar activation.jar
popd
%{__mkdir_p} 755 %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__cp} -a docs/* %{buildroot}%{_javadocdir}/%{name}-%{version}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/jaf
%{__ln_s} %{name}-%{version} %{buildroot}%{_javadocdir}/activation

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
%{__rm} -rf %{buildroot}

%post
%{_sbindir}/update-alternatives --install %{_javadir}/jaf.jar jaf %{_javadir}/%{name}.jar 10001
%{_sbindir}/update-alternatives --install %{_javadir}/activation.jar jaf %{_javadir}/%{name}.jar 10001
%if %{gcj_support}
%{update_gcjdb}
%endif

%postun
if [ "$1" = "0" ]; then
    %{_sbindir}/update-alternatives --remove jaf %{_javadir}/%{name}.jar
    %{_sbindir}/update-alternatives --remove activation %{_javadir}/%{name}.jar
fi

%if %{gcj_support}
%{clean_gcjdb}
%endif

%post javadoc
%{_sbindir}/update-alternatives --install %{_javadocdir}/jaf jaf-javadoc %{_javadocdir}/%{name} 10001
%{_sbindir}/update-alternatives --install %{_javadocdir}/jaf activation-javadoc %{_javadocdir}/%{name} 10001

%postun javadoc
if [ "$1" = "0" ]; then
    %{_sbindir}/update-alternatives --remove jaf-javadoc %{_javadocdir}/%{name}
    %{_sbindir}/update-alternatives --remove activation-javadoc %{_javadocdir}/%{name}
fi

if [ $1 -eq 0 ]; then
  %{__rm} -f %{_javadocdir}/%{name}
fi

%files
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog COPYING
%{_javadir}/%{name}.jar
%{_javadir}/%{name}-%{version}.jar
#%{_javadir}/activation-%{jafver}.jar
%ghost %{_javadir}/activation.jar
%ghost %{_javadir}/jaf.jar
#%{_javadir}/jaf-%{jafver}.jar

%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*
%endif

%files javadoc
%defattr(644,root,root,755)
%doc %{_javadocdir}/%{name}-%{version}
%doc %{_javadocdir}/%{name}
%ghost %doc %{_javadocdir}/jaf
%ghost %doc %{_javadocdir}/activation
