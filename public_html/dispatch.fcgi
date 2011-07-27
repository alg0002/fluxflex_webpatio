#!/usr/bin/env /usr/bin/perl

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
