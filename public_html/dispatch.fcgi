#!/usr/bin/env /usr/bin/perl

#„¡„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ
#„  [ WebPatio for fluxflex]
#„  dispatch.fcgi
#„  alg
#„  alg.info@gmail.com
#„  https://github.com/alg0002/fluxflex_webpatio
#„¤„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ„Ÿ

use CGI::Fast;
use CGI::Carp qw(fatalsToBrowser);

$scriptrootpath='../scripts';
while ($q = CGI::Fast->new()){
	if( -f "$scriptrootpath$ENV{'PATH_INFO'}" ){
		do "$scriptrootpath$ENV{'PATH_INFO'}";
	}else{
		print "Status: 404 Not Found\n";
	}
};
