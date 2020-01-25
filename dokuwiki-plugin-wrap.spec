%define		plugin		wrap
%define		php_min_version 5.0.0
Summary:	DokuWiki Wrap plugin
Summary(pl.UTF-8):	Wtyczka Wrap dla DokuWiki
Name:		dokuwiki-plugin-%{plugin}
Version:	20110515
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://www.dokuwiki.org/_media/plugin:dokuwiki_plugin_wrap_latest.zip#/%{plugin}-%{version}.zip
# Source0-md5:	2fa1c6cc5cf8d6f3cefa0cc969abae05
URL:		http://www.dokuwiki.org/plugin:wrap
BuildRequires:	rpm-php-pearprov >= 4.4.2-11
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20061106
Requires:	php-common >= 4:%{php_min_version}
Requires:	php-pcre
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

# no pear deps
%define		_noautopear	pear

# exclude optional php dependencies
%define		_noautophp	php-someext

# put it together for rpmbuild
%define		_noautoreq	%{?_noautophp} %{?_noautopear}

%description
Universal plugin which combines the functionality of many other
plugins. Wrap wiki text inside containers (divs or spans) and give
them a class (choose from a variety of preset classes), a width and/or
a language with its associated text direction.

%prep
%setup -qc
mv %{plugin}/* .

version=$(awk '/^date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
%{__rm} $RPM_BUILD_ROOT%{plugindir}/{COPYING,README}

%find_lang %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force js/css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
%dir %{plugindir}
%{plugindir}/*.css
%{plugindir}/*.php
%{plugindir}/*.txt
%{plugindir}/conf
%{plugindir}/images
%{plugindir}/syntax
